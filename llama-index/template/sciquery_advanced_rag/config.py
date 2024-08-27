EMBEDDING_MODEL_PATH = "mixedbread-ai/mxbai-embed-large-v1" #'all-MiniLM-L6-v2'

# https://huggingface.co/dunzhang/stella_en_400M_v5
# dunzhang/stella_en_400M_v5
# Instruct: Given a web search query, retrieve relevant passages that answer the query.\nQuery: {query}

RERANKER_MODEL_PATH = "mixedbread-ai/mxbai-rerank-base-v1"
PDF_DATA_DIR = "data/documents"
INDEX_AND_BIB_DIR = "data/index_and_bib"
INDEX_ARRAY_NAME = "index.npy"
BIB_JSON_NAME = "bibliographies.json"

TOP_K_RETRIEVED = 5
TOP_K_RANKED = 1
OLLAMA_MODEL_NAME = "llama3.1:latest"
DEVICE = "MPS" 
GENERATION_KWARGS = {"temperature":0.85,
                     "top_p": 1.0}

QDRANT_URL = "" 
QDRANT_API_KEY = "" 
QDRANT_COLLECTION_NAME = "sciquery_collection"
MAX_TOKENS = 4096

DEBUG = False