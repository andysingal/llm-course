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
