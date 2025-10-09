[What are agents](https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-llm-agents)

[How I Build an Agent with Long-Term, Personalized Memory](https://pub.towardsai.net/how-i-build-an-agent-with-long-term-personalized-memory-54b7f4272d5f)

[Mem0 with Ollama Locally](https://www.fahdmirza.com/2024/08/mem0-with-ollama-locally-memory-layer.html)

[Build low-latency voice agents powered by memory via mem0](https://docs.mem0.ai/integrations/pipecat)

[LlamaIndex ReAct Agent](https://docs.mem0.ai/examples/llama-index-mem0)

[diet_assistant_voice_cartesia](https://github.com/mem0ai/mem0/blob/main/examples/misc/diet_assistant_voice_cartesia.py)

[How to integrate Long-Term Memory for AI Agents with Mem0 and Weaviate](https://github.com/weaviate/recipes/blob/main/integrations/llm-agent-frameworks/mem0/quickstart_mem0_with_weaviate.ipynb)

```py
os.environ["MEM0_API_KEY"] = "<your-mem0-api-key>"

from llama_index.memory.mem0 import Mem0Memory

context = {"user_id": "david"}
memory_from_client = Mem0Memory.from_client(
    context=context,
    api_key=os.environ["MEM0_API_KEY"],
    search_msg_limit=4,  # optional, default is 5
)
```


[Memary](https://github.com/kingjulio8238/Memary)

<img width="930" alt="Screenshot 2024-08-06 at 12 52 04 PM" src="https://github.com/user-attachments/assets/d8f4dc02-54c2-4395-8864-49fb23522d51">

## Code Repos
[memobase](https://github.com/memodb-io/memobase)
Memobase is a user profile-based memory system designed to bring long-term user memory to your Generative AI (GenAI) applications. Whether you're building virtual companions, educational tools, or personalized assistants, Memobase empowers your AI to remember, understand, and evolve with your users.

[memo-aws](https://docs.mem0.ai/examples/aws_example)



## Resources

[Agentic-LongTerm-Memory](https://github.com/Farzad-R/Agentic-LongTerm-Memory)

![default_behavior](https://github.com/user-attachments/assets/86f06134-2c47-467c-8109-65dd95e90c94)


## Articles
[Memory: The secret sauce of AI agents](https://decodingml.substack.com/p/memory-the-secret-sauce-of-ai-agents)

[PdfToMem](https://github.com/alinvdu/PdfToMem)

Turn PDFs into structured, queryable memory—built for LLMs.

Large Language Models struggle with memory. PdfToMem makes it effortless.
By combining reasoning-powered ingestion, structured retrieval, and a multi-agent architecture, it transforms unstructured PDFs into rich memory representations.

[Integrating Long-Term Memory with Gemini 2.5](https://www.philschmid.de/gemini-with-memory)
