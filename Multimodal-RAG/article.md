[ChatPDF](https://dev.to/sharathkurup/engineering-rag-systems-that-actually-work-conversational-retrieval-page-awareness-debugging-52bm)

[repo](https://github.com/SharathKurup/chatPDF)

[Using LLM Councils for Multi-Agent Research Evaluation](https://www.swarm-ai.org/blog/llm-councils-for-multi-agent-evaluation/)

```
┌─────────────────────────────────────────────────────────┐
│                    StudyEvaluator                        │
│  Wraps Council with 3 expert personas + prompt formats  │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                      Council                            │
│              3-stage deliberation engine                 │
│                                                         │
│  Stage 1: Collect ──► Stage 2: Rank ──► Stage 3: Synth  │
└─────────────────────────────────────────────────────────┘
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
          LLMAgent   LLMAgent   LLMAgent
          (any provider per member)
```
