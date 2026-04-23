[LocalForge](https://github.com/al1-nasir/LocalForge)

Self-Hosted AI Control Plane for Intelligent Local LLM Orchestration

A production-grade platform for running, routing, benchmarking, and finetuning local LLMs.
Drop-in OpenAI-compatible API · Intelligent multi-model routing · LoRA finetuning with live monitoring.

```
┌────────────────────────────────────────────────────────────────────┐
│                        Next.js Frontend                            │
│   Dashboard · Models · Benchmarks · Traces · Memory · Finetune     │
└────────────────────────────┬───────────────────────────────────────┘
                             │ REST + SSE
┌────────────────────────────▼───────────────────────────────────────┐
│                       FastAPI Backend                               │
│  ┌──────────┐ ┌─────────┐ ┌──────────┐ ┌────────┐ ┌────────────┐  │
│  │  Router   │ │Lifecycle│ │Inference │ │ Memory │ │  Finetune   │  │
│  │  Engine   │ │ Manager │ │  Engine  │ │ Layer  │ │  Engine     │  │
│  └────┬─────┘ └────┬────┘ └────┬─────┘ └───┬────┘ └─────┬──────┘  │
│       │             │           │            │            │         │
│  ┌────▼─────┐  ┌────▼────┐ ┌───▼────┐ ┌────▼────┐ ┌─────▼──────┐  │
│  │Classifier│  │ SQLite  │ │ llama  │ │ Qdrant  │ │  Training  │  │
│  │(TF-IDF)  │  │  (WAL)  │ │ .cpp   │ │(Vector) │ │  Worker    │  │
│  └──────────┘  └─────────┘ │ server │ └─────────┘ │ (Subprocess│  │
│                             └────────┘             │  PEFT/TRL) │  │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  └────────────┘  │
│  │Benchmark │  │   Auth   │  │   RAG Layer      │                  │
│  │ Fetcher  │  │ (Bearer) │  │ (LlamaIndex +    │                  │
│  └──────────┘  └──────────┘  │  Qdrant)         │                  │
│                              └──────────────────┘                  │
└────────────────────────────────────────────────────────────────────┘
```

