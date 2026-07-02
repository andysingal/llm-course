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

<strong>Prefix Caching</strong>: Prefix caching (or prompt caching) is an AI inference technique that stores and reuses the Key-Value (KV) cache of recurring prompt segments. By bypassing the resource-heavy "prefill" phase for the shared prefix, it dramatically cuts processing time, lowers API costs, and accelerates the Time to First Token (TTFT)

How it Works: 
1. The Prefill Phase: When an AI model processes a prompt, it creates a KV cache—a map of how tokens relate to each other.
2. Caching: If your prompt shares an identical starting sequence (like a long system instruction or document) with a previous request, the system retrieves the precomputed KV cache.
3. Continuation: The model skips reading the identical prefix and begins processing instantly from the unique, dynamic suffix

[Automatic Prefix Caching](https://docs.vllm.ai/en/stable/design/prefix_caching/)

The core idea is simple – we cache the kv-cache blocks of processed requests, and reuse these blocks when a new request comes in with the same prefix as previous requests.

While there are many ways to implement prefix caching, vLLM chooses a hash-based approach.

```
messages = [
    {"role": "user",
     "content": [
         {"type": "text",
          "text": "What's in this image?"
         },
         {"type": "image_url",
          "image_url": {"url": image_url},
         },
    ]},
]
```
Cache Isolation for Security To improve privacy in shared environments, vLLM supports isolating prefix cache reuse through optional per-request salting. By including a cache_salt in the request, this value is injected into the hash of the first block, ensuring that only requests with the same salt can reuse cached KV blocks. This prevents timing-based attacks where an adversary could infer cached content by observing latency differences. This offers protection without compromising performance.




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

#### Article

[Integrating Memory into AI Agents](https://amanxai.com/2026/06/24/integrating-memory-into-ai-agents/)

