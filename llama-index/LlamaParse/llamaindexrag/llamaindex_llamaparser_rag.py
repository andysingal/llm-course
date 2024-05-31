from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.llms.azure_openai import AzureOpenAI

from llama_parse import LlamaParse
import os
from dotenv import load_dotenv

from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import MarkdownElementNodeParser


load_dotenv(override=True)  # take environment variables from .env.

# Variables not used here do not need to be updated in your .env file
openai_model_deployment_name = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
openai_model_model_name = os.environ["AZURE_OPENAI_MODEL_NAME"]
openai_model_version = os.environ["AZURE_OPENAI_API_VERSION"]
endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
index_name = os.environ["AZURE_SEARCH_INDEX"]
azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
azure_openai_key = os.environ["AZURE_OPENAI_KEY"] if len(os.environ["AZURE_OPENAI_KEY"]) > 0 else None
azure_openai_embedding_deployment = os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"]
os.environ["OPENAI_API_KEY"] = "sk-proj-fqVX8Cxuo8wdwBghya39T3BlbkFJuE4QuNPXlXfx1Eflh9TU"

parsing_instruction="""

"""

parser = LlamaParse(
    api_key="llx-o5jHmmF9CbTqkVns0OTBM0lOlowORfXca2LI9taFHK7WpWVg",  # can also be set in your env as LLAMA_CLOUD_API_KEY
    result_type="markdown",  # "markdown" and "text" are available
    verbose=True,
    parsing_instruction=parsing_instruction    
)

documents = parser.load_data(["./medicalrecords/medicalrecords.pdf"])

llm = AzureOpenAI(
    model=openai_model_model_name,
    deployment_name=openai_model_deployment_name,
    api_key=azure_openai_key,
    azure_endpoint=azure_openai_endpoint,
    api_version=openai_model_version,
)

embed_model = AzureOpenAIEmbedding(
    model="text-embedding-ada-002",
    deployment_name="textembeddingmodel",
    api_key=azure_openai_key,
    azure_endpoint=azure_openai_endpoint,
    api_version=openai_model_version,
)


node_parser = MarkdownElementNodeParser(llm=llm, num_workers=8)
nodes = node_parser.get_nodes_from_documents(documents=[documents[0]])
base_nodes, objects = node_parser.get_nodes_and_objects(nodes)


recursive_index = VectorStoreIndex(nodes=base_nodes+objects)
# recursive_index.storage_context.persist("vectorstorage")

query_engine = recursive_index.as_query_engine(similarity_top_k=25)
query1 = """
This document contains medical record in each page of the document. 
List the history of Present Illness from the medical prescription in sentences.
List the medications in bullet points the patient has been taking from the medical prescription.
List the blood test values that are high and low from all the blood test reports.
If the document contains a table that describes a blood test value, do not output it as a table, but as a sentence providing that value.
"""

response1 = query_engine.query(query1)

print(response1)

