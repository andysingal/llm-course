[Integrating AI Search into your Zoom Workplace](https://weaviate.io/blog/zooviate-zoom-and-weaviate)

[RAG-App-weaviate](https://www.freecodecamp.org/news/how-to-build-a-rag-pipeline-with-llamaindex/)

[What is Agentic RAG](https://weaviate.io/blog/what-is-agentic-rag)

[Game-recommender](https://github.com/weaviate/recipes/blob/main/weaviate-features/generative-search/generative_search_ollama/deepseek-ollama-epic-games-rag.ipynb)

[personalization-agent](https://colab.research.google.com/github/weaviate/recipes/blob/main/weaviate-services/agents/personalization-agent-get-started-recipes.ipynb#scrollTo=QUe7QF2nQJoL)

[Rotaional-quantization](https://weaviate.io/blog/weaviate-1-32-release?utm_source=blogs&utm_medium=w_social&utm_campaign=1.32_release&utm_content=diagram_post_268085932)

***[Elysia](https://weaviate.io/blog/elysia-agentic-rag?utm_source=channels&utm_medium=w_social&utm_campaign=elysia&utm_content=blog_annoucement_680931809)
 Elysia – our open-source, agentic RAG framework that represents a fundamental rethink of how we interact with our data through AI.

[reason_moderncolbert](https://github.com/weaviate/recipes/blob/main/weaviate-features/multi-vector/reason_moderncolbert.ipynb)
Multi-vector embeddings with Reasoning-ModernColBERT

<img width="494" alt="Screenshot 2024-08-22 at 10 39 01 PM" src="https://github.com/user-attachments/assets/b9063e75-1224-4126-a087-11bc7f725110">


### Evaluation Metrics
[Evals and Guardrails in Enterprise workflows](https://weaviate.io/blog/evals-guardrails-enterprise-workflows-1?utm_source=linkedin&utm_medium=w_social&utm_campaign=blog_post&utm_content=blog_annoucement_268065838)

1. Pre-Model Guardrails
This is the first layer of defence to catch bad inputs early — this reduces wasted compute and ensures policy compliance from the start. These are hard constraints applied before the input reaches the model. Think of them as a security checkpoint that blocks inappropriate or dangerous requests upfront.

Examples: A pre-filter for PII (personally identifiable information), content moderation checks, or blocking specific keywords.

2. Post-Model Guardrails
The second layer of defence which acts as a safety net — sanitising, constraining, or rejecting unsafe or non-compliant outputs. These are hard constraints applied after the model has generated a response but before it's sent back to the user. This catches anything the model might have generated that violates safety or quality standards.

Examples: PII redaction from the model's output, checking for factuality against a knowledge base, or ensuring the response meets a specific formatting requirement.

3. Evals
The feedback mechanism. Evals are used to assess the quality of the model's output. They don’t just measure; they trigger active feedback loops to correct agents in real-time. They are the key to dynamic self-correction and shaping behaviour. Evals can be automated (e.g., a test suite) or involve human feedback.

4. Traces
The "breadcrumbs" of the entire process. A trace captures the complete journey of a request—from the initial input, through the agent and model calls, to the final output. They let you inspect reasoning chains, measure latency, and refine agent orchestration. Traces are essential for debugging, understanding how a system is performing, and feeding data back into the evals.


Research paper:

[Late Interaction Retrieval Models: ColBERT, ColPali, and ColQwen](https://weaviate.io/blog/late-interaction-overview?utm_source=linkedin&utm_medium=dw_social&utm_campaign=dev_education&utm_content=diagram_post_680658140)

[37 Things I Learned About Information Retrieval in Two Years at a Vector Database Company](https://www.leoniemonigatti.com/blog/what_i_learned.html)
