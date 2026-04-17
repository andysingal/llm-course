Hooks are user-defined event handlers that run shell commands or scripts at specific points in Claude Code's lifecycle. Think of them as automated triggers - they fire when particular events occur, regardless of what the AI "decides" to do.

Every hook configuration consists of three components:

- Event: The lifecycle moment when the hook fires (SessionStart, PreToolUse, PostToolUse, Notification, Stop, and others)
- Matcher: An optional regex filter that narrows when the hook runs - for example, matching only "Bash" tool calls or only "Edit|Write" operations
- Action: What actually happens - usually a shell command, but can also be a prompt sent to a lightweight Claude model for evaluation



[claude-code-hooks](https://github.com/karanb192/claude-code-hooks)

Ready-to-use hooks for Claude Code — safety, automation, notifications, and more.

Hooks live in JSON configuration files. You have several options for where to place them:

- User-wide: ~/.claude/settings.json applies hooks to all your Claude Code projects
- Project-specific: .claude/settings.json in your repo root (shareable via version control)
- Local overrides: .claude/settings.local.json for personal tweaks that shouldn't be committed
- Managed policies: Organization-level hooks for enterprise environments

```
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
``` [source](https://blog.promptlayer.com/understanding-claude-code-hooks-documentation/)



