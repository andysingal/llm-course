import os

from llama_index import ServiceContext, set_global_service_context
from llama_index.llms import OpenAI
from llama_index.query_engine.router_query_engine import RouterQueryEngine
from indexing import get_query_engine_tool

# setup a global service context
llm = OpenAI(model="gpt-3.5-turbo-16k", temperature=0, max_tokens=512)
# embed_model = OpenAIEmbedding(embed_batch_size=50)
embed_model = "local:BAAI/bge-base-en"  # use a local model for embeddings

service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
set_global_service_context(service_context)


docs_directories = {
    "../docs/community": "Useful for information on community integrations with other libraries, vector dbs, and frameworks.", 
    "../docs/core_modules/agent_modules": "Useful for information on data agents and tools for data agents.", 
    "../docs/core_modules/data_modules": "Useful for information on data, storage, indexing, and data processing modules.",
    "../docs/core_modules/model_modules": "Useful for information on LLMs, embedding models, and prompts.",
    "../docs/core_modules/query_modules": "Useful for information on various query engines and retrievers, and anything related to querying data.",
    "../docs/core_modules/supporting_modules": "Useful for information on supporting modules, like callbacks, evaluators, and other supporting modules.",
    "../docs/getting_started": "Useful for information on getting started with LlamaIndex.", 
    "../docs/development": "Useful for information on contributing to LlamaIndex development.",
}

# Build query engine tools
query_engine_tools = [
    get_query_engine_tool(directory, description) for directory, description in docs_directories.items()
]


query_engine = RouterQueryEngine.from_defaults(
    query_engine_tools=query_engine_tools,
    select_multi=True,
    service_context=service_context,
)

while True:
    input_text = input("Enter a query: ").strip()
    input_text += "\nInclude relevant links from the context when it makes sense."
    response = query_engine.query(input_text)
    print(str(response))
    print("\n")
