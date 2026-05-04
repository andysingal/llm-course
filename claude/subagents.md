Subagents are specialized AI assistants that handle specific types of tasks. Use one when a side task would flood your main conversation with search results, logs, or file contents you won’t reference again: the subagent does that work in its own context and returns only the summary. Define a custom subagent when you keep spawning the same kind of worker with the same instructions.

Subagents help you:
- Preserve context by keeping exploration and implementation out of your main conversation
- Enforce constraints by limiting which tools a subagent can use
- Reuse configurations across projects with user-level subagents
- Specialize behavior with focused system prompts for specific domains
- Control costs by routing tasks to faster, cheaper models like Haiku


##### Quickstart: create your first subagent

Subagents are defined in Markdown files with YAML frontmatter. You can create them manually or use the /agents command.
This walkthrough guides you through creating a user-level subagent with the /agents command. The subagent reviews code and suggests improvements for the codebase.

######## Open the subagents interface
```
/agents

```

2. Choose a location

Switch to the Library tab, select Create new agent, then choose Personal. This saves the subagent to ~/.claude/agents/ so it’s available in all your projects.

3. Generate with Claude

```
A code improvement agent that scans files and suggests improvements
for readability, performance, and best practices. It should explain
each issue, show the current code, and provide an improved version.
```

4. Select tools

For a read-only reviewer, deselect everything except Read-only tools. If you keep all tools selected, the subagent inherits all tools available to the main conversation.

5. Select model

Choose which model the subagent uses. For this example agent, select Sonnet, which balances capability and speed for analyzing code patterns.

6. Choose a color

Pick a background color for the subagent. This helps you identify which subagent is running in the UI.

7. Configure memory

Select User scope to give the subagent a persistent memory directory at ~/.claude/agent-memory/. The subagent uses this to accumulate insights across conversations, such as codebase patterns and recurring issues. Select None if you don’t want the subagent to persist learnings.

8. Save and try it out

```
Use the code-improver agent to suggest improvements in this project
```
###### Choose the subagent scope
Subagents are Markdown files with YAML frontmatter. Store them in different locations depending on scope. When multiple subagents share the same name, the higher-priority location wins.

CLI-defined subagents are passed as JSON when launching Claude Code. They exist only for that session and aren’t saved to disk, making them useful for quick testing or automation scripts. You can define multiple subagents in a single --agents call:

```
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'
```

####### Write subagent files
Subagent files use YAML frontmatter for configuration, followed by the system prompt in Markdown:

```
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

### Control subagent capabilities

You can control what subagents can do through tool access, permission modes, and conditional rules.

Subagents can use any of Claude Code’s internal tools. By default, subagents inherit all tools from the main conversation, including MCP tools.

```
---
name: safe-researcher
description: Research agent with restricted capabilities
tools: Read, Grep, Glob, Bash
---
```

#### Restrict which subagents can be spawned

When an agent runs as the main thread with claude --agent, it can spawn subagents using the Agent tool. To restrict which subagent types it can spawn, use Agent(agent_type) syntax in the tools field.

```
---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(worker, researcher), Read, Bash
---
```

If Agent is omitted from the tools list entirely, the agent cannot spawn any subagents. This restriction only applies to agents running as the main thread with claude --agent. Subagents cannot spawn other subagents, so Agent(agent_type) has no effect in subagent definitions.

#### Scope MCP servers to a subagent

Use the mcpServers field to give a subagent access to MCP servers that aren’t available in the main conversation. Inline servers defined here are connected when the subagent starts and disconnected when it finishes. String references share the parent session’s connection.

```
---
name: browser-tester
description: Tests features in a real browser using Playwright
mcpServers:
  # Inline definition: scoped to this subagent only
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  # Reference by name: reuses an already-configured server
  - github
---

Use the Playwright tools to navigate, screenshot, and interact with pages.
```

### Preload skills into subagents


