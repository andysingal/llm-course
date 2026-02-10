[StrandsAgents + Claude](https://acro-engineer.hatenablog.com/entry/2025/08/28/120000)

[Writing effective tools for agents — with agents](https://www.anthropic.com/engineering/writing-tools-for-agents)

[ragmail](https://github.com/0xfe/ragmail)
RAGmail lets you search and analyze your email with your favourite agent (OpenCode, Claude, Codex, etc.)

It consists of a comprehensive ingestion pipeline to build a semantically-indexed local database of your email, along with an agent skill (ragmail) that you can use to ask questions.

Typical questions you can answer:

- "What did we decide about the school trip budget?"
- "Tell me how my communication style has changed over time, with examples."
- "Where all did I travel to in 2006?"
- "Explore my relationship with Alice and write me a doc on how it progressed, start to finish."
- "How many times did Bob email me in February 2026?"

[claude-flow](https://github.com/ruvnet/claude-flow)
Claude-Flow is a comprehensive AI agent orchestration framework that transforms Claude Code into a powerful multi-agent development platform. It enables teams to deploy, coordinate, and optimize specialized AI agents working together on complex software engineering tasks.
<img width="646" height="671" alt="Screenshot 2026-01-16 at 2 54 40 PM" src="https://github.com/user-attachments/assets/5269c081-dbbc-487d-8cac-c2580a78d632" />

[everything-claude-code](https://github.com/affaan-m/everything-claude-code)
The complete collection of Claude Code configs from an Anthropic hackathon winner.

Production-ready agents, skills, hooks, commands, rules, and MCP configurations evolved over 10+ months of intensive daily use building real products.


[Claude-superbase](https://www.aitmpl.com/component/skill/supabase-postgres-best-practices)
```
---
name: supabase-postgres-best-practices
description: Postgres performance optimization and best practices from Supabase. Use this skill when writing, reviewing, or optimizing Postgres queries, schema designs, or database configurations.
license: MIT
metadata:
  author: supabase
  version: "1.0.0"
---

# Supabase Postgres Best Practices

Comprehensive performance optimization guide for Postgres, maintained by Supabase. Contains rules across 8 categories, prioritized by impact to guide automated query optimization and schema design.

## When to Apply

Reference these guidelines when:
- Writing SQL queries or designing schemas
- Implementing indexes or query optimization
- Reviewing database performance issues
- Configuring connection pooling or scaling
- Optimizing for Postgres-specific features
- Working with Row-Level Security (RLS)

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Query Performance | CRITICAL | `query-` |
| 2 | Connection Management | CRITICAL | `conn-` |
| 3 | Security & RLS | CRITICAL | `security-` |
| 4 | Schema Design | HIGH | `schema-` |
| 5 | Concurrency & Locking | MEDIUM-HIGH | `lock-` |
| 6 | Data Access Patterns | MEDIUM | `data-` |
| 7 | Monitoring & Diagnostics | LOW-MEDIUM | `monitor-` |
| 8 | Advanced Features | LOW | `advanced-` |

## How to Use

Read individual rule files for detailed explanations and SQL examples:

```
rules/query-missing-indexes.md
rules/schema-partial-indexes.md
rules/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect SQL example with explanation
- Correct SQL example with explanation
- Optional EXPLAIN output or metrics
- Additional context and references
- Supabase-specific notes (when applicable)

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
```





```py
import asyncio
import os
from textwrap import dedent

from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.tools.mcp import MCPClient

TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

websearch = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command='npx',
            args=['-y', 'tavily-mcp@latest'],
            env={'TAVILY_API_KEY': TAVILY_API_KEY},
        )
    )
)

class DeepResearch:
    PROMPT = dedent("""\
    ユーザーから伝えられた調査したいトピックに対して、PDF換算で3枚分の詳細かつ広範なレポートを作成してください。
    レポートはMarkdown形式でフォーマットしてください。
    必ず日本語でレポートを書いてください

    レポートする内容はWeb検索を用いて収集してください。
    収集した内容をよく吟味し、さらに徹底的な調査が必要だと判断した内容は、検索文言を書き換えてさらにWeb検索を行ってください。
    ユーザーが指示したトピックについて包括的な情報を収集することが重要です。

    参照したサイト脚注で示し、脚注には `[脚注番号][タイトル](URL)` 形式で列挙してください。
    """)

    def __init__(self, tools):
        model = BedrockModel(
            model='us.anthropic.claude-sonnet-4-20250514-v1:0',
            streaming=True,
            additional_request_fields={
                'thinking': {'type': 'enabled', 'budget_tokens': 4000},
                'anthropic_beta': ['interleaved-thinking-2025-05-14'],
            },
        )
        self.agent = Agent(
            model=model,
            system_prompt=self.PROMPT,
            tools=tools,
        )

    async def stream(self, prompt):
        async for event in self.agent.stream_async(prompt):
            if text := event.get('event', {}).get('contentBlockDelta', {}).get('delta', {}).get('text', ''):
                yield text
            for content in event.get('message', {}).get('content', []):
                if isinstance(content, dict) and (tool_use := content.get('toolUse', '')):
                    print(tool_use)
```

![image-2012487322726748160](https://github.com/user-attachments/assets/af65ef5c-6f97-4143-9a7f-1f8843f4e4a2)



## Article
[We got Claude to teach open models how to write CUDA kernels!](https://huggingface.co/blog/upskill)
```
install upskill
pip install upskill

or use uvx 
uvx upskill --help

generate a skill based on an agent trace
upskill generate "write nvidia kernels" --from ./trace.md
evaluate models on a skill
upskill eval ./skills/my-skill/ --model haiku --model sonnet

generate skills for local models
upskill generate "parse YAML" 
    --model opus 
    --eval-model "unsloth/GLM-4.7-Flash-GGUF:Q4_0" 
    --eval-base-url http://localhost:8080/v1

```
<img width="507" height="633" alt="Screenshot 2026-02-04 at 6 49 09 PM" src="https://github.com/user-attachments/assets/be218305-1029-4e2c-9780-459c72d9d8d2" />

[Councils of agents](https://theengineeringmanager.substack.com/p/councils-of-agents)
