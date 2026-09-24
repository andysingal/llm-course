LLM → JEV → AGENT

I want you to install Jev by TypeSafe AI into the AI agent or LLM environment I am using right now, then make Jev available for future tasks in this project. I should be able to write normal task prompts. You should call Jev when its decision could improve the next action, without requiring me to mention Jev.

Complete the setup and verify it. Work through the steps below; do not stop after giving me a plan.

- 1. Understand my work

Read the conversation and project context you can actually access. Identify three specific situations in my work where Jev could help decide what to do before expensive agent work begins. Give one short example for each. Do not claim access to other chats or files you cannot see.

- 2. Check this environment

Before running any installation commands, identify the exact environment you are currently running in: Claude Code, Codex, Grok Bot, Muse, Cursor, another coding agent, or an ordinary LLM chat.

Output:

```py
AGENT: detected agent
PROJECT: detected project path / unavailable
OS: detected OS / unknown
CAPABILITIES: terminal / file access / network / persistent instructions / unavailable

```

Check only the installation methods and commands relevant to the detected agent and operating system. Do not test Claude Code, Codex, macOS, npx, or other unrelated environments unless they are actually required.

If you have terminal and file access, continue with installation. If you cannot modify the user’s system, do not claim to install Jev; complete the analysis and provide the exact shortest handoff required for a compatible agent. Preserve existing project instructions and configuration.

3. Use verified sources

Check the current official TypeSafe instructions:

https://docs.typesafe.ai/introduction/quickstart
https://docs.typesafe.ai/agent-skill
https://github.com/typesafe-ai/skills

For the working decision router, inspect:

https://github.com/Bodil51/muse-jev-playbook
https://github.com/Bodil51/muse-jev-playbook/blob/main/QUICKSTART.md

The official TypeSafe skill teaches you the API. The muse-jev-playbook repository provides routing code, recipes, and an agent policy. Treat these as separate components.

4. Install and test

Follow the repository’s current QUICKSTART in an appropriate project directory. On a Unix-like system, its setup begins with:

```py
git clone https://github.com/Bodil51/muse-jev-playbook.git
cd muse-jev-playbook
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp config.example.yaml config.yaml
```

Adapt commands to this operating system if necessary. Read the relevant files before changing configuration. Install the official TypeSafe skill using the supported method for this agent; use one installation method, not duplicate copies.

Run the repository’s offline dry run first. Then guide me to create an API key at:

https://console.typesafe.ai/keys

Tell me exactly how to set TYPESAFE_API_KEY privately in this environment. Never ask me to paste the key into chat, display its value, or commit it.

Once it is available, run the live CLI check from QUICKSTART and verify that Jev returned an actual response.

Jev returns typed choice, score, and null answers. The router translates them into actions. Do not mistake an SDK import or a successful raw API call for a working agent integration.


5. Make future use natural

Add a concise, project-scoped instruction to the persistent instruction file supported by the detected agent:

CLAUDE.md for Claude Code
AGENTS.md for Codex
or the equivalent rules, memory, skill, project-instruction, or configuration file for Grok Bot, Muse, Cursor, or another agent.

Preserve its current content.

The instruction must tell the agent:

```
Before substantial browser research, repeating a failed approach, loading several tools or skills, spawning agents, choosing between materially different execution routes, or proposing a consequential action, consider whether a small bounded Jev decision would change the next step. If yes, build a compact state without secrets, call the installed router, interpret its action, and continue the original task. Skip Jev for simple answers, deterministic calculations, routine file edits, and situations where the call adds no useful decision. Respect “bypass jev”. Keep irreversible actions behind human confirmation.

```
Connect this instruction to a tool invocation that this agent can actually perform. Do not claim that adding an instruction alone guarantees Jev will run.

Start in the repository’s “shadow” mode, inspect the decision log, and explain when moving to “active” would be justified.

6. Prove it works

Test three tasks in this environment:

A simple question that should skip Jev.
A substantial task with a real routing decision.
A repeated failure where the router may recommend changing approach.

Check both the agent’s behavior and the router’s logs.

If a test needs a new session to verify that instructions persist, start one if possible or give me the exact one-line test to run there.

Finish with a compact report:

- What was installed
- Where the files are
- Whether the live API call succeeded
- Whether this agent actually invoked the router on a suitable task
- Which tests passed
- What still needs my action

Give me three personalized prompts to try next.

Never mark the integration complete without evidence that the agent used Jev during a real task.

A key point: this prompt assumes the assistant may have terminal access, file access, network access, and the ability to modify project files. In this chat environment, I do not have access to your local machine, project directory, persistent agent configuration, or external networked installation targets, so I can extract and analyze the instructions but cannot actually perform the installation described.
