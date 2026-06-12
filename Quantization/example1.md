```py
from optimum.quanto import freeze, qfloat8, quantize
from diffusers import PixArtSigmaPipeline
import torch
 
pipeline = PixArtSigmaPipeline.from_pretrained(
    "PixArt-alpha/PixArt-Sigma-XL-2-1024-MS", torch_dtype=torch.float16
).to("cuda")
 
quantize(pipeline.transformer, weights=qfloat8)
freeze(pipeline.transformer)

image = pipeline("ghibli style, a fantasy landscape with castles").images[0]

```


Resource: 

-[Quanto-Transformers](https://www.cnblogs.com/huggingface/p/18388714)
- [headroom](https://github.com/chopratejas/headroom)

Headroom compresses everything your AI agent reads — tool outputs, logs, RAG chunks, files, and conversation history — before it reaches the LLM. Same answers, fraction of the tokens.
