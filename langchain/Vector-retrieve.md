```py
import os

import chromadb
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import OpenAIEmbeddings

# OpenAI embedding model
EMBEDDING_MODEL = "text-embedding-3-small"

# ChromaDB
CHROMA_PERSIST_DIRECTORY = os.environ.get("CHROMA_PERSIST_DIRECTORY")
CHROMA_COLLECTION_NAME = os.environ.get("CHROMA_COLLECTION_NAME")

# Retriever settings
TOP_K_VECTOR = 10

# 既存のChromaDBを読み込みVector Retrieverを作成
def vector_retriever(top_k: int = TOP_K_VECTOR):
    """Create base vector retriever from ChromaDB

    Returns:
        Vector Retriever
    """

    # chroma db
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIRECTORY)
    vectordb = Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        embedding_function=embeddings,
        client=client,
    )

    # base retriever (vector retriever)
    vector_retriever = vectordb.as_retriever(
        search_kwargs={"k": top_k},
    )

    return vector_retriever


# プロンプトテンプレート
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# 実際の応答生成の例
def chat_with_bot(session_id: str):

    # LLM
    chat_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.0)

    # Vector Retriever
    retriever = vector_retriever()

    # RAG Chain
    basic_qa_chain = create_stuff_documents_chain(
        llm = chat_model,
        prompt = prompt_template,
    )
    rag_chain = create_retrieval_chain(retriever, basic_qa_chain)

    count = 0
    while True:
        print("---")
        input_message = input(f"[{count}]あなた: ")
        if input_message.lower() == "終了":
            break

        # プロンプトテンプレートに基づいて応答を生成
        response = rag_chain.invoke(
            {"input": input_message},
            config={"configurable": {"session_id": session_id}}
        )
        
        print(f"AI: {response['answer']}")
        count += 1


if __name__ == "__main__":

    # チャットセッションの開始
    session_id = "example_session"
    chat_with_bot(session_id)
```

Example 2:
```py
import os

import chromadb
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.vectorstores import Chroma
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import OpenAIEmbeddings

# OpenAI embedding model
EMBEDDING_MODEL = "text-embedding-3-small"

# ChromaDB
CHROMA_PERSIST_DIRECTORY = os.environ.get("CHROMA_PERSIST_DIRECTORY")
CHROMA_COLLECTION_NAME = os.environ.get("CHROMA_COLLECTION_NAME")

# Retriever settings
TOP_K_VECTOR = 10
DEFAULT_MAX_MESSAGES = 4

# 既存のChromaDBを読み込みVector Retrieverを作成
def vector_retriever(top_k: int = TOP_K_VECTOR):
    """Create base vector retriever from ChromaDB

    Returns:
        Vector Retriever
    """

    # chroma db
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIRECTORY)
    vectordb = Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        embedding_function=embeddings,
        client=client,
    )

    # base retriever (vector retriever)
    vector_retriever = vectordb.as_retriever(
        search_kwargs={"k": top_k},
    )

    return vector_retriever


# 会話履歴数をmax_lengthに制限するLimitedChatMessageHistoryクラス
class LimitedChatMessageHistory(ChatMessageHistory):

    # 会話履歴の保持数
    max_messages: int = DEFAULT_MAX_MESSAGES

    def __init__(self, max_messages=DEFAULT_MAX_MESSAGES):
        super().__init__()
        self.max_messages = max_messages

    def add_message(self, message):
        super().add_message(message)
        # 会話履歴数を制限
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_messages(self):
        return self.messages


# 会話履歴のストア
store = {}

# セッションIDごとの会話履歴の取得
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = LimitedChatMessageHistory()
    return store[session_id]

# プロンプトテンプレート
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

# 実際の応答生成の例
def chat_with_bot(session_id: str):

    # LLM
    chat_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.0)

    # Vector Retriever
    retriever = vector_retriever()

    # RAG Chain
    basic_qa_chain = create_stuff_documents_chain(
        llm = chat_model,
        prompt = prompt_template,
    )
    rag_chain = create_retrieval_chain(retriever, basic_qa_chain)

    # Runnable chain を RunnableWithMessageHistory でラップ
    runnable_with_history = RunnableWithMessageHistory(
        runnable=rag_chain,
        get_session_history=get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    count = 0
    while True:
        print("---")
        input_message = input(f"[{count}]あなた: ")
        if input_message.lower() == "終了":
            break

        # プロンプトテンプレートに基づいて応答を生成
        response = runnable_with_history.invoke(
            {"input": input_message},
            config={"configurable": {"session_id": session_id}}
        )
        
        print(f"AI: {response['answer']}")
        count += 1


if __name__ == "__main__":

    # チャットセッションの開始
    session_id = "example_session"
    chat_with_bot(session_id)
```

