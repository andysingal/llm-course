[cagvault](https://github.com/letslego/cagvault)

```

┌─────────────────────────────────────────────────────────────────────────────┐
│               CACHE-AUGMENTED GENERATION (CAG) WORKFLOW                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─── SETUP PHASE (One-time) ─────────────────────────────────────────┐   │
│  │                                                                    │   │
│  │  All Documents                                                     │   │
│  │      │                                                             │   │
│  │      ▼                                                             │   │
│  │  ┌──────────────────┐                                             │   │
│  │  │  LLM Processor   │  Precompute KV-Cache                        │   │
│  │  │  (Batch Process) │  (Encodes all knowledge)                    │   │
│  │  └────────┬─────────┘                                             │   │
│  │           │                                                        │   │
│  │           ▼                                                        │   │
│  │  ┌──────────────────────┐                                         │   │
│  │  │  Cached KV-State     │  💾  Stored on Disk/Memory             │   │
│  │  │  (Ready to use)      │                                         │   │
│  │  └──────────┬───────────┘                                         │   │
│  │             │                                                     │   │
│  └─────────────┼─────────────────────────────────────────────────────┘   │
│                │                                                           │
│  ┌─── INFERENCE PHASE (Fast) ────────────────────────────────────────┐   │
│  │                                                                   │   │
│  │  User Query        Cached KV-State                               │   │
│  │      │                  │                                        │   │
│  │      └──────────┬───────┘                                        │   │
│  │                 ▼                                                │   │
│  │        ┌──────────────────────┐                                 │   │
│  │        │  LLM with Preloaded  │  ✨ NO RETRIEVAL!               │   │
│  │        │  Context + KV-Cache  │  ✨ NO LATENCY!                │   │
│  │        │                      │  ✨ GUARANTEED CONTEXT!        │   │
│  │        └──────────┬───────────┘                                 │   │
│  │                   │                                              │   │
│  │                   ▼                                              │   │
│  │              Answer (Instant)                                    │   │
│  │                                                                  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│  ┌─── MULTI-TURN OPTIMIZATION ───────────────────────────────────────┐   │
│  │                                                                   │   │
│  │  For next query: Simply truncate and reuse cached knowledge     │   │
│  │  (No need to reprocess documents)                              │   │
│  │                                                                 │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

[vLLM + LMCache: A Starter Guide, No GPU Required](https://blog.lmcache.ai/en/2026/06/23/vllm-lmcache-a-starter-guide-no-gpu-required/)

- ① What problem LMCache solves;

- ② How to set up your workspace on a MacBook;

- ③ How to run vLLM + LMCache end to end;

- ④ What to do when you run out of memory, or when the model won’t download;

- ⑤ What specifically you can work on across four directions.



