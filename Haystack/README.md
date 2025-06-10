HayStack
Haystack is a Python-based framework developed by deepset, a startup founded in 2018 in Berlin by Milos Rusic, Malte Pietsch, Timo Möller. Deepset provides developers with the tools to build Natural Language Processing (NLP)-based application, and with the introduction of Haystack they are making it to the next level.Haystack has the following core components:

1. Nodes. These are components that perform a specific task or function, such as a retriever, a reader, a generator, a summarizer, etc. Nodes can be LLMs or other utilities that interact with LLMs or other resources. Among LLMs, Haystack supports proprietary models, such as those available in OpenAI and Azure OpenAI, and open-source models consumable from the Hugging Face Hub.
2. Pipelines. These are sequences of calls to nodes that perform natural language tasks or interact with other resources. Pipelines can be querying pipelines or indexing pipelines, depending on whether they perform searches on a set of documents or prepare documents for search. Pipelines are predetermined and hardcoded, meaning that they do not change or adapt based on the user input or the context.
3. Agent. This is an entity that uses LLMs to generate accurate responses to complex queries. An agent has access to a set of tools, which can be pipelines or nodes, and it can decide which tool to call based on the user input and the context. An agent is dynamic and adaptive, meaning that it can change or adjust its actions based on the situation or the goal.
4. Tools. There are functions that an agent can call to perform natural language tasks or interact with other resources. Tools can be pipelines or nodes that are available to the agent and they can be grouped into toolkits, which are sets of tools that can accomplish specific objectives.
DocumentStores. Those are backends that store and retrieve documents for search. DocumentStores can be based on different technologies, also including VectorDB (such as FAISS, Milvus, or Elasticsearch).


[Creating a Multi-Agent System with Haystack](https://haystack.deepset.ai/tutorials/45_creating_a_multi_agent_system)

