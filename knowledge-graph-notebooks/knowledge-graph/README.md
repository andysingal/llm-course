[trustgraph](https://github.com/trustgraph-ai/trustgraph)

[PolarDB-langchain](https://developer.aliyun.com/article/1611770)

[Semantica](https://github.com/Hawksight-AI/semantica)

```
import semantica
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

# Build an agent with structured context
context = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=ContextGraph(advanced_analytics=True),
    decision_tracking=True,
    kg_algorithms=True,
)

# Store memory
memory_id = context.store(
    "GPT-4 outperforms GPT-3.5 on reasoning benchmarks by 40%",
    conversation_id="research_session_1",
)

# Record a decision with full context
decision_id = context.record_decision(
    category="model_selection",
    scenario="Choose LLM for production reasoning pipeline",
    reasoning="GPT-4 benchmark advantage justifies 3x cost increase",
    outcome="selected_gpt4",
    confidence=0.91,
    entities=["gpt4", "gpt35", "reasoning_pipeline"],
)

# Find similar decisions from history
precedents = context.find_precedents("model selection reasoning", limit=5)

# Analyze downstream influence of this decision
influence = context.analyze_decision_influence(decision_id)
```

[embabel-agent-rag-graph](https://github.com/embabel/embabel-agent-rag-graph)

RAG (Retrieval-Augmented Generation) implementation for graph databases using Drivine, part of the Embabel Agent framework.

Overview
This module provides a graph-database-backed implementation of the RAG pattern using Drivine4j. It supports Neo4j, FalkorDB, and Memgraph through a dialect abstraction that handles the Cypher differences between engines.

Key Components
- DrivineStore: Content element repository for storing and retrieving documents, chunks, and embeddings
- RagDialect: Strategy interface for database-specific operations (index creation, vector search, fulltext search, embedding storage)
- CypherSearch / DrivineCypherSearch: Cypher query execution layer
- LogicalQueryResolver: Resolves logical query names to Cypher query files
- Mappers: Row mappers for converting query results to domain objects

Transform Chaos into Intelligence. Build AI systems with context graphs, decision tracking, and advanced knowledge engineering that are explainable, traceable, and trustworthy — not black boxes.
