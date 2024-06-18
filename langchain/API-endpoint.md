## How to implement RAG with AI Endpoints (and LangChain)

```py
How to implement RAG with AI Endpoints (and LangChain)
Be sure to have the correct dependencies in your requirements.txt:

langchain
langchain-mistralai
langchain_community
langchain_chroma
argparse
unstructured
langchainhub
pip3 install -r requirements.txt
Then you can develop your chatbot with RAG feature:

import argparse
import time

from langchain import hub

from langchain_mistralai import ChatMistralAI

from langchain_chroma import Chroma

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings.ovhcloud import OVHCloudEmbeddings

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_text_splitters import RecursiveCharacterTextSplitter

# Function in charge to call the LLM model.
# Question parameter is the user's question.
# The function print the LLM answer.
def chat_completion(new_message: str):
  # no need to use a token
  model = ChatMistralAI(model="Mixtral-8x22B-Instruct-v0.1", 
                        api_key="foo",
                        endpoint='https://mixtral-8x22b-instruct-v01.endpoints.kepler.ai.cloud.ovh.net/api/openai_compat/v1', 
                        max_tokens=1500, 
                        streaming=True)

  # Load documents from a local directory
  loader = DirectoryLoader(
     glob="**/*",
     path="./rag-files/",
     show_progress=True
  )
  docs = loader.load()

  # Split documents into chunks and vectorize them
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
  splits = text_splitter.split_documents(docs)
  vectorstore = Chroma.from_documents(documents=splits, embedding=OVHCloudEmbeddings(model_name="multilingual-e5-base"))

  prompt = hub.pull("rlm/rag-prompt")

  rag_chain = (
    {"context": vectorstore.as_retriever(), "question": RunnablePassthrough()}
    | prompt
    | model
  )

  print("🤖: ")
  for r in rag_chain.stream({"question", new_message}):
    print(r.content, end="", flush=True)
    time.sleep(0.150)

# Main entrypoint
def main():
  # User input
  parser = argparse.ArgumentParser()
  parser.add_argument('--question', type=str, default="What is the meaning of life?")
  args = parser.parse_args()
  chat_completion(args.question)

if __name__ == '__main__':
    main()

```

```py
python3 chat-bot-streaming-rag.py --question "What is AI Endpoints?"
```
