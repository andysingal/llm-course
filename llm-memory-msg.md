[How to manage conversation history in a ReAct Agent¶](https://langchain-ai.github.io/langgraph/how-tos/create-react-agent-manage-message-history/)

[langmem](https://www.analyticsvidhya.com/blog/2025/03/langmem-sdk/)


[memory system for AI\LLMs](https://forum.level1techs.com/t/i-made-a-memory-system-for-ai-llms/235061)


### Evaluating Very Long-Term Conversational Memory of LLM Agents
[locomo](https://github.com/snap-research/locomo)


[Five Agent Memory Types in LangGraph: A Deep Code Walkthrough](https://dev.to/sreeni5018/five-agent-memory-types-in-langgraph-a-deep-code-walkthrough-part-2-17kb)

- Memory Type 1: Short Term Memory (STM) The Conversation Buffer
- Memory Type 2: Long Term Memory(LTM) Cross Thread Persistence
- Memory Type 3: Working Memory — The Reasoning Scratchpad
- Memory Type 4: Episodic Memory — The Event Log
- Memory Type 5: Semantic Memory RetrievalAugmented Generation (RAG)

[Efficient Memory Sharing for Multi-Agent Systems via KV Cache Compaction](https://x.com/RampLabs/status/2042660310851449223)

[TencentDB-Agent-Memory](https://github.com/Tencent/TencentDB-Agent-Memory)

TencentDB Agent Memory = symbolic short-term memory + layered long-term memory.

- Symbolic short-term memory offloads heavy tool logs and condenses them into compact Mermaid symbols, cutting token usage and improving task success.
- Layered long-term memory distills fragmented conversations into structured personas and scenes, instead of flat vector piles.

[Continuous batching](https://huggingface.co/blog/sergiopaniego/cb-trl-grpo)

```
GRPOConfig(
    use_transformers_continuous_batching=True,
    transformers_continuous_batching_config={
        "use_cuda_graph": False,
        "max_memory_percent": 0.4,  # leave headroom for the backward pass
    },
)
```
