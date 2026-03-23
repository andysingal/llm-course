[Anatomy of the .claude/ folder](https://x.com/akshay_pachaar/status/2035341800739877091)

- The rules/ folder: modular instructions that scale'
- The commands/ folder: your custom slash commands
- The skills/ folder: reusable workflows on demand
- /.claude/agents/-- Subagents
settings.json: permissions and project config
```md
your-project/
├── CLAUDE.md                  # Team instructions (committed)
├── CLAUDE.local.md            # Your personal overrides (gitignored)
│
└── .claude/
    ├── settings.json          # Permissions + config (committed)
    ├── settings.local.json    # Personal permission overrides (gitignored)
    │
    ├── commands/              # Custom slash commands
    │   ├── review.md          # → /project:review
    │   ├── fix-issue.md       # → /project:fix-issue
    │   └── deploy.md          # → /project:deploy
    │
    ├── rules/                 # Modular instruction files
    │   ├── code-style.md
    │   ├── testing.md
    │   └── api-conventions.md
    │
    ├── skills/                # Auto-invoked workflows
    │   ├── security-review/
    │   │   └── SKILL.md
    │   └── deploy/
    │       └── SKILL.md
    │
    └── agents/                # Specialized subagent personas
        ├── code-reviewer.md
        └── security-auditor.md

~/.claude/
├── CLAUDE.md                  # Your global instructions
├── settings.json              # Your global settings
├── commands/                  # Your personal commands (all projects)
├── skills/                    # Your personal skills (all projects)
├── agents/                    # Your personal agents (all projects)
└── projects/                  # Session history + auto-memory
```

#### A practical setup to get started
If you're starting from scratch, here's a progression that works well.
- Step 1. Run /init inside Claude Code. It generates a starter CLAUDE.md by reading your project. Edit it down to the essentials.
- Step 2. Add .claude/settings.json with allow/deny rules appropriate for your stack. At minimum, allow your run commands and deny .env reads.
- Step 3. Create one or two commands for the workflows you do most. Code review and issue fixing are good starting points.
- Step 4. As your project grows and your CLAUDE.md gets crowded, start splitting instructions into .claude/rules/ files. Scope them by path where it makes sense.
- Step 5. Add a ~/.claude/CLAUDE.md with your personal preferences. This might be something like "always write types before implementations" or "prefer functional patterns over class-based."
That's genuinely all you need for 95% of projects. Skills and agents come in when you have recurring complex workflows worth packaging up.
