```py
import torch
from typing import Any, List
from pydantic import Extra
from langchain.embeddings.base import Embeddings
from sentence_transformers import SentenceTransformer

device = 'cpu'

class CustomEmbedding(Embeddings):

    client: Any  #: :meta private:
    tokenizer: Any
    context_sequence_length: int = 512
    query_sequence_length: int = 512
    model_name: str = ''
    """Model name to use."""

    def __init__(self, **kwargs: Any):
        """Initialize the sentence_transformer."""
        # super().__init__(**kwargs)
        self.client = SentenceTransformer(
            'BAAI/bge-m3',
            device=device,
            trust_remote_code=True)
        self.context_sequence_length = 512
        self.query_sequence_length = 512

    class Config:
        extra = Extra.forbid

    @staticmethod
    def mean_pooling(model_output, attention_mask):
        # First element of model_output contains all token embeddings
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(
            -1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / \
            torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:

        with torch.no_grad():
            embeddings = self.client.encode(texts)
        embeddings = embeddings.astype('float32')
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]
        


# 使用测试
model = CustomEmbedding()
emb = model.embed_query("张三")
print(len(emb))
```
