import torch
from torch import nn
from dataclasses import dataclass
from pathlib import Path
import json
from typing import List, Optional

from mixtral.rope import precompute_freqs_cis, apply_rotary_emb
from mixtral.cache import CacheView, RotatingBufferCache

from xformers.ops.fmha import (
    memory_efficient_attention,
)

@dataclass
class MoeArgs:
    num_experts_per_tok: int
    num_experts: int

@dataclass
class ModelArgs:
    dim: int
    n_layers: int
    head_dim: int
    hidden_dim: int
    n_heads: int
    n_kv_heads: int
    norm_eps: float
    vocab_size: int
    moe: MoeArgs

    max_batch_size: int = 0


@dataclass
class SimpleInputMetadata:
    # rope absolute positions
    positions: torch.Tensor

    @staticmethod
    def from_seqlens(seqlens: List[int], device: torch.device) -> "SimpleInputMetadata":
        return SimpleInputMetadata(
            positions = torch.cat(
                [torch.arange(0, seqlen) for seqlen in seqlens]
            ).to(device=device, dtype=torch.long)
        )


def repeat_kv(keys: torch.Tensor, values: torch.Tensor, repeats: int, dim: int):
    keys = torch.repeat_interleave(keys, repeats=repeats, dim=dim)
    values = torch.repeat_interleave(values, repeats=repeats, dim=dim)
    return keys, values


class Attention(nn.Module):
    def __init__(self, args: ModelArgs, device='cuda', dtype=torch.float16):
        super().__init__()
        self.args = args

        self.n_heads: int = args.n_heads
        self.n_kv_heads: int = args.n_kv_heads
        
        self.repeats = self.n_heads // self.n_kv_heads

        self.scale = self.args.head_dim**-0.5

        self.wq = nn.Linear(
            args.dim,
            args.n_heads * args.head_dim,
            bias=False,
            device='meta',
            dtype=dtype
        )
        self.wq.to_empty(device=device)
        self.wk = nn.Linear(
            args.dim,
            args.n_kv_heads * args.head_dim,
            bias=False,
            device='meta',
            dtype=dtype
        )
        self.wk.to_empty(device=device)
        self.wv = nn.Linear(
            args.dim,
            args.n_kv_heads * args.head_dim,
            bias=False,
            device='meta',
            dtype=dtype
        )
        self.wv.to_empty(device=device)
        self.wo = nn.Linear(
            args.n_heads * args.head_dim,
            args.dim,
            bias=False,
            device='meta',
            dtype=dtype
        )
        self.wo.to_empty(device=device)
        

    def forward(
        self, x: torch.Tensor, 
        freqs_cis: torch.Tensor,
        cache: Optional[CacheView],
    ) -> torch.Tensor:
        seqlen_sum, _ = x.shape

        xq, xk, xv = self.wq(x), self.wk(x), self.wv(x)
        xq = xq.view(seqlen_sum, self.n_heads, self.args.head_dim)
        xk = xk.view(seqlen_sum, self.n_kv_heads, self.args.head_dim)
        xv = xv.view(seqlen_sum, self.n_kv_heads, self.args.head_dim)
        xq, xk = apply_rotary_emb(xq, xk, freqs_cis=freqs_cis)

        xk = xk.to('cuda:0')
        xv = xv.to('cuda:0')

        if cache is None:
            key, val = xk, xv
        elif cache.prefill:
            key, val = cache.interleave_kv(xk, xv)
            cache.update(xk, xv)
        else: 
            cache.update(xk, xv)
            key, val = cache.key, cache.value
            key = key.view(seqlen_sum * cache.sliding_window, self.n_kv_heads, self.args.head_dim)
            val = val.view(seqlen_sum * cache.sliding_window, self.n_kv_heads, self.args.head_dim)

        key, val = key.to(x.device), val.to(x.device)

        # Repeat keys and values to match number of query heads
        key, val = repeat_kv(key, val, self.repeats, dim=1)

        # xformers requires (B=1, S, H, D)
        xq, key, val = xq[None, ...], key[None, ...], val[None, ...]
        output = memory_efficient_attention(xq, key, val, None if cache is None else cache.mask)

        return self.wo(output.view_as(x))

class FeedForward(nn.Module):
    def __init__(self, args: ModelArgs, device='cuda', dtype=torch.float16):
        super().__init__()
        
        self.gate = nn.Linear(args.dim, args.moe['num_experts'],
                              bias=False, device='meta', dtype=dtype)
        self.gate.to_empty(device=device)

        self.experts = torch.nn.ModuleList(
            [FeedForwardExpert(args, device=device, dtype=dtype)
             for _ in range(args.moe['num_experts'])]
        )

    def forward(self, x) -> torch.Tensor:
        g = self.gate(x)
        g = torch.softmax(g, dim=-1)
        weights, expert_indices = torch.topk(g, 2, dim=-1)
        weights /= weights.sum(dim=-1, keepdim=True)

        result = torch.zeros_like(x)
        for batch in range(x.shape[0]):
            w_b, ei_b = weights[batch], expert_indices[batch]
            for i, w in zip(ei_b, w_b):
                result[batch] += w * self.experts[i](x[batch])

        return result

