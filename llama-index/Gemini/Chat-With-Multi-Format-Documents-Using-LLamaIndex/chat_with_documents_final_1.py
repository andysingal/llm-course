# Chat with the following documents
    # .csv - comma-separated values
    # .docx - Microsoft Word
    # .ipynb - Jupyter Notebook
    # .md - Markdown
    # .pdf - Portable Document Format
    # .ppt, .pptm, .pptx - Microsoft PowerPoint
    # .txt - text 

#import statements
import os
import shutil
import streamlit as st 
from tempfile import mkdtemp
from llama_index.llms.palm import PaLM
from llama_index.llms.openai import OpenAI
from llama_index.llms.gemini import Gemini
from llama_index.core import Settings,set_global_service_context
from llama_index.core import SimpleDirectoryReader,VectorStoreIndex,ServiceContext,load_index_from_storage
from llama_index.core.storage.storage_context import StorageContext
from llama_index.embeddings.google import GooglePaLMEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
import tiktoken


# API KEY
os.environ['GOOGLE_API_KEY'] = "YOUR_GOOGLE_API_KEY" 
os.environ['OPENAI_API_KEY'] = "YOUR_OPENAI_API_KEY"


#gemini
def gemini_service_context():
    llm = Gemini()

    embed_model = GooglePaLMEmbedding(
        model_name="models/embedding-gecko-001"
    )

    service_context = ServiceContext.from_defaults(
        llm=llm, embed_model=embed_model
    )
    # set the global default!
    set_global_service_context(service_context) 



#OpenAI
def openai_service_context():
    llm = OpenAI("gpt-3.5-turbo")

    embed_model = OpenAIEmbedding(
        model="text-embedding-3-small"
    )

    service_context = ServiceContext.from_defaults(
        llm=llm,  embed_model=embed_model
    )
    # set the global default!
    set_global_service_context(service_context)


# Custom model Embedding: Gemini & Answer: OpenAI
def custom_model():
    llm = OpenAI()
    embed_model = GooglePaLMEmbedding(
        model_name="models/embedding-gecko-001"
    )
    service_context = ServiceContext.from_defaults(
        llm=llm, embed_model=embed_model
    )
    # set the global default!
    set_global_service_context(service_context)



# Setup a temporary directory for this session
temp_dir = mkdtemp()



#Indexing Documents
def process_documents_for_gemini(temp_dir):
    gemini_service_context()
    """
    Process uploaded documents to create or load an index for querying.
    """
    documents = SimpleDirectoryReader(input_dir=temp_dir).load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist()
    storage_context = StorageContext.from_defaults(persist_dir='./storage')
    index = load_index_from_storage(storage_context=storage_context)
    return index.as_query_engine()

def process_documents_for_openai(temp_dir):
    openai_service_context()
    """
    Process uploaded documents to create or load an index for querying.
    """
    documents = SimpleDirectoryReader(input_dir=temp_dir).load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist()
    storage_context = StorageContext.from_defaults(persist_dir='./storage')
    index = load_index_from_storage(storage_context=storage_context)
    return index.as_query_engine()

def process_documents_for_custom(temp_dir):
    custom_model()
    """
    Process uploaded documents to create or load an index for querying.
    """
    documents = SimpleDirectoryReader(input_dir=temp_dir).load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist()
    storage_context = StorageContext.from_defaults(persist_dir='./storage')
    index = load_index_from_storage(storage_context=storage_context)
    return index.as_query_engine()

#Streamlit app
def app():
    st.title('Chat with Your Documents: LlamaIndex')

    Model = st.sidebar.radio("Choose a model to Chat", ("Gemini","OpenAI","Custom"), index=0)
    print("-"*100)
    print(f"Model: {Model}")

    # Initialize session state for query history if not already done
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []

    # Check if the index has been created
    if 'query_engine' not in st.session_state:
        st.session_state.query_engine = None

    # File uploader in sidebar
    st.sidebar.title("Upload Files")
    uploaded_files = st.sidebar.file_uploader("Choose a file", accept_multiple_files=True)
    if uploaded_files and not st.session_state.query_engine:
        for uploaded_file in uploaded_files:
            with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
        st.sidebar.success('Files uploaded successfully. Processing...')

        if Model == "Gemini":
            #Calling gemini
            with st.spinner('Indexing documents...'):
                st.session_state.query_engine = process_documents_for_gemini(temp_dir)

        elif Model == "OpenAI":
            #calling openai
            with st.spinner('Indexing documents...'):
                st.session_state.query_engine = process_documents_for_openai(temp_dir)
        elif Model == "Custom":
            #calling custom model
            with st.spinner("Indexing documents..."):
                st.session_state.query_engine = process_documents_for_custom(temp_dir)

    # Main body for chat interface
    if st.session_state.query_engine:
        user_query = st.chat_input("Ask a question to your documents:")
        print(f"User input: {user_query}")
        if user_query:
            with st.spinner('Searching for answers...'):
                response = st.session_state.query_engine.query(user_query)
                print(f"Answer: {response}")
                # Store the query and response in session state
                st.session_state.query_history.append((user_query, response))

    # Display the query history in the main body
    if st.session_state.query_history:
        st.subheader("Query History")
        for i, (query, response) in enumerate(st.session_state.query_history, start=1):
            st.markdown(f"**Query {i}:** {query}")
            st.markdown(f"**Response {i}:** {response}")
            st.write("---")

    # Clean up the temporary directory when the session ends
    def cleanup():
        shutil.rmtree(temp_dir)
    
    st.session_state['cleanup'] = cleanup

if 'cleanup' not in st.session_state:
    st.session_state['cleanup'] = lambda: None

app()

# Ensure cleanup happens on script rerun or exit
st.session_state['cleanup']()