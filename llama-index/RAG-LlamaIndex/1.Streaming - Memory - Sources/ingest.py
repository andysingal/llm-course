import os
import openai
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

documents = SimpleDirectoryReader("./data").load_data(show_progress=True)
index = VectorStoreIndex.from_documents(documents)
index.storage_context.persist()
