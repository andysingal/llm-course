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

### Automate and scale
Once you’re effective with one Claude, multiply your output with parallel sessions, headless mode, and fan-out patterns.
Everything so far assumes one human, one Claude, and one conversation. But Claude Code scales horizontally. The techniques in this section show how you can get more done.
​
Run headless mode
Use ```claude -p "prompt"``` in CI, pre-commit hooks, or scripts. Add --output-format stream-json for streaming JSON output.
With ```claude -p "your prompt"```, you can run Claude headlessly, without an interactive session. Headless mode is how you integrate Claude into CI pipelines, pre-commit hooks, or any automated workflow. The output formats (plain text, JSON, streaming JSON) let you parse results programmatically.

```
# One-off queries
claude -p "Explain what this project does"

# Structured output for scripts
claude -p "List all API endpoints" --output-format json

# Streaming for real-time processing
claude -p "Analyze this log file" --output-format stream-json
```

### Fan out across files
For large migrations or analyses, you can distribute work across many parallel Claude invocations:
1. <strong>Generate a task list</strong>: Have Claude list all files that need migrating (e.g., list all 2,000 Python files that need migrating)
2.Write a script to loop through the list
```
for file in $(cat files.txt); do
  claude -p "Migrate $file from React to Vue. Return OK or FAIL." \
    --allowedTools "Edit,Bash(git commit *)"
done
```
3. <strong>Test on a few files, then run at scale</strong>: Refine your prompt based on what goes wrong with the first 2-3 files, then run on the full set. The ```--allowedTools``` flag restricts what Claude can do, which matters when you’re running unattended.

### I find it helpful to have claude ring the terminal bell when something needs my attention.
 
Here is a prompt that sets that up.

```
  Please set up a bell notification system for our session. When long operations complete (builds, tests, large file operations) or when major milestones are achieved, ring my terminal
   bell to notify me.

  Technical requirements:
  1. In SSH sessions, write directly to $SSH_TTY device file (not stdout)
  2. Use this pattern that works from non-TTY contexts:
     python3 -c "import os; f=open(os.getenv('SSH_TTY'), 'w'); f.write('\a'*3); f.flush(); f.close()"
  3. Create a helper script at ~/.local/bin/bell for easy reuse

  Please:
  1. Create the bell helper script
  2. Test it to confirm it works in my terminal
  3. Remember to use it throughout our session for notifications

  Ring the bell when:
  - Long operations complete (builds, tests, deployments, large syncs)
  - Major milestones achieved (phase completions, significant checkpoints)
  - Errors need my attention
  - Tasks I'm waiting on finish

  After setup, ring the bell 3 times to confirm it's working.
```

PRO Tips with Claude Code:

The "deny" list overrides `bypassPermissions`

So you can basically enable bypassPermissions and then deny every command you're afraid AI can do

Simple and safe

<img width="379" height="321" alt="Screenshot 2026-02-11 at 6 22 52 PM" src="https://github.com/user-attachments/assets/0c3cdbe5-55c4-4c5c-8b2a-56142335a789" />

