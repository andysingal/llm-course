##### Skills
[Skills](https://github.com/anthropics/skills) are folders of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks. Skills teach Claude how to complete specific tasks in a repeatable way, whether that's creating documents with your company's brand guidelines, analyzing data using your organization's specific workflows, or automating personal tasks.

####### Skill Sets
./skills: Skill examples for Creative & Design, Development & Technical, Enterprise & Communication, and Document Skills
./spec: The Agent Skills specification
./template: Skill template



Write a Mermaid / D2 flowchart in http://[SKILL.md](https://support.claude.com/en/articles/12580051-teach-claude-your-way-of-working-using-skills)

[Using skills in the API](https://platform.claude.com/docs/en/build-with-claude/skills-guide#creating-a-skill)

Now when you invoke /<skill-name>, the steps can be magically enforced, just like workflows. 
Agents won't lost in the middle any more.

In the meantime, agents can still understand it as usual.

#### Flow skills
Flow skills are a special skill type that embed an agent flow diagram in SKILL.md, used to define multi-step automated workflows . Unlike standard skills , flow skills are invoked via /flow:<name> commands and automatically execute multiple conversation turns following the flow diagram.

####### Creating a flow skill
To create a flow skill, set ```type: flow ``` in the frontmatter and include a Mermaid or D2 code block in the content:

```
----
name: code-review
description: Code review Workflow
type: flow
----
```mermaid
flowchart TD
A([BEGIN]) --> B[Analyze code changes, list all modified files and features]
B --> c{Is code quality acceptable?}
C --> |Yes| D[Generate code review report]
C -->|No| E[List Issues and propose improvements]
E --> B
D --> F([END])
```
### Reference
-- [Claude1](https://github.com/anthropics/skills?tab=readme-ov-file)

[Claude Skills: definition, use cases, and limitations](https://portkey.ai/blog/claude-skills-definition-use-cases-and-limitations/)

[Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills)
A practical guide to turning agent skills into something you can test, score, and improve over time.

[claude-skills](https://github.com/dmccreary/claude-skills)
Claude Skills for Intelligent Textbooks is a comprehensive collection of AI-powered skills and workflows designed to revolutionize educational content creation. Built with Claude AI and optimized for intelligent textbook development, this repository provides educators and content creators with powerful tools to generate interactive, standards-based educational materials at scale.

[Langchain-skills](https://playbooks.com/skills/hoodini/ai-agents-skills/langchain)
This skill helps you build production-grade LLM applications using LangChain and LangGraph. It provides patterns for composing chains, RAG pipelines, agent graphs, memory, streaming, and structured outputs so you can orchestrate complex LLM workflows reliably. The examples cover LCEL composition, retriever-augmented generation, tool-using agents, and tracing with LangSmith.

[langchain-kill-1](https://playbooks.com/skills/omer-metin/skills-for-antigravity/langgraph)

[digital-brain-skill](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/tree/main/examples/digital-brain-skill)
Digital Brain is a structured knowledge management system designed for AI-assisted personal productivity. It provides a complete folder-based architecture for managing:

- Personal Brand - Voice, positioning, values
- Content Creation - Ideas, drafts, publishing pipeline
- Knowledge Base - Bookmarks, research, learning
- Network - Contacts, relationships, introductions
- Operations - Goals, tasks, meetings, metrics

[design-taste-frontend](https://github.com/Leonxlnx/taste-skill/blob/main/SKILL.md)
This project gives your AI (like in Antigravity, Cursor, Codex, Claude Code) good taste. It stops the AI from generating boring, generic, "slop" code and forces it to build modern, high-end interfaces.
