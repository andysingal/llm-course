[Running Multiple Claude Code Sessions in Parallel with git worktree](https://dev.to/datadeer/part-2-running-multiple-claude-code-sessions-in-parallel-with-git-worktree-165i)

```
How to use git worktree?
I navigate to my project folder.
cd /Users/lucca/Godot/mobsters

I create a separate project version with git worktree.
git worktree add ../mobsters-worktree/find-my-mobster -b feat/find-my-mobster

I create a separate terminal tab where I navigate to the new worktree folder.
cd ./../mobsters-worktree/find-my-mobster

I can now start a Claude Code session in the first and second tab and work on separate features. (running claude)

Once I'm done, I commit my changes to my repo and navigate back to my main worktree (/Users/lucca/Godot/mobsters) to remove the linked worktree with git worktree remove ../mobsters-worktree/find-my-mobster

To find your main worktree, use git worktree list
```
- To control what’s preserved during compaction, add a “Compact Instructions” section to CLAUDE.md or run /compact with a focus (like /compact focus on the API changes).
- Run /context to see what’s using space. MCP servers add tool definitions to every request, so a few servers can consume significant context before you start working. Run /mcp to check per-server costs.

### Manage context with skills and subagents
- Beyond compaction, you can use other features to control what loads into context.
- Skills load on demand. Claude sees skill descriptions at session start, but the full content only loads when a skill is used. For skills you invoke manually, set disable-model-invocation: true to keep descriptions out of context until you need them.
- Subagents get their own fresh context, completely separate from your main conversation. Their work doesn’t bloat your context. When done, they return a summary. This isolation is why subagents help with long sessions.


#### Control what Claude can do
Press Shift+Tab to cycle through permission modes:
Default: Claude asks before file edits and shell commands
Auto-accept edits: Claude edits files without asking, still asks for commands
Plan mode: Claude uses read-only tools only, creating a plan you can approve before execution
Delegate mode: Claude coordinates work through agent teammates only, with no direct implementation. Only available when an agent team is active.

You can also allow specific commands in [```.claude/settings.json```](https://code.claude.com/docs/en/settings) so Claude doesn’t ask each time. This is useful for trusted commands like npm test or git status. Settings can be scoped from organization-wide policies down to personal preferences. See Permissions for details.  

```
{
  "env": {
      "CLAUDE_CODE_USE_BEDROCK": "1",
      "AWS_REGION": "east",
      "ANTHROPIC_MODEL":
      "ANTHROPIC_SMALL_FAST_MODEL":"",
      "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "",
      "MAX_THINKING_TOKENS": "1024"
}
}
```

#### Ask Claude Code for help
Claude Code can teach you how to use it. Ask questions like “how do I set up hooks?” or “what’s the best way to structure my CLAUDE.md?” and Claude will explain.
Built-in commands also guide you through setup:
- [```/init```](https://kau.sh/blog/build-ai-init-command/) walks you through creating a [CLAUDE.md](https://code.claude.com/docs/en/best-practices) for your project
- ```/agents``` helps you configure custom subagents
- ```/doctor``` diagnoses common issues with your installation

