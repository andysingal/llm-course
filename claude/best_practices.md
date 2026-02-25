[claude-code](https://github.com/shanraisshan/claude-code-best-practice)

[claude-code_1](https://github.com/shanraisshan/claude-code-best-practice)

When you run claude in a directory, Claude Code gains access to:
- Your project. Files in your directory and subdirectories, plus files elsewhere with your permission.
- Your terminal. Any command you could run: build tools, git, package managers, system utilities, scripts. If you can do it from the command line, Claude can too.
- Your git state. Current branch, uncommitted changes, and recent commit history.
- Your CLAUDE.md. A markdown file where you store project-specific instructions, conventions, and context that Claude should know every session.
- Extensions you configure. MCP servers for external services, skills for workflows, subagents for delegated work, and Claude in Chrome for browser interaction.

Claude Code saves your conversation locally as you work. Each message, tool use, and result is stored, which enables rewinding, resuming, and forking sessions. Before Claude makes code changes, it also snapshots the affected files so you can revert if needed. Claude can persist learnings across sessions using auto memory, and you can add your own persistent instructions in CLAUDE.md.

Since sessions are tied to directories, you can run parallel Claude sessions by using git worktrees, which create separate directories for individual branches.

When you resume a session with claude --continue or claude --resume, you pick up where you left off using the same session ID. New messages append to the existing conversation. Your full conversation history is restored, but session-scoped permissions are not. You’ll need to re-approve those.

#### The context window
Claude’s context window holds your conversation history, file contents, command outputs, CLAUDE.md, loaded skills, and system instructions. As you work, context fills up. Claude compacts automatically, but instructions from early in the conversation can get lost


To control what’s preserved during compaction, add a “Compact Instructions” section to CLAUDE.md or run ```/compact``` with a focus (like ```/compact``` focus on the API changes).

#### Manage context with skills and subagents

- Skills load on demand. Claude sees skill descriptions at session start, but the full content only loads when a skill is used. For skills you invoke manually, set ```disable-model-invocation: true``` to keep descriptions out of context until you need them.
- Subagents get their own fresh context, completely separate from your main conversation. Their work doesn’t bloat your context. When done, they return a summary. This isolation is why subagents help with long sessions.

### Control what Claude can do
Press Shift+Tab to cycle through permission modes:
- Default: Claude asks before file edits and shell commands
- Auto-accept edits: Claude edits files without asking, still asks for commands
- Plan mode: Claude uses read-only tools only, creating a plan you can approve before execution
- You can also allow specific commands in ```.claude/settings.json``` so Claude doesn’t ask each time. This is useful for trusted commands like ```npm test``` or ```git status```. Settings can be scoped from organization-wide policies down to personal preferences.

Built-in commands also guide you through setup:
- ```/init``` walks you through creating a CLAUDE.md for your project
- ```/agents``` helps you configure custom subagents
- ```/doctor``` diagnoses common issues with your installation

#### Extensions
Extensions plug into different parts of the agentic loop:
- CLAUDE.md adds persistent context Claude sees every session
- Skills add reusable knowledge and invocable workflows
- MCP connects Claude to external services and tools
- Subagents run their own loops in isolated context, returning summaries
- Agent teams coordinate multiple independent sessions with shared tasks and peer-to-peer messaging
- Hooks run outside the loop entirely as deterministic scripts
- Plugins and marketplaces package and distribute these features

##### Common workflows

Step-by-step guides for exploring codebases, fixing bugs, refactoring, testing, and other everyday tasks with Claude Code.



```
Claude Code: "npm add ..."

You: "Use pnpm, you idiot!"

*adds it to CLAUDE​.md*

Claude: "npm add ..."

There's a better way:
```

Life hack, put empty strings for "commit" and "pr" in attribution settings for Claude Code and it will stop doing that growth hacker thing where it lists itself on all your commits
<img width="1034" height="693" alt="Screenshot 2026-02-25 at 7 02 00 AM" src="https://github.com/user-attachments/assets/2271dd6b-6839-418d-8bf8-94b98ea8c8f0" />

