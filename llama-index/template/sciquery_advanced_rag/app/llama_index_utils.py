import os
from glob import glob
import re

from qdrant_client import QdrantClient, AsyncQdrantClient

from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import StorageContext, SimpleDirectoryReader, Document
from llama_index.core.storage.docstore import SimpleDocumentStore


from llama_index.core.node_parser import (SemanticSplitterNodeParser,
                                          SentenceSplitter,
                                          SentenceWindowNodeParser,
                                          HierarchicalNodeParser
                                          )
from llama_index.core import VectorStoreIndex, StorageContext

from app.pdf_processing_utils import get_page_text, is_int
from config import (OLLAMA_MODEL_NAME,
                    DEBUG,
                    EMBEDDING_MODEL_PATH,
                    QDRANT_URL,
                    QDRANT_API_KEY,
                    QDRANT_COLLECTION_NAME
                    )


def get_llms(model_provider="ollama"):
    if model_provider == "ollama":
        model_name = OLLAMA_MODEL_NAME
        llm = Ollama(model=OLLAMA_MODEL_NAME,request_timeout=120.0)
    else:
        raise ValueError (f"Model provider : {model_provider} not supported. Pick Ollama")
    
    print(f'{"==="*10} LLM {model_name} is loaded successfully using the provider {model_provider}')
    if DEBUG:
        print('Testing the LLM output for query: Who is Paul Graham?')
        print(llm.complete("Who is Paul Graham?"))
    return llm


def get_embedding_model(embedding_provider="huggingface"):
    if embedding_provider=="huggingface":
        embed_model_name = EMBEDDING_MODEL_PATH
        embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL_PATH)
    else:
        raise ValueError (f"Embedding provider : {embedding_provider} not supported. Pick 'huggingface")
    
    print(f'{"==="*10} Embedding {embed_model_name} is loaded successfully using the provider {embedding_provider}')
    if DEBUG:
        print('Testing the Embedding output for query: Hellow World"')
        embeddings = embed_model.get_text_embedding("Hello World!")
        print(len(embeddings))
        print(embeddings[:5])
    return embed_model


def prepare_vector_store(store_collection_name,vector_db="qdrant"):
    if vector_db == "qdrant":
        client = QdrantClient(location=QDRANT_URL,api_key=QDRANT_API_KEY)
        async_client = AsyncQdrantClient(location=QDRANT_URL,api_key=QDRANT_API_KEY)
        vector_store = QdrantVectorStore(client=client,aclient=async_client,collection_name=store_collection_name)
    else:
        raise ValueError (f"Vector db : {vector_db} not supported. Pick 'qdrant")
    print(f'{"==="*10} Vectore Store created using vector db {vector_db}')
    return vector_store


def create_vector_collection(nodes, store_collection_name, vector_db="qdrant"):
    vector_store = prepare_vector_store(store_collection_name,vector_db)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return VectorStoreIndex(nodes,storage_context=storage_context)


def load_vector_collection(store_collection_name, embed_model, vector_db="qdrant"):
    vector_store = prepare_vector_store(store_collection_name,vector_db=vector_db)
    return VectorStoreIndex.from_vector_store(embed_model=embed_model,vector_store=vector_store)


# def index_document(nodes, vector_db, store_collection_name, embed_model):
#     try:
#         # th
#         return load_vector_db(store_collection_name, embed_model, vector_db)
#     except Exception as e:
#         print(f'DB form vector store provider {vector_db} with collection name {store_collection_name} does not exits. Creating one now....')
#         return create_vector_db(nodes, store_collection_name, vector_db)


def save_simple_doc_store(document_nodes,persist_fn):

    doc_store = SimpleDocumentStore()
    doc_store.add_documents(document_nodes)
    
    storage_context = StorageContext.from_defaults(docstore=doc_store)
    storage_context.persist(os.path.join("data",persist_fn))


def get_doc_store(persist_fn):
    return SimpleDocumentStore.from_persist_dir(persist_dir=os.path.join("data",persist_fn))


def basic_clean(txt):
    txt = txt.replace('-\n','') # remove line hyphenated words
    txt = re.sub(r'(?<!\n)\n(?!\n|[A-Z0-9])', ' ', txt) # remove unnecessary line break by merge sentence which starts with lower case
    txt = '\n\n'.join([line for line in txt.split('\n') if not is_int(line)]) # remove line whihc only have number, most likely a page number
    return txt


from app.text_cleaning_helpers import clean as advance_clean
from functools import partial

def prepare_document(pdf_paths,method="simple"):

    cleaning_func = partial(advance_clean,
            extra_whitespace=True,
            broken_paragraphs=True,
            bullets=True,
            ascii=True,
            lowercase=False,
            citations=True,
            merge_split_words=True,
            )

    pattern = os.path.join(pdf_paths, "*.pdf")
    pdf_files = glob(pattern)

    if DEBUG:
        pdf_files = pdf_files[:3]

    try:
        documents = None
        if method == "simple":
            documents = SimpleDirectoryReader(input_files=pdf_files).load_data()  
            for doc in documents:
                doc.text = basic_clean(doc.text)
                doc.text = cleaning_func(doc.text)


        elif method == "manual_parsing":
            documents = []
            for pdf in pdf_files:
                fn = os.path.basename(pdf).split('.')[0]
                documents.extend([Document(text=cleaning_func(page["text"]), metadata=page["metadata"]) for page in get_page_text(pdf,fn)])

                if DEBUG:
                    print(f'Text extraction completed from PDF document at path {pdf}')
        else:
            raise ValueError (f"Invalid Method : {method} not supported. Pick one of 'simple' or 'manual_parsing'")
        return documents
    except Exception as e:
        print(f"An error occurred while creating Document from pdf files: {e}")


def get_node_parser(embed_model, parsing_method="semantic", **kwargs):
    if parsing_method == "semantic":
        # If the distance between two adjacent sentence groups exceeds the breakpoint threshold, it indicates a semantic shift and marks the start of a new node.
        node_parser = SemanticSplitterNodeParser(buffer_size=1, breakpoint_percentile_threshold=95, embed_model=embed_model)
    elif parsing_method == "simple":
        # Check for required kwargs and provide default values or raise error
        chunk_size = kwargs.get("chunk_size")
        chunk_overlap = kwargs.get("chunk_overlap")
        if chunk_size is None or chunk_overlap is None:
            raise ValueError("chunk_size and chunk_overlap must be provided for 'simple' parsing method")
        node_parser = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    elif parsing_method == "sentence_window":
        window_size = kwargs.get("window_size")
        if window_size is None:
            raise ValueError("window_size must be provided for 'sentence_window' parsing method")
        node_parser = SentenceWindowNodeParser.from_defaults(
            window_size=window_size,
            window_metadata_key="window",
            original_text_metadata_key="original_sentence",
        )
    elif parsing_method == "hierarchical":
        node_parser = HierarchicalNodeParser(chunk_sizes=[512, 256, 128])
    else: 
        raise ValueError(f'Invalid Parsing Method: {parsing_method}, choose one of "semantic", "simple", "sentence_window", "hierarchical"')
    
    return node_parser



