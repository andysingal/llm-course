[CLAUDE.md Masterclass: From Start to Pro-Level User with Hooks & Subagents](https://newsletter.claudecodemasterclass.com/p/claudemd-masterclass-from-start-to)

<img width="536" height="435" alt="Screenshot 2026-02-28 at 2 14 01 AM" src="https://github.com/user-attachments/assets/df7de75d-bab3-417e-b691-006fcea6cdbc" />

<h2>Why Claude Will Ignore Your CLAUDE.md</h2>h2>
Claude Code wraps your CLAUDE.md with a system reminder that tells Claude to ignore irrelevant content.

The actual wrapper looks like this:

```
<system-reminder>
  IMPORTANT: this context may or may not be relevant to your tasks. 
  You should not respond to this context unless it is highly relevant to your task.
</system-reminder>
```
Think of CLAUDE.md as three things:

- Project Memory — Claude remembers your setup across sessions

- Operational Boundaries — Rules Claude won’t break

- Context Primer — Claude starts informed, not blank

When you understand this mental model, you stop treating CLAUDE.md like a README since it’s the best leverage configuration point you have in Claude Code.


<h2>CLAUDE.md Hierarchy System</h2>
<img width="543" height="584" alt="Screenshot 2026-02-28 at 2 19 48 AM" src="https://github.com/user-attachments/assets/d08d1a62-6101-44eb-a207-ae9b1e1bb28e" />



<img width="790" height="395" alt="Screenshot 2026-02-28 at 2 20 58 AM" src="https://github.com/user-attachments/assets/46781b57-778b-415b-926a-bbba3267b05a" />

```
my-monorepo/
├── CLAUDE.md                    # Monorepo-wide rules
├── apps/
│   ├── web/
│   │   └── CLAUDE.md            # Frontend-specific rules
│   └── api/
│       └── CLAUDE.md            # Backend-specific rules
├── packages/
│   └── shared/
│       └── CLAUDE.md            # Shared library rules
└── tests/
    └── CLAUDE.md                # Testing conventions
```

<h2>Anatomy of a Great CLAUDE.md</h2>
A well-structured CLAUDE.md answers three questions for Claude:

- WHAT — The tech stack, project structure, key files

- WHY — The purpose of the project, what each part does

- HOW — Commands to run, workflows to follow, conventions to respect


<h3>Core Sections</h3>

```
# Project Context

Brief description of what this project is and your working philosophy.

## About This Project

Tech stack, architecture pattern, key dependencies.

## Key Directories

- `src/` — Source code
- `tests/` — Test files
- `docs/` — Documentation

## Commands

```bash
npm run dev      # Start development server
npm run test     # Run tests
npm run build    # Production build
```

-------CONTINUED----------



```
Start with /init to get a baseline, then refine manually. Use # to add instructions as you discover new ideas, and keep this in mind: the best CLAUDE.md files are built iteratively.
```

<h2>Advanced CLAUDE.md Patterns</h2>

<h3>Pattern 1: Index Files for Large Codebases</h3>
For large or unfamiliar codebases, create index files that help Claude navigate efficiently.

Step 1: Generate a general index:
```
# general_index.md

## /src/api/
- `auth.py` — Authentication endpoints, JWT handling
- `users.py` — User CRUD operations
- `products.py` — Product catalog endpoints

## /src/models/
- `user.py` — User model, relationships to orders
- `product.py` — Product model, inventory tracking

## /src/utils/
- `validators.py` — Input validation helpers
- `formatters.py` — Response formatting utilities
```

Step 2: Reference it in CLAUDE.md

```
## Navigation

I have provided index files to help you navigate:

- `general_index.md` — File descriptions for each module
- `detailed_index.md` — Function signatures and docstrings

These indexes may or may not be up to date. Verify by checking 
the actual files when needed.
```
Pattern 2: Modular CLAUDE.md Design
Break your CLAUDE.md into clear sections with markdown headers. This prevents instruction bleeding between different functional areas.
```
# CLAUDE.md

## Development Commands
<!-- Build, test, run instructions -->

## Code Standards  
<!-- Conventions that apply everywhere -->

## Workflow Procedures
<!-- How to complete common tasks -->

## File Boundaries
<!-- What Claude can and cannot modify -->

## Tool Integration
<!-- MCP servers, custom commands -->
```
Pattern 3: Workflow Definitions
Define step-by-step workflows for complex tasks.

This prevents Claude from jumping straight into code without planning.
```
## Workflows

### Adding a New API Endpoint

1. Check if similar endpoint exists in `src/api/`
2. Create schema in `src/schemas/` if new data types needed
3. Implement endpoint in appropriate router file
4. Add tests in `tests/api/`
5. Update API documentation
6. Run full test suite before committing

### Database Schema Changes

1. Describe the change and why it's needed
2. Create migration: `alembic revision --autogenerate -m "description"`
3. Review generated migration file
4. Test migration: `alembic upgrade head`
5. Test rollback: `alembic downgrade -1`
6. Update relevant models and schemas
```
Pattern 4: Context Swapping
For projects with distinct phases (development vs. deployment, frontend vs. backend), maintain multiple CLAUDE.md variants:

```
project/
├── CLAUDE.md                 # Active configuration
├── .claude/
│   ├── CLAUDE.development.md # Development focus
│   ├── CLAUDE.deployment.md  # Deployment focus
│   └── CLAUDE.debugging.md   # Debugging focus
```
<h3>Pattern 5: Conditional Instructions</h3>
Tell Claude to behave differently based on what it’s working on:

```
## Conditional Rules

When working in `src/api/`:
- All endpoints must have OpenAPI documentation
- Use dependency injection for database sessions
- Return appropriate HTTP status codes

When working in `tests/`:
- Use fixtures from `conftest.py`
- Mock external services, never call them
- Each test file mirrors the source file structure

When working in `scripts/`:
- Scripts must be idempotent (safe to run multiple times)
- Include --dry-run option for destructive operations
- Log all actions for debugging
```
Pattern 6: MCP Server Documentation
If you use MCP servers, document them in CLAUDE.md so Claude knows when and how to use them:
```
## MCP Integrations

### Slack MCP
- Posts to #dev-notifications channel only
- Use for deployment notifications and build failures
- Do not use for individual PR updates
- Rate limited to 10 messages per hour

### Database MCP
- Read-only access to production replica
- Use for data exploration, never for writes
- Prefer this over raw SQL when possible
```

<h2>CLAUDE.md + Hooks & Subagents</h2>
CLAUDE.md becomes more powerful when combined with other Claude Code features. Here’s a preview of how they work together.

<h3>CLAUDE.md + Hooks</h3>h3>
Hooks are automated actions that run at specific points in Claude’s workflow. Your CLAUDE.md can reference and coordinate with them.
<img width="709" height="319" alt="Screenshot 2026-02-28 at 2 52 08 AM" src="https://github.com/user-attachments/assets/ea6032f2-aeb7-4d2f-8a29-3b9a9f156979" />

Instead of asking Claude to check formatting (slow, expensive), set up a hook:
```
## Standards

Code must pass linting before commit. 
A pre-commit hook runs `npm run lint` automatically.
Do not manually check formatting — the hook handles it.
```


<h2>CLAUDE.md + Subagents</h2>h2>
Subagents are isolated Claude instances that handle specific tasks. They have their own context window, preventing information from one task from polluting another.


<img width="579" height="418" alt="Screenshot 2026-02-28 at 2 55 03 AM" src="https://github.com/user-attachments/assets/e89cb933-0703-497d-8201-887b976b542e" />

Your CLAUDE.md helps subagents understand the project quickly without needing the full conversation history.

```
## Subagent Guidelines

When delegating tasks to subagents:
- Security reviews: Use fresh subagent, don't carry implementation context
- Code exploration: Subagent should read general_index.md first
- Documentation: Subagent can access docs/ freely
```
CLAUDE.md alone is powerful. Combined with hooks and subagents, it becomes a complete automation system:

- CLAUDE.md defines the rules

- Hooks enforce them automatically

- Subagents handle specialized tasks with a clean context
