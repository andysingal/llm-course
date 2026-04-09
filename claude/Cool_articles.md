[How I Dropped Our Production Database and Now Pay 10% More for AWS](https://alexeyondata.substack.com/p/how-i-dropped-our-production-database)

-  let Claude Code run terraform plan and then terraform apply
-  Analyzing and Deleting Duplicate Resources through AWS CLI
-  The agent kept deleting files, and at some point, it output: “I cannot do it. I will do a terraform destroy. Since the resources were created through Terraform, destroying them through Terraform would be cleaner and simpler than through AWS CLI

[How to Run Local LLMs with Claude Code](https://unsloth.ai/docs/basics/claude-code)

This step-by-step guide shows you how to connect open LLMs and APIs to Claude Code entirely locally, complete with screenshots. Run using any open model like Qwen3.5, DeepSeek and Gemma.

[I read Claude Code’s memory source code. This one limit silently deletes your agent’s memory](https://x.com/mem0ai/status/2039041449854124229)

[Anatomy of an AI Agent. Know your Score!](https://doneyli.substack.com/p/anatomy-of-an-ai-agent-know-your)

In my system, memory operates on four levels:

- Global memory (~/.claude/CLAUDE.md): Rules that apply everywhere. My communication style, port assignments, workflow conventions. Every agent inherits this.

- Project memory (project/CLAUDE.md): Context specific to one codebase. The content system knows about newsletter formats. The advisory practice knows about pricing tiers.

- Session memory (~/.claude/projects/*/memory/): What the agent learned during our last conversation. Corrections I made. Decisions we reached.

- Conversation memory: Ephemeral context within a single interaction.

