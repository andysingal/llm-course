[Claude-Code-Usage-Monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor)

A beautiful real-time terminal monitoring tool for Claude AI token usage with advanced analytics, machine learning-based predictions, and Rich UI. Track your token consumption, burn rate, cost analysis, and get intelligent predictions about session limits.

[claude-code-templates](https://github.com/davila7/claude-code-templates)
A comprehensive collection of AI agents, custom commands, settings, hooks, external integrations (MCPs), and project templates to enhance your development workflow.

[Everything Claude Code](https://github.com/affaan-m/everything-claude-code)

The complete collection of Claude Code configs from an Anthropic hackathon winner.

Production-ready agents, skills, hooks, commands, rules, and MCP configurations evolved over 10+ months of intensive daily use building real products.

[claude-howto](https://github.com/luongnv89/claude-howto)

Go from typing claude to orchestrating agents, hooks, skills, and MCP servers — with visual tutorials, copy-paste templates, and a guided learning path.

[claude-token-efficient](https://github.com/drona23/claude-token-efficient)

One file. Drop it in your project. Keeps responses terse and can reduce total tokens on output-heavy workflows. Note: instruction files add input tokens on every turn. Keep this file short - if it grows too much, it can cost more than it saves. Model support: benchmarks were run on Claude only. The rules are model-agnostic and should work on any model that reads context - but results on local models like llama.cpp, Mistral, or others are untested. Community results welcome.

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

[drawio-skill](https://github.com/Agents365-ai/drawio-skill)

- Generates .drawio XML files from natural language descriptions
- Exports diagrams to PNG, SVG, PDF, or JPG using the native draw.io desktop CLI
- 6 diagram type presets: ERD, UML Class, Sequence, Architecture, ML/Deep Learning, Flowchart — with preset shapes, styles, and layout conventions
- Animated connectors (flowAnimation=1) for data-flow and pipeline diagrams (visible in SVG and draw.io desktop)
- ML model diagram support with tensor shape annotations (B, C, H, W) — ideal for NeurIPS/ICML/ICLR papers
- Grid-aligned layout — all coordinates snap to 10px multiples for clean alignment
- Browser fallback — generates diagrams.net URLs when the desktop CLI is unavailable
- Iterative design: preview, get feedback, and refine diagrams until they look right
- Auto-launch draw.io desktop after export for manual fine-tuning
- Triggers automatically when diagrams would help explain complex systems
- Style presets (v1.3 new) — teach the skill your visual style from a .drawio file or image, save it by name, and apply it to future diagrams. See ## Style Presets in SKILL.md.
- Custom output directory (v1.4 new) — ask for any output path (e.g. ./artifacts/, docs/images/) and the skill will mkdir -p and export there; ideal for CI/CD artifact pipelines.

<img width="877" height="650" alt="Screenshot 2026-05-02 at 11 21 28 AM" src="https://github.com/user-attachments/assets/985a08b3-e191-4925-8ae5-4edebe97ac54" />





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

[code-review-graph](https://github.com/tirth8205/code-review-graph)


- 1. [Supabase CLI](https://github.com/supabase/cli)

- 2. [Skill Creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)

- 3. [Get Sh*t Done](https://github.com/gsd-build/get-shit-done)

- 4. [NotebookLM (Python)](https://github.com/teng-lin/notebooklm-py)

- 5. [Obsidian](https://github.com/obsidianmd)

- 6. [Continue](https://github.com/continuedev/continue)

- 7. [Open Interpreter](https://github.com/OpenInterpreter/open-interpreter)

- 8. [Flowise](https://github.com/FlowiseAI/Flowise)

- 9. [Boltdotnew (clone)](https://github.com/stackblitz/bolt.new) 

- 10. [Awesome Claude Code](https://github.com/hesreallyhim/awesome-claude-code)

- 11. [Prompt Engineering Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)  



[rtk](https://github.com/rtk-ai/rtk)

rtk filters and compresses command outputs before they reach your LLM context. Single Rust binary, 100+ supported commands, <10ms overhead



AI coding tools re-read your entire codebase on every task. code-review-graph fixes that. It builds a structural map of your code with Tree-sitter, tracks changes incrementally, and gives your AI assistant precise context via MCP so it reads only what matters.

[RAPTOR](https://github.com/gadievron/raptor)

RAPTOR is an autonomous offensive/defensive security research framework, based on Claude Code. It empowers security research with agentic workflows and automation.

RAPTOR stands for Recursive Autonomous Penetration Testing and Observation Robot. (We really wanted to name it RAPTOR)

RAPTOR autonomously:

- Code Understanding: Adversarial code comprehension — map attack surface, trace data flows, hunt for vulnerability variants
- Scans your code with Semgrep and CodeQL and tries dataflow validation
- Fuzzes your binaries with American Fuzzy Lop (AFL)
- Analyses vulnerabilities using advanced LLM reasoning
- Exploits by generating proof-of-concepts
- Patches with code to fix vulnerabilities
- FFmpeg-specific patching for Google's recent disclosure (https://news.ycombinator.com/item?id=45891016)
- OSS Forensics for evidence-backed GitHub repository investigations
- Agentic Skills Engine for security research & operations (SecOpsAgentKit)
- Offensive Security Testing via autonomous specialist agent with SecOpsAgentKit
- Cost Management with budget enforcement, real-time tracking, and quota detection
- Reports everything in structured formats

[Bright Data Plugin for Claude Code](https://github.com/brightdata/skills)

Instead of raw HTML that the agent has to parse, Bright Data provides pre-built extractors for 40+ platforms (Amazon, LinkedIn, Instagram, TikTok, YouTube, Reddit) that return clean JSON with specific fields like product prices, review scores, profile data, and post content.

<img width="634" height="684" alt="Screenshot 2026-05-04 at 10 28 51 AM" src="https://github.com/user-attachments/assets/496dcad1-8931-43ee-9750-c95699c228a6" />

InsForge

InsForge (open-source, Apache 2.0) acts as the backend context engineering layer for agents using Skills and CLI.
<img width="547" height="276" alt="Screenshot 2026-05-04 at 10 56 40 AM" src="https://github.com/user-attachments/assets/2d5837d5-3e28-4105-a4d7-34389e541c4f" />

```
npx skills add insforge/insforge-skills
```


<img width="974" height="742" alt="Screenshot 2026-05-04 at 10 55 15 AM" src="https://github.com/user-attachments/assets/ae1d6168-2e39-43a1-95e6-c647e21d49a3" />

[Claude Code Has Two Big Blind Spots. I Fixed Both](https://x.com/akshay_pachaar/status/2051291922409603238)


[open-slide](https://github.com/1weiho/open-slide)

The slide framework built for agents. Describe your deck in natural language — your coding agent writes the React. open-slide handles the canvas, scaling, navigation, hot reload, and present mode so the agent can focus on content.

Every slide renders into a fixed 1920 × 1080 canvas. Pages are arbitrary React components, not a constrained DSL.

<img width="627" height="319" alt="Screenshot 2026-05-04 at 12 22 18 PM" src="https://github.com/user-attachments/assets/3b961646-7927-4d82-9613-c0e1e1c11cc2" />



#### Articles
[How To Be A World-Class Agentic Engineer](https://x.com/systematicls/status/2028814227004395561)

