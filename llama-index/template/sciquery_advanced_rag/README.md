# SciQuery (WIP): Advanced RAG System using LlamaIndex

This repository demonstrates the use of the llama index library for Advance Retrieval-Augmented Generation (RAG), specifically designed for scientific literature Q&A. It showcases a multiple RAG system, building using several chunking and retrieval methods. In addition to that it also uses Qdrant vector database to persist embeddings. This approach help in understanding how different RAG technique works. The system also provides an API for updating, deleting, and quering documents in the index.

## Steps to Implement SciQuery:

To get started, you need to download scientific literatures and save it in the `$PDF_DATA_DIR` folder for initial indexing. The application will creates an index of all documents using several chunking methods and persist their embeddings along with metadata on Qdrant vector DB.

### Step 1: PDF Processing:
The first step involves processing PDF documents and converting them into text. We provide two options, one, default `llama_index's` pdf parsing and second using the `PyMuPDF` library to extract text from pdfs.

We use regex to identify the starting point of the `Reference` section, which is useful for cleaning bibliography from each paper.

### Step 2: Chunking:
The system provides several chunking methods to process and divide text into manageable segments or "nodes". Suitable method can be choosen after emperical testing: to different use cases and requirements:

  1. Semantic Chunking:
    This method splits text based on semantic shifts. It uses an embedding model to detect changes in meaning, creating a new chunk whenever a significant semantic difference is identified. This is useful for tasks where preserving the coherence of meaning is important.

  2. Simple Chunking:
    This method divides text into fixed-size chunks, with a specified overlap between consecutive chunks. It is straightforward and useful for scenarios where equal-sized segments are needed, regardless of content. 

  3. Sentence Window Chunking (sentence_window):
    This method uses a sliding window to generate chunks, moving over the text with a specified window size. Each window captures a group of sentences, allowing for overlapping segments that provide context continuity. 
  
  4. Hierarchical Chunking (hierarchical):
    This method creates a hierarchical structure of chunks, using different sizes for different levels. It enables a layered representation of text, which is beneficial for complex tasks requiring multi-level analysis or summary. It uses predefined chunk sizes for different hierarchy levels (e.g., 512, 256, 128).

### Step 3: Embedding:

