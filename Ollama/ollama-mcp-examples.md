```py
# Install dependencies and run AI agent with LangChain + MCP + RAG + Ollama/OpenAI
!pip install -q langchain langchain-community langchain-core langchain-ollama faiss-cpu exa-py firecrawl fastapi uvicorn aiohttp nest-asyncio python-dotenv

import os, nest_asyncio, asyncio
from typing import List
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from exa_py import Exa

nest_asyncio.apply()

# ===== ENVIRONMENT VARIABLES (INSERT YOUR KEYS HERE) =====
os.environ["EXA_API_KEY"] = "YOUR_EXA_KEY"
os.environ["FIRECRAWL_API_KEY"] = "YOUR_FIRECRAWL_KEY"
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_KEY"

# Initialize the Exa search engine
exa = Exa(api_key=os.environ["EXA_API_KEY"])

# ===== FUNCTIONS =====

# Web search using Exa API
async def search_web(query: str, num_results: int = 5):
    print(f"🔍 Searching: {query}")
    search_results = exa.search_and_contents(
        query,
        summary={"query": "Main summary"},
        num_results=num_results
    )
    urls = [r.url for r in search_results.results if hasattr(r, 'url')]
    return search_results.results, urls

# Web scraping with FireCrawl
async def get_web_content(url: str) -> List[Document]:
    try:
        loader = FireCrawlLoader(url=url, mode="scrape")
        docs = await asyncio.wait_for(loader.aload(), timeout=15)
        return docs
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return [Document(page_content=f"Error: {e}", metadata={"source": url})]

# Create vector database using RAG
async def create_rag(urls: list[str]):
    documents = []
    tasks = [get_web_content(url) for url in urls]
    results = await asyncio.gather(*tasks)
    for r in results:
        documents.extend(r)

    splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=500)
    split_docs = splitter.split_documents(documents)

    try:
        embeddings = OllamaEmbeddings(model="mistral-embed")
    except:
        print("⚠️ Ollama unavailable. Falling back to OpenAI.")
        embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])

    return FAISS.from_documents(split_docs, embedding=embeddings)

# Vector search in the RAG database
async def search_rag(query: str, vectorstore: FAISS):
    return vectorstore.similarity_search(query, k=3)

# Run the full agent
async def agente(query="What’s new with Mistral AI?"):
    print(f"\n🚀 Running agent for: {query}")
    raw_results, urls = await search_web(query)
    if not urls:
        return print("No results found.")

    store = await create_rag(urls)
    response = await search_rag(query, store)

    print("\n✅ Relevant results:\n")
    for i, doc in enumerate(response, 1):
        print(f"{i}️⃣ {doc.page_content[:800]}...\n")

# 🔥 Direct call to the agent
await agente("What’s new in LangChain and MCP?")

```
