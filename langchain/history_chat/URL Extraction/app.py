
import os, openai
import warnings
warnings.filterwarnings("ignore")
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

#provide key
open_ai_key = ""
if open_ai_key == '':
    try:
        open_ai_key = os.environ['OPENAI_API_KEY']
    except:
        pass
openai.api_key = open_ai_key
os.environ['OPENAI_API_KEY'] = open_ai_key


def main(url_path, prompt):
    bs_strainer = bs4.SoupStrainer(class_=("post-content", "post-title", "post-header"))
    loader = WebBaseLoader(
        web_paths=(url_path,),
        bs_kwargs={"parse_only": bs_strainer},
    )
    docs = loader.load()
    
    # Index documents into search engine
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    
    llm = ChatOpenAI(
        model="gpt-4", temperature=0,
    )
    # RAG Chain
    retriever = vectorstore.as_retriever()
    chain = RetrievalQA.from_llm(llm=llm,
                                    retriever=retriever)
    response = chain.invoke(prompt)
    print("Assistant: ", response['result'])
    print()


if __name__ == '__main__':
    while True:
        prompt = str(input("User: "))
        main(os.path.join('https://lilianweng.github.io/posts/2023-06-23-agent/'), prompt)
    