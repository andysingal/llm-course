[HASH](https://github.com/hashintel/hash)

HASH is a self-building, open-source database which grows, structures and checks itself. HASH integrates data in (near-)realtime, and provides a powerful set of interfaces so that information can be understood and used in any context. Intelligent, autonomous agents can be deployed to grow, check, and maintain the database, integrating and structuring information from the public internet as well as your own connected private source

[RuVector](https://github.com/ruvnet/RuVector)

The self-learning, self-optimizing vector database — with graph intelligence, local AI, and PostgreSQL built in.

RuVector is fundamentally different. It watches how you use it and gets smarter: search results improve automatically, the system tunes itself to your workload, and it runs AI models right on your hardware — no cloud APIs, no per-query bills, GPUs optional, CPUs preferred. It drops into PostgreSQL, runs in browsers, and ships as a single file.

```
User Query → [SONA Engine] → Model Response → User Feedback
                  ↑                                 │
                  └─────── Learning Signal ─────────┘
                         (< 1ms adaptation)
```

[OpenViking](https://github.com/volcengine/OpenViking)

OpenViking is an open-source Context Database designed specifically for AI Agents.

We aim to define a minimalist context interaction paradigm for Agents, allowing developers to completely say goodbye to the hassle of context management. OpenViking abandons the fragmented vector storage model of traditional RAG and innovatively adopts a "file system paradigm" to unify the structured organization of memories, resources, and skills needed by Agents.

With OpenViking, developers can build an Agent's brain just like managing local files:

- Filesystem Management Paradigm → Solves Fragmentation: Unified context management of memories, resources, and skills based on a filesystem paradigm.
- Tiered Context Loading → Reduces Token Consumption: L0/L1/L2 three-tier structure, loaded on demand, significantly saving costs.
- Directory Recursive Retrieval → Improves Retrieval Effect: Supports native filesystem retrieval methods, combining directory positioning with semantic search to achieve recursive and precise context acquisition.
- Visualized Retrieval Trajectory → Observable Context: Supports visualization of directory retrieval trajectories, allowing users to clearly observe the root cause of issues and guide retrieval logic optimization.
- Automatic Session Management → Context Self-Iteration: Automatically compresses content, resource references, tool calls, etc., in conversations, extracting long-term memory, making the Agent smarter with use.
