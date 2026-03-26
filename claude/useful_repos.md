[Claude-Code-Usage-Monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor)

A beautiful real-time terminal monitoring tool for Claude AI token usage with advanced analytics, machine learning-based predictions, and Rich UI. Track your token consumption, burn rate, cost analysis, and get intelligent predictions about session limits.

[claude-code-templates](https://github.com/davila7/claude-code-templates)
A comprehensive collection of AI agents, custom commands, settings, hooks, external integrations (MCPs), and project templates to enhance your development workflow.

[Everything Claude Code](https://github.com/affaan-m/everything-claude-code)

The complete collection of Claude Code configs from an Anthropic hackathon winner.

Production-ready agents, skills, hooks, commands, rules, and MCP configurations evolved over 10+ months of intensive daily use building real products.

[claude-howto](https://github.com/luongnv89/claude-howto)

Go from typing claude to orchestrating agents, hooks, skills, and MCP servers — with visual tutorials, copy-paste templates, and a guided learning path.

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


[agent-view](https://github.com/Frayo44/agent-view)

<img width="702" height="698" alt="Screenshot 2026-03-07 at 2 34 11 PM" src="https://github.com/user-attachments/assets/78b5fc8a-049e-4cee-9b3e-b0a162ab5267" />


[claude_statusline](https://github.com/kamranahmedse/claude-statusline)
Configure your Claude Code statusline to show limits, directory and git info


[claude-code-settings](https://github.com/feiskyer/claude-code-settings)
A curated collection of Claude Code settings, skills and sub-agents designed for enhanced development workflows. This setup includes specialized skills and subagents for feature development (spec-driven workflow), code analysis, GitHub integration, and knowledge management.

[codex-skills](https://github.com/aniketpanjwani/skills/tree/main)
A set of reusable skills for Codex and Claude Code.

[claude-code-workflow](https://github.com/runesleo/claude-code-workflow)

A battle-tested workflow template for Claude Code — memory management, context engineering, and task routing from 3 months of daily usage across multiple projects.

[agency-agents](https://github.com/msitarzewski/agency-agents)

A complete AI agency at your fingertips - From frontend wizards to Reddit community ninjas, from whimsy injectors to reality checkers. Each agent is a specialized expert with personality, processes, and proven deliverables.


#### Articles
[How To Be A World-Class Agentic Engineer](https://x.com/systematicls/status/2028814227004395561)

