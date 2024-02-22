import os
import chromadb
import phoenix as px

from langchain import hub
from langchain.llms import ollama
from langchain.chains import RetrievalQA
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from phoenix.trace.langchain import LangChainInstrumentor

# path dirs
chroma_path = "C:/Users/~/"
document_dir = "C:/Users/~/"

# Start Phoenix server and Instrument LangChain
session = px.launch_app()
LangChainInstrumentor().instrument()

def load_documents(document_dir):
    """Loads PDF documents from the specified directory, handling errors and splitting PDFs."""

    loader_cls = PyPDFLoader  # Only use PyPDFLoader for this function

    for filename in os.listdir(document_dir):
        if os.path.splitext(filename)[1].lower() == ".pdf":  # Check for lowercase ".pdf" extension
            try:
                loader = loader_cls(os.path.join(document_dir, filename))             
                doc = loader.load()
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000,chunk_overlap=300)
                chunks = text_splitter.split_documents(doc)
                
            except Exception as e:
                print(f"Error loading {filename}: {e}")  # Log any errors

    return chunks


def RAG(query:str):
     
    # Create Chroma client and database
    chunks = load_documents(document_dir)
    client = chromadb.PersistentClient(path=chroma_path)
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(client=client, embedding_function=embedding_function, collection_name="KnowledgeBase")
    db.add_documents(chunks)
       
    llm = ollama.Ollama(model="mistral", temperature=0.7) # setup llm
    rag_prompt_llama = hub.pull("rlm/rag-prompt-llama") # setup prompt
    
    # Use db.as_retriever() for retrieval
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever(),
                chain_type_kwargs={"prompt": rag_prompt_llama})

    return qa_chain.invoke({"query": query})

while True:
    user_input = input("You: ")
    # If the user types "exit", exit the loop
    if user_input == "exit":
        break
    response = RAG(user_input)
    print(response)

px.active_session().url
