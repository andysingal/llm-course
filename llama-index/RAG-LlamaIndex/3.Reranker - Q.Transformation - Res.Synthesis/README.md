# Adding reranker, query transformations and response synthesis.

This repository leverages the synergy between Cohere reranker and a hybrid retriever to merge the strengths of keyword and vector-based searches with sophisticated semantic reranking. This innovative approach guarantees not only the retrieval of a wide array of pertinent documents but also organizes them in a manner that aligns seamlessly with the user's intentions.

To enhance query processing, we implement two additional methods:

1. **Multi-Step Transformations**: This method deconstructs intricate queries into simpler, more manageable subquestions, each of which is then executed against the database. The responses obtained from these subquestions guide the construction and execution of follow-up queries, ensuring a comprehensive and detailed exploration of the user's original inquiry.

2. **Refine**: This approach methodically processes each piece of retrieved text, making individual calls to the Large Language Model (LLM) for each text chunk. This sequential refinement enables a progressive enhancement of the answer, ensuring that each chunk contributes to a more complete and accurate response.

By incorporating these methods, the repository not only improves the precision and relevance of search results but also ensures a deeper, more nuanced understanding and response to complex queries, enhancing overall search performance and user experience.

![](https://github.com/felipearosr/GPT-Documents/blob/main/1.Streaming%20-%20Memory%20-%20Sources/images/RAG.gif)

## Table of Contents

1. [Installation Instructions](#installation-instructions)
2. [Usage](#usage)
3. [Reranker](#reranker)
4. [Query Transformations](#query-transformations)
5. [Response Synthesis](#response-synthesis)


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
    - Create a folder named 'data'.
    - Place your documents inside the 'data' folder.
    - Execute the 'ingest.py' script to initiate the loading process.

## Usage

Once the setup is complete, launch the chainlit app using the following command:

```shell
chainlit run -w main.py
```

Feel free to explore the functionalities and contribute to the development of this project. Your feedback and contributions are highly appreciated!

## Reranker

### What is a reranker and why do we use it?

The Cohere reranker is a tool that enhances search quality by semantically reranking documents to align more closely with user queries, without needing major changes to existing systems. It's easy to implement and can be customized for specific needs. When combined with a hybrid retriever, which merges keyword and vector search benefits, the Cohere reranker ensures documents are not just relevant but also correctly prioritized according to the query's semantic intent, thus boosting search accuracy and user satisfaction.

### How do we implement it?

```python
from llama_index.postprocessor.cohere_rerank import CohereRerank

# make sure you add your cohere key to your .env file
cohere_api_key = os.environ.get("COHERE_API_KEY")

@cl.on_chat_start
async def start():
   # ...
   reranker = CohereRerank(api_key=cohere_api_key, top_n=3)

   query_engine = index.as_query_engine(
      streaming=True,
      similarity_top_k=6,
      node_postprocessors=[reranker],  # add this line
      vector_store_query_mode="hybrid",
      query_transform=step_decompose_transform,
      response_synthesizer_mode=ResponseMode.REFINE,
   )
   # ...
```

## Query Transformations

### What are query transformations?

LlamaIndex facilitates query transformations, allowing the conversion of a query into a different form for improved processing. These transformations can be single-step, where the transformation occurs once before execution, or multi-step, involving sequential transformation and execution phases with responses influencing subsequent queries.

Use Cases:

- **HyDE**: This technique generates a hypothetical answer document from a natural language query for more effective embedding lookup.
- **Multi-Step Transformations**: Involves breaking down a complex query into smaller, manageable subquestions, executing each against the index, and using the responses to inform follow-up questions.

In this case we implement the multi-step transformation, feel free to play around with other techniques.

### How do we implement it?

```python
from llama_index.core.indices.query.query_transform.base import StepDecomposeQueryTransform

@cl.on_chat_start
async def start():
   step_decompose_transform = StepDecomposeQueryTransform(llm=MODEL, verbose=True)
   
   query_engine = index.as_query_engine(
      streaming=True,
      similarity_top_k=6,
      node_postprocessors=[reranker],
      vector_store_query_mode="hybrid",
      query_transform=step_decompose_transform, # add this line
      response_synthesizer_mode=ResponseMode.REFINE,
   )
```

## Response Synthesis

### What are the different response modes?

The system supports various response modes for processing and refining answers from retrieved text chunks:

1. **Refine**: Processes each retrieved text chunk sequentially, making separate LLM calls for each, refining the answer progressively with each chunk.

2. **Compact (default)**: Similar to refine, but compacts all chunks before processing, reducing the number of LLM calls needed by concatenating chunks to fit within context windows.

3. **Tree Summarize**: Uses a summary template for all chunks and recursively condenses responses into a single final answer, ideal for summarization with multiple rounds of LLM queries.

4. **Simple Summarize**: Truncates text chunks to fit a single LLM prompt for a quick summary, potentially losing details due to truncation.

5. **No Text**: Fetches nodes without sending them to the LLM, allowing for manual inspection of retrieved chunks.

6. **Accumulate**: Applies the query to each text chunk separately, accumulating responses into an array, useful for separate detailed queries.

7. **Compact Accumulate**: A combination of compact and accumulate, compacting prompts before applying the same query to each, for efficiency with detail.

Each mode is designed for different levels of detail and summarization needs.

For more information visit this [link](https://docs.llamaindex.ai/en/stable/module_guides/deploying/query_engine/response_modes.html).

### How do we implement it?

```python
from llama_index.core.response_synthesizers import ResponseMode

@cl.on_chat_start
async def start():
   query_engine = index.as_query_engine(
      streaming=True,
      similarity_top_k=6,
      node_postprocessors=[reranker],
      vector_store_query_mode="hybrid",
      query_transform=step_decompose_transform,
      response_synthesizer_mode=ResponseMode.REFINE,  # add this line
   )
```
