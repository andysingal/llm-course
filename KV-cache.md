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
