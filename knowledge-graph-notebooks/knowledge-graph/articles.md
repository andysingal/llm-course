[graphiti](github.com/getzep/graphiti)

[Pydantic fixed my Agent's Memory](https://x.com/akshay_pachaar/status/2058976178908885210)

<img width="540" height="284" alt="Screenshot 2026-05-26 at 7 19 49 PM" src="https://github.com/user-attachments/assets/f7434e97-d298-457e-8ddc-f1639cfbc223" />

```
from zep_cloud.external_clients.ontology import EntityModel, EntityText
from pydantic import Field

class Project(EntityModel):
    """
    Represents a specific software project, application, 
    or codebase that the user is building or contributing to.
    """

    project_status: EntityText = Field(
        description="Current status: active, completed, paused, or archived.",
    )
    project_type: EntityText = Field(
        description="Type of project: web app, mobile app, API, CLI tool, etc.",
    )
```

Zep (Temporal Knowledge Graph for Agents)

Zep is purpose-built as a long-term memory layer for LLM-based agents. It automatically ingests, structures, and synthesizes unstructured chat and structured business data into a queryable temporal knowledge graph.Core Technology: Built on the open-source Graphiti framework, often backed by graph databases like Neo4j.Temporal Awareness: It natively tracks how facts change over time using a bi-temporal model (storing both when an event occurred and when it was recorded), allowing AI agents to understand what is true now versus what was true then.Use Cases: AI chatbots, personal assistants, CRM memory, and conversational state.Pros: Extracts and summarizes entities automatically; hybrid search (semantic + graph); explicitly designed to solve AI amnesia
