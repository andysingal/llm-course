[Technology Research - LangGraph](https://zenn.dev/suwash/articles/lang_graph_20251110)

LangGraph has the following key features for realizing complex agent systems:

- Loopable
Graphs - Construct graphs with loops, and define autonomous retries and corrective actions.
- State Persistence
Saving and restoring execution state. Continue execution after server restarts and track history.
- Human-in-the-loop
: Pause and human intervention at any node for pre-execution checks and quality control.
- Comprehensive Memory Management -
Shared state management across the entire graph, enabling short-term and long-term memory.
- Streaming
Get intermediate results in real time. View your thought process as it happens.
- Advanced Debugging and Observability
: Integration with LangSmith. Visually trace execution paths and state transitions.
- Time Travel:
Rewinding a state to a specific step in the past.
These features work together to give agents more control and reliability. Human-in-the-loop requires pausing. Persistence is essential for safe pausing. Persisted history makes time travel possible.
