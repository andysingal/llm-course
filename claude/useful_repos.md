[Claude-Code-Usage-Monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor)

A beautiful real-time terminal monitoring tool for Claude AI token usage with advanced analytics, machine learning-based predictions, and Rich UI. Track your token consumption, burn rate, cost analysis, and get intelligent predictions about session limits.

[Everything Claude Code](https://github.com/affaan-m/everything-claude-code)

The complete collection of Claude Code configs from an Anthropic hackathon winner.

Production-ready agents, skills, hooks, commands, rules, and MCP configurations evolved over 10+ months of intensive daily use building real products.

[recall](https://github.com/arjunkmrm/recall)

Ever lost a conversation session with Claude Code or Codex and wish you could resume it? This skill lets Claude and your agents search across all your past conversations with full-text search. Builds a SQLite FTS5 index over ~/.claude/projects/ and ~/.codex/sessions/ with BM25 ranking, Porter stemming, and incremental updates.

```py
npx skills add arjunkmrm/recall
```

```py
 ~/.claude/projects/**/*.jsonl ──┐
                                  ├─▶ Index ──▶ ~/.recall.db (SQLite FTS5)
  ~/.codex/sessions/**/*.jsonl ──-┘      │
                                         │  incremental (mtime-based)
                                         │
  Query ──▶ FTS5 Match ──▶ BM25 rank ──▶ Recency boost ──▶ Results
                │                    [half-life: 30 days]
                │  [Porter stemming
                │   phrase/boolean/prefix]
                ▼
         snippet extraction
         highlighted excerpts
```

[agency-agents](https://github.com/msitarzewski/agency-agents)

A complete AI agency at your fingertips - From frontend wizards to Reddit community ninjas, from whimsy injectors to reality checkers. Each agent is a specialized expert with personality, processes, and proven deliverables.
