[SlideOn-SAE](https://huggingface.co/lightonai/SlideOn-SAE)

SlideOn-SAE maps L2-normalized DenseOn token representations to their top-32 latent activations, followed by ReLU. Its decoder reconstructs the original token representations during SAE pretraining. For retrieval, the included adapter max-pools token activations into one sparse vector per query or document.

```py
from sentence_transformers import SparseEncoder

model = SparseEncoder("lightonai/SlideOn-SAE", trust_remote_code=True)

query_embeddings = model.encode_query(["What is sparse retrieval?"])
document_embeddings = model.encode_document([
    "Sparse retrieval uses inverted indexes to search sparse vectors."
])

print(query_embeddings.shape, document_embeddings.shape)
# torch.Size([1, 32768]) torch.Size([1, 32768])

```