class FeedForwardExpert(nn.Module):
    def __init__(self, args: ModelArgs, device='cuda', dtype=torch.float16):
        super().__init__()

        self.w1 = nn.Linear(
            args.dim,
            args.hidden_dim,
            bias=False,
            device='meta',
            dtype=dtype
        )
        self.w1.to_empty(device=device)
        self.w2 = nn.Linear(
            args.hidden_dim,
            args.dim,
            bias=False,
            device='meta',
            dtype=dtype
        )
        self.w2.to_empty(device=device)
        self.w3 = nn.Linear(
            args.dim,
            args.hidden_dim,
            bias=False,
            device='meta',
            dtype=dtype
        )
        self.w3.to_empty(device=device)

    def forward(self, x) -> torch.Tensor:
        return self.w2(nn.functional.silu(self.w1(x)) * self.w3(x))


class RMSNorm(torch.nn.Module):
    def __init__(self, dim: int, eps: float = 1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def _norm(self, x):
        return x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)

    def forward(self, x):
        output = self._norm(x.float()).type_as(x)
        return output * self.weight


class TransformerBlock(nn.Module):
    def __init__(self, args: ModelArgs, device='cuda', dtype=torch.float16):
        super().__init__()
        self.n_heads = args.n_heads
        self.dim = args.dim
        self.attention = Attention(args, device=device, dtype=dtype)
        self.feed_forward = FeedForward(args=args, device=device, dtype=dtype)
        self.attention_norm = RMSNorm(args.dim, eps=args.norm_eps).to(device, dtype=dtype)
        self.ffn_norm = RMSNorm(args.dim, eps=args.norm_eps).to(device, dtype=dtype)
        self.args = args

    def forward(
        self, x: torch.Tensor, freqs_cis: torch.Tensor, cache: Optional[CacheView]
    ) -> torch.Tensor:
        x = x.to(self.attention_norm.weight.device)
        freqs_cis = freqs_cis.to(self.attention_norm.weight.device)

        r = self.attention.forward(self.attention_norm(x), freqs_cis, cache)
        h = x + r
        r = self.feed_forward.forward(self.ffn_norm(h))
        out = h + r
        return out


class Transformer(nn.Module):
    def __init__(self, args: ModelArgs, devices: List[str], dtype=torch.float16):
        super().__init__()
        self.args = args
        self.vocab_size = args.vocab_size
        self.n_layers = args.n_layers
        assert self.vocab_size > 0

        self.tok_embeddings = nn.Embedding(args.vocab_size, args.dim, device='meta', dtype=dtype)
        self.tok_embeddings.to_empty(device=devices[0])

        self.layers = torch.nn.ModuleList(
            [
                TransformerBlock(args=args, device=devices[(i * len(devices)) // args.n_layers], dtype=dtype)
                for i in range(args.n_layers)
            ]
        )

        self.norm = RMSNorm(args.dim, eps=args.norm_eps).to(devices[0], dtype=dtype)

        self.output = nn.Linear(
            args.dim,
            args.vocab_size,
            bias=False,
            device='meta',
            dtype=dtype
        )
        self.output.to_empty(device=devices[0])

        self.freqs_cis = precompute_freqs_cis(self.args.head_dim, 128_000, 1e6).to(devices[0])

    @property
    def dtype(self) -> torch.dtype:
        return self.tok_embeddings.weight.dtype

    @property
    def device(self) -> torch.device:
        return self.tok_embeddings.weight.device

    def forward_partial(
        self,
        input_ids: torch.Tensor,
        seqlens: List[int],
        cache: Optional[RotatingBufferCache]=None,
    ) -> torch.Tensor:
        assert len(seqlens) <= self.args.max_batch_size, f"Max batch size is {self.args.max_batch_size}, got batch size of {len(seqlens)}"
        assert sum(seqlens) == input_ids.shape[0], (sum(seqlens), input_ids.shape[0])
        if cache is not None:
            input_metadata = cache.get_input_metadata(seqlens)
        else:
            input_metadata = SimpleInputMetadata.from_seqlens(seqlens, self.device)
        h = self.tok_embeddings(input_ids)
        freqs_cis = self.freqs_cis[input_metadata.positions]

        for layer_id, layer in enumerate(self.layers):
            cache_view = None if cache is None else cache.get_view(layer_id, input_metadata)
            h = layer(h, freqs_cis, cache_view)
        
        h = h.to(self.norm.weight.device)
        
        if cache is not None:
            cache.update_seqlens(seqlens)

        return self.norm(h)

    def forward(
        self,
        input_ids: torch.Tensor,
        seqlens: List[int],
        cache: Optional[RotatingBufferCache]=None,
    ) -> torch.Tensor:
        return self.output(self.forward_partial(
            input_ids, seqlens, cache=cache
        )).float()

    @staticmethod
    def from_folder(folder: Path, max_batch_size: int = 1, devices=['cuda'], dtype=torch.float16) -> "Transformer":
        with open(folder / 'params.json', 'r') as f:
            model_args = ModelArgs(**json.loads(f.read()))
        model_args.max_batch_size = max_batch_size
        model = Transformer(model_args, devices, dtype=dtype)
        loaded = torch.load(folder / 'consolidated.00.pth')
        model.load_state_dict(loaded)
        return model