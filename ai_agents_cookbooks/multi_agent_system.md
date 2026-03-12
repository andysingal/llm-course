 We’re about to introduce a more powerful architecture: the dual RAG MAS. It uses Retrieval-Augmented Generation (RAG) in two ways. The first is what you’d expect—retrieving facts from a knowledge base. But the second is new: retrieving procedural instructions, instructions to implement procedural (or dynamic) RAG. This addition changes the game. Now, the system can learn not only what to say but also how to say it, switching style and structure on demand.

  The first focuses on data ingestion, where we’ll create a knowledge base for facts and a context library for semantic blueprints. The second brings everything to life in runtime execution, showing how agents retrieve and combine both kinds of context in real time.

  Context-aware systems are technologies that sense their physical or digital environment—including location, time, user identity, and activity—to adapt their behavior and proactively provide relevant information or services.

  <img width="438" height="321" alt="Screenshot 2026-03-12 at 3 53 32 PM" src="https://github.com/user-attachments/assets/a175dabc-940d-47d7-9796-2e8dafc64661" />

  Phase 1 is data preparation, which prepares the data. Phase 2 is runtime execution, where our MAS uses the prepared data to respond to a user goal.

  - Knowledge data: Factual information that the system should know
  - Context data: Structured instructions, or semantic blueprints

  Both data types are processed by the embedding model. For knowledge data, we split the text into chunks and embed each chunk. For context data or semantic blueprints, we embed only the description of the blueprint’s intent

  All embeddings are stored in a Pinecone vector database, which will hold everything the system needs. We use a single Pinecone index, divided into two strictly separated namespaces:

- KnowledgeStore: This namespace stores the vectors from the factual data
- ContextLibrary: This namespace stores the vectors from the procedural blueprints


### Phase 2: Runtime execution analysis

The process begins with a user goal, a high-level instruction submitted by the user—for example, Write a suspenseful story about Apollo 11.

The Orchestrator receives this goal. Acting as the system’s central coordinator, it analyzes the request and identifies two components:

- intent_query: This is the intent of the Librarian query and relates to the desired style or structure (in our example, suspenseful story)
- topic_query: This is the topic of the Researcher query and relates to the subject matter (in our example, Apollo 11)


  The Orchestrator then delegates each query to a specialist agent:

- The Librarian agent, responsible for retrieving instruction scripts, receives the intent_query through the engine’s MCP messaging layer. It queries the ContextLibrary namespace, performs a semantic search to find the blueprint description that best matches the requested intent, and retrieves the corresponding semantic blueprint.
- The Researcher agent, responsible for retrieving factual information, receives the topic_query. It queries the KnowledgeStore namespace, retrieves the relevant factual chunks, and synthesizes them into concise findings.

Once both responses are ready, the Orchestrator can now facilitate the delivery of the retrieved instructions script and the synthesized facts to the Writer agent. The arrows in Figure above show the blueprint and facts moving from the Librarian and Researcher toward the Writer.



