```py
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI

from src.constants import (
    NEO4J_PASSWORD,
    NEO4J_URI,
    NEO4J_USERNAME,
)


graph = Neo4jGraph(
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD,
)
llm = ChatOpenAI(temperature=0, model="gpt-4o")
llm_transformer = LLMGraphTransformer(llm=llm)
graph_documents = llm_transformer.convert_to_graph_documents(texts)
graph.add_graph_documents(graph_documents)
```
