# Adding vector db, hybrid retriever and improved ingestion

In this updated version, we've added three major features to enhance the repository:

1. **Vector DB Integration**: We've integrated Pinecone for efficient vector data handling, improving real-time analysis and insight extraction.

2. **Hybrid Retriever**: Implements a blend of dense and sparse vector methods, enhancing search accuracy and relevance.

3. **Advanced Ingestion**: Employs specialized techniques like Unstructured for general documents and LLM Sherpa for PDFs, plus metadata enhancement to improve document retrievability and context for LLMs.

![](https://github.com/felipearosr/GPT-Documents/blob/main/1.Streaming%20-%20Memory%20-%20Sources/images/RAG.gif)

## Table of Contents

1. [Installation Instructions](#installation-instructions)
2. [Usage](#usage)
3. [Pinecone](#pinecone)
4. [Hybrid Retriever](#hybrid-retriever)
5. [Advanced Ingestion](#advanced-ingestion)

## Installation Instructions

Follow these steps to set up the GPT Documents chatbot on your local machine:

1. Create a conda environment:

   ```shell
   conda create -n rag python==3.11 -y && source activate rag
   ```

2. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

3. Load your documents into the vector store by: 
    - Create a folder named `data`.
    - Place your documents inside the `data` folder.
    - Execute the `ingest.py` script to initiate the loading process.

## Usage

Once the setup is complete, launch the chainlit app using the following command:

```shell
chainlit run -w main.py
```

Feel free to explore the functionalities and contribute to the development of this project. Your feedback and contributions are highly appreciated!

## Pinecone

### What is Pinecone?

Pinecone is a specialized vector database designed to optimize the storage and querying of vector embeddings. This capability enables efficient real-time analysis and extraction of insights from complex, large-scale data. Its architecture is specifically tuned for handling the intricacies of vector data, making it an ideal choice for applications requiring rapid retrieval and analysis of such information.

In the provided example, Pinecone is utilized to create a hybrid index, which is a critical component for a hybrid retriever system. This system leverages both textual and vector-based data to enhance search and retrieval capabilities. While Pinecone is highlighted for its effective handling of vector embeddings and support for hybrid indexing, it's worth noting that other vector databases offering similar types of indexing could also be considered based on project requirements and specific use cases.

By adopting Pinecone or a similar vector database, developers can implement advanced retrieval systems that combine the strengths of traditional and vector-based search methods, leading to more nuanced and efficient data handling and retrieval solutions.

### How do we implement it?
`main.py`
```python
from pinecone import Pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore

pinecone_api_key = os.environ.get("PINECONE_API_KEY")

@cl.cache
def load_context():
    pc = Pinecone(api_key=pinecone_api_key)
    pinecone_index = pc.Index("pinecone-index")
    vector_store = PineconeVectorStore(
        pinecone_index=pinecone_index,
    )

    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
    )
    return index
```
`ingest.py`
```python
from pinecone import Pinecone, PodSpec
from llama_index.vector_stores.pinecone import PineconeVectorStore

pinecone_api_key = os.environ.get("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)

def get_pinecone_index(pc, index_name):
    pinecone_index = pc.Index(index_name)
    return pinecone_index


def get_pinecone_vector_store(pinecone_index):
    vector_store = PineconeVectorStore(
        pinecone_index=pinecone_index,
        add_sparse_vector=True,
    )
    return vector_store
```
Use `--gen` flag to generate a pinecone pod if you haven't created one already.
`ingest.py --gen`
def create_pinecone_pod(pc, index_name):
    print("Creating pinecone pod")
    pc.create_index(
        name=index_name,
        dimension=3072,
        metric="dotproduct",
        spec=PodSpec(environment="gcp-starter"),
    )

## Hybrid Retriever

### What is an Hybrid Retriever?

A hybrid retriever is a sophisticated tool used in information retrieval systems, combining the best features of both dense and sparse vector methods to enhance search results' accuracy and relevance. In the context of AI and data search, this means leveraging the strengths of both context-understanding capabilities (dense vectors) and keyword-matching skills (sparse vectors).

Typically, dense vectors are excellent at grasping the overall context of a query but may miss out on important keyword-specific details. On the other hand, sparse vectors excel at identifying exact keyword matches but might lack in understanding the broader context. A hybrid retriever merges these approaches, providing a more balanced and effective retrieval mechanism.

For instance, in the field of document retrieval, such as with academic papers or medical abstracts, a hybrid approach can be particularly beneficial. By combining the contextual understanding of dense vector models with the precision of sparse retrieval methods like BM25, a hybrid retrieval pipeline can significantly improve the relevance and accuracy of search results.

In practical applications, hybrid retrievers involve creating and processing both sparse and dense vectors for documents and queries. This includes tokenization processes for sparse vectors and embedding generation for dense vectors, as well as the management of these vectors within a suitable database or search engine like Pinecone or Weaviate. The retrieval process then utilizes these vectors to deliver highly relevant search results, balancing the depth of context and specificity of keywords.


### How do we implement it?
```python
@cl.on_chat_start
async def start():
    # ...
    # What is important here is adding `vector_store_query_mode="hybrid"`
    # Is also really important to change what type of index you have, make sure
    # that you read the ingestion part of this README.
    query_engine = index.as_query_engine(
        streaming=True,
        similarity_top_k=4,
        vector_store_query_mode="hybrid", # Added line of code
    )
    # ...
```
## Advanced Ingestion

### What is advanced ingestion?

Advanced ingestion involves specialized methods to optimize documents for better retrieval by large language models (LLMs). We use two main approaches:

1. **Unstructured**: Applied for all document types except PDFs, enhancing data extraction and structuring to improve LLM readability. Explore various connectors from Llama Index for optimal results. More details [here](https://github.com/Unstructured-IO/unstructured).

2. **Llama Parse**: Specifically for processing PDFs, transforming them into a more LLM-friendly format. Check it out [here](https://github.com/run-llama/llama_parse).

3. **Metadata Enhancement**: We're incorporating metadata into the documents for enriched context and searchability. You have the option to exclude them as needed. However, be mindful that each piece of metadata incurs a processing cost by the LLM due to the additional analysis required.

### How do we implement it?

```unstructured```
```python
UnstructuredReader = download_loader("UnstructuredReader")

file_extractor = {
    # ...
    ".html": UnstructuredReader(),
       ".txt": UnstructuredReader(),
}
director_reader = SimpleDirectoryReader(
        input_dir=input_dir, file_extractor=file_extractor
)
documents = director_reader.load_data(show_progress=True)
```

`llama parse`
```python
llama_parser = LlamaParse(api_key=llama_parse_api_key, result_type="markdown", verbose=True)

file_extractor = {
    ".pdf": llama_parser,
    # ...
}
director_reader = SimpleDirectoryReader(
        input_dir=input_dir, file_extractor=file_extractor
)
documents = director_reader.load_data(show_progress=True)
```

`metadata enhancement`
```python
pipeline = IngestionPipeline(
   transformations=[
      SentenceSplitter(chunk_size=512, chunk_overlap=126),
         TitleExtractor(llm=llm, num_workers=num_workers),
         QuestionsAnsweredExtractor(questions=3, llm=llm, num_workers=num_workers),
         SummaryExtractor(summaries=["prev", "self"], llm=llm, num_workers=num_workers),
         KeywordExtractor(keywords=5, llm=llm, num_workers=num_workers),
         OpenAIEmbedding(model=EMBEDDING)
      ],
   vector_store=vector_store,
)
pipeline.run(documents=documents, show_progress=True, num_workers=num_workers)
```
