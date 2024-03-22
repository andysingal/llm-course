
import os, openai
from typing import List
import warnings
from PyPDF2 import PdfReader
warnings.filterwarnings("ignore")
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import CTransformers
from langchain import PromptTemplate

custom_prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

def set_custom_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """
    prompt = PromptTemplate(template=custom_prompt_template,
                            input_variables=['context', 'question'])
    return prompt
    
    
def load_llm_embeddings():
    llm = CTransformers(
    model="TheBloke/Llama-2-7B-Chat-GGUF",
    model_type="llama",
    config={'max_new_tokens': 2048,
                            'temperature': 0,
                            'context_length': 2048},
    
    temperature=0
    )
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                    model_kwargs={'device': 'cpu'})
    return llm, embeddings

    
    
def main(pdf_path, prompt, chat_history):
    pdf_reader = PdfReader(pdf_path)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    # split into chunks
    text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    # Index documents into search engine
    llm, embeddings = load_llm_embeddings()
    vector_db = FAISS.from_texts(chunks, embeddings)

    
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
    qa_system_prompt = """Use the following pieces of information to answer the user's question.
                        If you don't know the answer, just say that you don't know, don't try to make up an answer.

                        Context: {context}
                        Question: {question}

                        Only return the helpful answer below and nothing else.
                        Helpful answer:
                        """
        
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
        chat_history = main(os.path.join('9cf7eda3-full.pdf'), prompt, chat_history)
    