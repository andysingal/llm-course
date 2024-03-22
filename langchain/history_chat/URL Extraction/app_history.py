
import os, openai
import warnings, bs4
warnings.filterwarnings("ignore")
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader

#provide key
open_ai_key = ""
if open_ai_key == '':
    try:
        open_ai_key = os.environ['OPENAI_API_KEY']
    except:
        pass
openai.api_key = open_ai_key
os.environ['OPENAI_API_KEY'] = open_ai_key
    
    
def main(url_path, prompt, chat_history):
    bs_strainer = bs4.SoupStrainer(class_=("post-content", "post-title", "post-header"))
    loader = WebBaseLoader(
        web_paths=(url_path,),
        bs_kwargs={"parse_only": bs_strainer},
    )
    docs = loader.load()
    
    # Index documents into search engine
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vector_db = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    
    llm = ChatOpenAI(
        model="gpt-4", temperature=0,
    )
    
    # RAG Chain
    retriever = vector_db.as_retriever()
    contextualize_q_system_prompt = """Given a chat history and the latest user question \
        which might reference context in the chat history, formulate a standalone question \
        which can be understood without the chat history. Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is."""
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )
    contextualize_q_chain = contextualize_q_prompt | llm | StrOutputParser()
    qa_system_prompt = """You are an assistant for question-answering tasks. \
        Use the following pieces of retrieved context to answer the question. \
        If you don't know the answer, just say that you don't know. \

        {context}"""
        
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ]
    )


    def contextualized_question(input: dict):
        if input.get("chat_history"):
            return contextualize_q_chain
        else:
            return input["question"]
        
        
    rag_chain = (
        RunnablePassthrough.assign(
            context=contextualized_question | retriever 
        )
        | qa_prompt
        | llm
        | StrOutputParser()
    )
    response = rag_chain.invoke({"question": prompt, "chat_history": chat_history})
    chat_history.extend([HumanMessage(content=prompt), response])
    print("Assistant: ", response)
    print()
    return chat_history


if __name__ == '__main__':
    chat_history = []
    
    while True:
        prompt = str(input("User: "))
        chat_history = main(os.path.join('https://lilianweng.github.io/posts/2023-06-23-agent/'), prompt, chat_history)
    