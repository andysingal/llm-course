
[Running Claude Code for Free with Gemma 4 and Ollama](https://www.analyticsvidhya.com/blog/2026/04/running-gemma-4-locally/)

#### Document Loader & Chunker Script (using Claude Code CLI)
- Write a Python script in 'scripts/data_peocessor". This script should use 'langchain_community.document_loaders' (specifically 'PyMuPDFLoader' for PDFs and 'TextLoader' for TXT) and     
   'langchain.text_splitter.RecursiveCharacterTextSplitter'. It loads documents from the 'data' directory. Chunks are 1000 characters with 100 overlaps. Each chunk must retain its         
  original source and page metadata.Make sure the script handles multiple file types and returns the processed chunks as a list of Langchain 'Document' objects

### Embedding & Vector Store Script (using Claude Code CLI)
- Create a Python script in 'scripts/vector_db_manager.py'. This script should take a list o Langchain 'Document' objects.It generates embeddings using the Ollama embedding model
  ('OllamaEmbeddings' from 'langchain_community.embeddings', modl 'gemma4:2b'). Then, it persists them into a ChromaDB instance in the 'vector_store' directory. It must also have a        
  function to load an existing ChromaDB  

  #### RAG Query Function (using Claude Code CLI)
  - Develop a Python function in app.py' called 'query_second_brain(query_text:str)'. This function loads the ChromaDB. It retrieves the top 3 relevant chunks based on confidence          
  scrore. It then uses 'langchain_openai.ChatOpenAI' (configured for Ollama's API: 'base_url="http://localhostt:11434/v1"', 'model="gemma4:e2b"') to  answer 'query_text' using the       
  rerieved chunks as context. Use a clear RAG prompt structure. Show the full function 

  #### Summarization Function (using Claude Code CLI) 
  - Add a Python function to 'app.py' called 'summarize_document(file_path:str)'. This function should load the document, pass its content to the locl Gemm4 model via ollama, and return a concise summary. Use a suitable prompt for summarization

  #### We gave it a simple prompt

  - analyse the @second_brain/ project and make a full plan to make the project functional

  
