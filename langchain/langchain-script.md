```py
import os
import json
import re
import nltk

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import TokenTextSplitter
from langchain.vectorstores import Chroma

os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

def init():
   files = ['2022.txt']
   for file in files:
          with open("./data/{file}",'r', encoding='utf-8') as f:
               data = f.read()

          cut_data = " ".join[w for w in list(jb.cut(data))])
          cut_file = f"./data/cut/cut_{file}"
          with open(cut_file, 'w') as f:
               f.write(cut_data)

def load_documents(directory):
    loader = DirectoryLoader(directory, glob="**/*.txt")
    docs = loader.load()
    return docs

def split_documents(docs):
    text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs_texts = text_splitter.split_documents(docs)
    return docs_texts

def create_embeddings(api_key):
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    return embeddings

def create_chroma(docs_texts, embeddings, persist_directory):
    vectorstore = Chroma.from_documents(docs_texts, embeddings, persist_directory=persist_directory)
    vectorstore.persist()
    return vectorstore

def load():
    docs = load_documents('./data/cut')
    docs_texts = split_documents(docs)
    api_key = os.environ.get("OPENAI_API_KEY")
    embeddings = create_embeddings(api_key)
    vectordb = create_chroma(docs_texts, embeddings, "./data/cut/")
    llm = ChatOpenAI(temperature=0, model_name="text-davinci-003")
    chain = ConversationalRetrievalChain.from_llm(llm, vectordb.as_retriever())
    return chain

chain = load()

def get_ans(question):
    chat_history = []
    result = chain.run({
          'chat_history': chat_history,
          'question': question,
         })
    return result['answer']

if __name__ == '__main__':
   s = input('please input: ')
   while s! = 'exit':
        ans = get_ans(s)
        print(ans)
        s = input('please input: ')

```