For effective semantic search, it is crucial to obtain vector embeddings of text passages. We generate these embeddings using the [Sentence Transformer](https://pypi.org/project/sentence-transformers/) library and [MixedBread Embedding](https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1).

These embeddings, along with the original text passages and their metadata, are saved on Qdrant vector store.

### Step 4: Retrieval Techniques (WIP):
we provide variety of Retrieval-Augmented Generation (RAG) techniques to enhance the effectiveness of text retrieval and generation. These techniques are designed to improve the quality and relevance of generated responses by utilizing structured retrieval processes. Below is a brief explanation of each supported RAG technique:

  1. RAG with Hierarchical Indexing:
    This technique utilizes a hierarchical structure to organize and index documents. By segmenting documents into different levels of granularity, it enables efficient and precise retrieval of relevant information based on the query context. This hierarchical approach enhances the ability to handle large and complex documents.
    
  2. Contextual Compression:
    Contextual compression reduces the amount of irrelevant information presented to the language model by compressing the retrieved context. It intelligently selects and condenses only the most relevant portions of text, allowing the model to focus on key information, thereby improving both retrieval accuracy and response generation quality.

  3. Adaptive Retrieval:
    Adaptive retrieval dynamically adjusts the retrieval strategy based on the nature of the query and the context. This method enables the system to use different retrieval methods or parameters in real-time, ensuring that the most relevant information is obtained for varying types of questions or requests.

  4. Sophisticated Controllable Agent:
    This technique involves using advanced control mechanisms to guide the behavior of the retrieval and generation process. The controllable agent can adjust various aspects of retrieval, such as selecting specific indices or tuning relevance scores, to tailor the output to meet specific user requirements or task objectives.
  
  5. Recursive Retrieval:
    Recursive retrieval repeatedly refines the search process by using initial retrieval results to form new queries. This iterative approach allows the system to drill down deeper into the available data, progressively refining the search results to find the most relevant and specific information.
  
  6. Context Enrichment using QA and Summary:
    Description
  
  7. DocumentSummaryIndex Retrieval:
    DocumentSummaryIndex retrieval focuses on using pre-computed summaries of documents to improve retrieval efficiency. By indexing summaries rather than full documents, this method speeds up the retrieval process and ensures that the most relevant and concise information is used to inform the generation process.


## REST API Endpoints

The SciQuery system exposes several REST API endpoints to manage and query the document index. Below is a description of each endpoint, along with example `curl` commands for interacting with them.

### 1. **Manage Index**

This resource handles operations related to managing the document index, including retrieving, adding, and deleting documents.

- **GET `/api/documents`**

  Fetches a dictionary mapping UUIDs to filenames of all PDF documents currently in the index. Later, these UUID can be use to delete a document from INDEX.

  **Example `curl` Command:**
  ```bash
  curl -X GET "http://localhost:5000/api/documents"
  ```

  **Sample Response**
  ```json
  {
  "00da0765-ab15-4553-9ea1-3cfab674b3b0": "levy2014_neural_word_embeddings_implicit_matrix_factorization.pdf",
  "01c79fe2-7f76-487f-97c9-32b30ad89b75": "bojaniwski2017_enriching_we_with_subword_info_fasttext.pdf",
  "0307bfb7-e32c-49bd-8df0-eb197cf92660": "wudredze2019_betobentzbecas.pdf",
  "088a5d31-0228-4647-aa5f-bc9456c80cf4": "conneau2017_word_translation_without_parallel_data_muse_csls.pdf",
  "09a653e3-212e-4229-8685-930f2e8b013c": "lample2018_words_translation_withou_pralell.pdf",
  }
  ```

- **DELETE `/api/documents/<string:uid>`**

  Deletes a document from the index by its UUID. Replace `<string:uid>` with the actual UUID of the document you want to delete.

  **Example `curl` Command:**
  ```bash
  curl -X DELETE "http://localhost:5000/api/documents/00da0765-ab15-4553-9ea1-3cfab674b3b0"
  ```

  **Sample Response**
  ```json
  {
    "message": "Document with UID 01c79fe2-7f76-487f-97c9-32b30ad89b75 and filename bojaniwski2017_enriching_we_with_subword_info_fasttext.pdf deleted successfully from Index"
  }
  ```
  **You can see File with UUID "01c79fe2-7f76-487f-97c9-32b30ad89b75" is deleted from Index**
  ```json
  {
  "00da0765-ab15-4553-9ea1-3cfab674b3b0": "levy2014_neural_word_embeddings_implicit_matrix_factorization.pdf",
  "0307bfb7-e32c-49bd-8df0-eb197cf92660": "wudredze2019_betobentzbecas.pdf",
  "088a5d31-0228-4647-aa5f-bc9456c80cf4": "conneau2017_word_translation_without_parallel_data_muse_csls.pdf",
  "09a653e3-212e-4229-8685-930f2e8b013c": "lample2018_words_translation_withou_pralell.pdf",
  }
  ```

- **POST `/api/documents`**

  Adds a new PDF document to the index. The PDF file should be included in the form-data under the key `file`.

  **Example `curl` Command:**
  ```bash
  curl -X POST "http://localhost:5000/api/documents" \
  -F "file=@/path/to/bojaniwski2017_enriching_we_with_subword_info_fasttext.pdf.pdf"
  ```

  **Sample Response**
  ```json
  {
    "filename": "bojaniwski2017_enriching_we_with_subword_info_fasttext.pdf",
    "uid": "bd49bc59-cea9-4eaa-84c2-53b43a5dc93e"
  }
  ```

  **You can see "bojaniwski2017_enriching_we_with_subword_info_fasttext.pdf" is added back to the Index but with different UUID**
  ```json
  {
  "00da0765-ab15-4553-9ea1-3cfab674b3b0": "levy2014_neural_word_embeddings_implicit_matrix_factorization.pdf",
  "0307bfb7-e32c-49bd-8df0-eb197cf92660": "wudredze2019_betobentzbecas.pdf",
  "088a5d31-0228-4647-aa5f-bc9456c80cf4": "conneau2017_word_translation_without_parallel_data_muse_csls.pdf",
  "09a653e3-212e-4229-8685-930f2e8b013c": "lample2018_words_translation_withou_pralell.pdf",
  "bd49bc59-cea9-4eaa-84c2-53b43a5dc93e": "bojaniwski2017_enriching_we_with_subword_info_fasttext.pdf",
  }
  ```


### 2. **Query Index**

This resource processes queries to retrieve relevant information from the indexed documents.

- **POST `/api/query`**

  Sends a query to retrieve relevant passages and generate an answer. The query should be provided in the JSON body under the key `query`.

  **Example `curl` Command:**
  ```bash
  curl -X POST "http://localhost:5000/api/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain what is ULMFIT?"}'
  ```

  **Sample Response with [TRUNCATED] passage**
  ```json
  {
    "query": "Explain what is ULMFIT?",
    "answer": "\nULMFiT is a transfer learning method for NLP (Natural Language Processing) that can be applied to any NLP task. It is a type of language model fine-tuning that uses a universal language model (ULM) as a starting point for adapting to specific NLP tasks. ULMFiT enables robust learning across a diverse range of tasks and prevents catastrophic forgetting, which means it can retain knowledge from previous tasks while learning new ones. It is an effective and extremely sample-efficient transfer learning method that can significantly outperform existing transfer learning techniques and the state-of-the-art on representative text classification tasks.",
    "metadata": [
        {
            "passage": "## Discussion and future directions\nWhile we have shown that ULMFiT can achieve state-of-the-art performance on widely used text classification tasks, we believe that language model fine-tuning will be particularly useful in the following settings compared to existing transfer learning approaches (Conneau et al., 2017; McCann et al., 2017; Peters et al., 2018): a) NLP for non-English languages, [TRUNCATED] .....",
            "pdf_path": "data/documents/ruder2019_ulmfit.pdf",
        }
    ]
  }
  ```

## Installation and Setup

To get started with SciQuery, follow these steps to set up your Python environment, install the required dependencies, and start the Flask application.

1. **Create a Python Virtual Environment**

   First, create a virtual environment to manage your project's dependencies. Run the following command:

   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment**

   Activate the virtual environment. The command depends on your operating system:

   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

3. **Install Required Dependencies**

   With the virtual environment activated, install the necessary packages using `pip`. Make sure to also install [MLX](https://pypi.org/project/mlx-llm/) library for Apple Silicon. This library is useful to load quantized model on Apple Silicon.:

   ```bash
   pip install -r requirements.txt
   ```

4. **Start the Flask Application**

   Finally, start the Flask application using the following command:

   ```bash
   flask run
   ```

Make sure to set any necessary environment variables as specified in the `config.py` file before running the application.

TODO: 
- [ ] Test Docker script.
- [ ] Improve PDF parsing.

Replace `http://localhost:5000` with the actual base URL of your SciQuery API server. For the `POST` and `DELETE` requests, make sure to use the appropriate file paths and UUIDs as needed.

Thank you for exploring the SciQuery project. If you have any questions or contributions, please feel free to reach out.
