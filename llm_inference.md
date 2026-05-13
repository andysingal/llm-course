[Superlinked Inference Engine](https://github.com/superlinked/sie)

SIE is an open-source inference engine that serves embeddings, reranking, and entity extraction through a single unified API. It replaces the patchwork of separate model servers with one system that handles 85+ models across dense, sparse, multi-vector, vision, and cross-encoder architectures.

Three functions (encode, score, extract) cover the entire embedding, reranking, and extraction pipeline
- 85+ pre-configured models, hot-swappable, all quality-verified against MTEB in CI
- Serves multiple models simultaneously with on-demand loading and LRU eviction
- Ships the full production stack: load-balancing gateway, KEDA autoscaling, Grafana dashboards, Terraform for GKE/EKS
- Integrates with LangChain, LlamaIndex, Haystack, DSPy, CrewAI, Chroma, Qdrant, and Weaviate
- OpenAI-compatible /v1/embeddings endpoint for drop-in migration
