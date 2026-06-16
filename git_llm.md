[git_worktree](https://x.com/ai_edisonZ/status/2066528346754957464)

Git Worktree is becoming the standard for multi-agent programming workflows.

It's not some new technology, but rather a long-standing feature in Git. It was only in the era of AI Coding that everyone rediscovered just how practical it is.

If multiple Agents share a single directory: Agent A writes login code, Agent B switches branches to fix a bug, Agent C runs a git add . command, and the scene quickly descends into chaos.
The role of git worktree is simple: Share the same Git repository while giving each Agent an independent workspace.

Its principle is actually quite straightforward:
A single Git repository can have multiple independent working directories at the same time.
For example:
- projects/
├── shop/           # main
├── shop-login/     # feature/login
└── shop-payment/   # fix/payment

These three directories share the same Git commit history and branch system, but each has its own independent files, staging area, uncommitted changes, and current branch.

Creating a workspace is also straightforward:
> git worktree add ../shop-login -b feature/login main

When first created, the code in shop/ and shop-login/ is essentially identical. But afterward, any modifications and commits you make in shop-login/ will only advance feature/login and won't automatically affect main.

Once development is complete, you need to manually merge:
> cd ../shop
> git merge feature/login

After confirming everything is fine, delete the workspace and branch:
> git worktree remove ../shop-login
> git branch -d feature/login

The difference from re-cloning a repository is: Clone creates a completely independent set of Git data, while Worktree shares the original repository's history and objects, so it's faster to create, takes up less space, and new commits are immediately visible to other workspaces.
Of course, Worktree mainly isolates code and can't automatically isolate ports, databases, or Docker containers. When multiple Agents run the project simultaneously, these resources still need separate configuration.

In the era of multi-agent parallel development, worktree is becoming the foundational infrastructure for task isolation.