Example 3: 
```py
import os
import uuid

import chromadb
from langchain.chains import (create_history_aware_retriever,
                              create_retrieval_chain)
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.vectorstores import Chroma
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import OpenAIEmbeddings

# OpenAI embedding model
EMBEDDING_MODEL = "text-embedding-3-small"

# ChromaDB
CHROMA_PERSIST_DIRECTORY = os.environ.get("CHROMA_PERSIST_DIRECTORY")
CHROMA_COLLECTION_NAME = os.environ.get("CHROMA_COLLECTION_NAME")

# Retriever settings
TOP_K_VECTOR = 10
DEFAULT_MAX_MESSAGES = 4

# Langchain LangSmith
unique_id = uuid.uuid4().hex[0:8]
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = f"Tracing Walkthrough - {unique_id}"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"


# 既存のChromaDBを読み込みVector Retrieverを作成
def vector_retriever(top_k: int = TOP_K_VECTOR):
    """Create base vector retriever from ChromaDB

    Returns:
        Vector Retriever
    """

    # chroma db
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIRECTORY)
    vectordb = Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        embedding_function=embeddings,
        client=client,
    )

    # base retriever (vector retriever)
    vector_retriever = vectordb.as_retriever(
        search_kwargs={"k": top_k},
    )

    return vector_retriever


# 会話履歴数をmax_lengthに制限するLimitedChatMessageHistoryクラス
class LimitedChatMessageHistory(ChatMessageHistory):

    # 会話履歴の保持数
    max_messages: int = DEFAULT_MAX_MESSAGES

    def __init__(self, max_messages=DEFAULT_MAX_MESSAGES):
        super().__init__()
        self.max_messages = max_messages

    def add_message(self, message):
        super().add_message(message)
        # 会話履歴数を制限
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_messages(self):
        return self.messages


# 会話履歴のストア
store = {}

# セッションIDごとの会話履歴の取得
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = LimitedChatMessageHistory()
    return store[session_id]

# QAプロンプトテンプレート
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

# コンテキスト化QAプロンプト
"""
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)
contextualize_q_system_prompt = "チャット履歴とユーザーの質問を用いて、チャット履歴なしで理解できる独立した質問を作成してください。ユーザー質問に直接答えてはいけません。必要に応じて質問を再構成し、それ以外の場合はそのまま返してください。"
"""
contextualize_q_system_prompt = """Using the chat history and the user's question, create a standalone question that can be understood without the chat history.
formulate the question if necessary; otherwise, return it as is.
**Important!** Do not directly answer the user's question."""

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# 実際の応答生成の例
def chat_with_bot(session_id: str):


    # LLM
    #chat_model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.0)
    chat_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.0)

    # Vector Retriever
    retriever = vector_retriever()

    # History aware retriever
    history_aware_retriever = create_history_aware_retriever(
        chat_model,
        retriever,
        contextualize_q_prompt
    )

    # RAG Chain
    basic_qa_chain = create_stuff_documents_chain(
        llm = chat_model,
        prompt = qa_prompt,
    )
    rag_chain = create_retrieval_chain(history_aware_retriever, basic_qa_chain)

    # Runnable chain を RunnableWithMessageHistory でラップ
    runnable_with_history = RunnableWithMessageHistory(
        runnable=rag_chain,
        get_session_history=get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    count = 0
    while True:
        print("---")
        input_message = input(f"[{count}]あなた: ")
        if input_message.lower() == "終了":
            break

        # プロンプトテンプレートに基づいて応答を生成
        response = runnable_with_history.invoke(
            {"input": input_message},
            config={"configurable": {"session_id": session_id}}
        )
        
        print(f"AI: {response['answer']}")
        count += 1


if __name__ == "__main__":

    # チャットセッションの開始
    session_id = "example_session"
    chat_with_bot(session_id)
```

Resource:
- [rag-chatbot](https://github.com/kzhisa/rag-chatbot/blob/main/rag_chatbot3.py) 
