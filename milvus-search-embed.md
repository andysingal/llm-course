[Funnel Search with Matryoshka Embeddings](https://milvus.io/docs/funnel_search_with_matryoshka.md)

[Graph RAG with Milvus](https://milvus.io/docs/graph_rag_with_milvus.md#Graph-RAG-with-Milvus)

#### Article

[How to make RAG 32x memory efficient (explained with code)!](https://x.com/_avichawla/status/2040326889928356122)

- Ingest documents and generate binary embeddings.
- Create a binary vector index and store embeddings in the vector DB:  we generate text embeddings (in float32) and convert them to binary vectors, resulting in a 32x reduction in memory and storage.
```
import numpy as np
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-large-en-v1.5",
    trust_remote_code=True,
    cache_folder='./hf_cache'
)

for context in batch_iterate(documents, batch_size=512):
    # Generate float32 vector embeddings
    batch_embeds = embed_model.get_text_embedding_batch(context)
    # Convert float32 vectors to binary vectors
    embeds_array = np.array(batch_embeds)
    binary_embeds = np.where(embeds_array > 0, 1, 0).astype(np.uint8)
    # Convert to bytes array
    packed_embeds = np.packbits(binary_embeds, axis=1)
    byte_embeds = [vec.tobytes() for vec in packed_embeds]

    binary_embeddings.extend(byte_embeds)
```

### Vector indexing: 
After our binary quantization is done, we store and index the vectors in a Milvus vector database for efficient retrieval.
```
from pymilvus import MilvusClient, DataType

# Initialize client and schema
client = MilvusClient("milvus_binary_quantized.db")
schema = client.create_schema(auto_id=True, enable_dynamic_fields=True)

# Add fields to schema
schema.add_field(field_name="context", datatype=DataType.VARCHAR)
schema.add_field(field_name="binary_vector", datatype=DataType.BINARY_VECTOR)

# Create index parameters for binary vectors
index_params = client.prepare_index_params()
index_params.add_index(
    field_name="binary_vector",
    index_name="binary_vector_index",
    index_type="BIN_FLAT",  # Exact search for binary vectors
    metric_type="HAMMING"   # Hamming distance for binary vectors
)

# Create collection with schema and index
client.create_collection(
    collection_name="fastest-rag",
    schema=schema,
    index_params=index_params
)

# Insert data to index
client.insert(
    collection_name="fastest-rag",
    data=[
        {"context": context, "binary_vector": binary_embedding}
        for context, binary_embedding in zip(batch_context, binary_embeddings)
    ]
)
```


- Retrieve top-k similar documents to the user's query.

In the retrieval stage, we:
- Embed the user query and apply binary quantization to it.
- Use Hamming distance as the search metric to compare binary vectors.
- Retrieve the top 5 most similar chunks.
- Add the retrieved chunks to the context.
```
# Generate float32 query embedding
query_embedding = embed_model.get_query_embedding(query)
# Apply binary quantization to query
binary_query = binary_quantize(query_embedding)

# Perform similarity search using Milvus
search_results = client.search(
    collection_name="fastest-rag",
    data=[binary_query],
    anns_field="binary_vector",
    search_params={"metric_type": "HAMMING"},
    output_fields=["context"],
    limit=5  # Retrieve top 5 similar chunks
)

# Store retrieved context
full_context = []
for res in search_results:
    context = res["payload"]["context"]
    full_context.append(context)
```

- LLM generates a response based on additional context.

Moving on, we build a generation pipeline using the Kimi-K2 instruct model, served on the fastest AI inference by Groq.
We specify both the query and the retrieved context in a prompt template and pass it to the LLM.

```
from llama_index.llms.groq import Groq
from llama_index.core.base.llms.types import (
    ChatMessage, MessageRole )

llm = Groq(
    model="moonshotai/kimi-k2-instruct",
    api_key=groq_api_key,
    temperature=0.5,
    max_tokens=1000
)

prompt_template = (
    "Context information is below.\n"
    "---------------------\n"
    "CONTEXT: {context}\n"
    "---------------------\n"
    "Given the context information above think step by step "
    "to answer the user's query in a crisp and concise manner. "
    "In case you don't know the answer say 'I don't know!'.\n"
    "QUERY: {query}\n"
    "ANSWER: "
)

query = "Provide concise breakdown of the document"

prompt = prompt_template.format(context=full_context, query=query)
user_msg = ChatMessage(role=MessageRole.USER, content=prompt)

# Stream response from LLM
streaming_response = llm.stream_complete(user_msg.content)
```
