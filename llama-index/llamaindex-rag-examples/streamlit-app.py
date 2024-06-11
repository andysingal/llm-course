from openai import AzureOpenAI
import streamlit as st
import chromadb.utils.embedding_functions as embedding_functions
import chromadb
from chromadb.config import Settings
from llama_index.core import PromptTemplate

st.title("SEGES-GPT")

client = AzureOpenAI(api_key=st.secrets["OPENAI_API_KEY"], 
                api_version="2024-05-01-preview", 
                azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"])

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=st.secrets["OPENAI_API_KEY"],
    model_name="text-embedding-ada-002",
    api_type="azure",
    api_version="2024-05-01-preview"
)

chroma_client_load = chromadb.PersistentClient(
    path="./landsforsøg/data/baseline-rag/chromadb",
    settings=Settings(allow_reset=True)
)

# Get the existing collection by name
collection_load = chroma_client_load.get_collection(name="landsforsoeg", embedding_function=openai_ef)
###

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt4"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Define the default prompt template


default_prompt = """You are a helpful assistant that answers questions about the content of documents and provides detailed expert advice. 
    You must provide your answer in the Danish language.
    If the answer contains multiple steps or points, provide the answer in a bullet format.
    Below the answer, the source of the answer should be provided including file_name and page number.
    ---------------------
    {context}
    ---------------------
    Given the context information and not prior knowledge, answer the query.
    Query: {query}
    Answer: 
    """

# Add a text input in the sidebar to configure the prompt template
prompt_template = st.sidebar.text_area("Prompt Template", default_prompt)


if query := st.chat_input("Stil et spørgsmål"):
    
    #RAG
    result = collection_load.query(query_texts=[query], n_results=5)
    context = result["documents"][0]
    prompt = PromptTemplate(
    """You are a helpful assistant that answers questions about the content of documents and provides detailed expert advice. 
    You must provide your answer in the Danish language.
    If the answer contains multiple steps or points, provide the answer in a bullet format.
    Below the answer, the source of the answer should be provided including file_name and page number.
    ---------------------
    {context}
    ---------------------
    Given the context information and not prior knowledge, answer the query.
    Query: {query}
    Answer: 
    """)

    prompt = PromptTemplate(prompt_template)

    
    message = prompt.format(query=query, context="\n\n".join(context))
    ###

    st.session_state.messages.append({"role": "user", "content": query}) #message
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in [{"role": "user", "content": message}]#st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.write("RAG Chunks:")
    st.json(context, expanded=False)