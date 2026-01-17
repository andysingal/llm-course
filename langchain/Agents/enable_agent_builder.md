Agent Builder allows users to create, deploy, and manage AI agents directly within LangSmith. This page explains how to enable Agent Builder on a self-hosted LangSmith instance.

Agent Builder consists of the following components:
- agentBootstrap: Job that deploys the LangSmith Deployment (agent) needed for Agent Builder.
agentBuilder
- toolServer: Provides MCP tool execution for agents.
- triggerServer: Handles webhooks and scheduled triggers.
- agent: The main agent that will handle agent generation and where all the assistants will be created.

[ai_email_agent_langsmith.md](https://github.com/user-attachments/files/24683944/ai_email_agent_langsmith.md)
# How I Built an AI Agent to Automate My Emails

Based on the YouTube video: *How I built an AI agent to automate my emails with LangSmith Agent Builder*  
Source: https://www.youtube.com/watch?v=bzcAZJTxOrs

---

## Overview

This document summarizes how an AI agent can be built using **LangSmith Agent Builder** to automate email workflows such as reading, classifying, and drafting responses.

---

## What Is LangSmith Agent Builder?

LangSmith Agent Builder is a no-code interface for creating AI agents using natural language instructions. It allows users to:

- Define agent behavior in plain English  
- Connect real-world tools (like Gmail)  
- Add human approval steps  
- Monitor and debug agent runs  

---

## Agent Architecture

### Trigger
- Activated when a new email is received.

### Tools
- Gmail (read, draft, send)
- Optional calendar or notification tools

### Instructions
The agent is instructed to:
1. Read incoming emails
2. Identify intent and urgency
3. Draft a concise, context-aware response
4. Request human approval before sending

---

## Testing & Results

- Informational emails are auto-drafted or archived
- Action-required emails generate suggested replies
- Sensitive actions require approval

---

## Benefits

- Saves time on repetitive email tasks
- Maintains human control where needed
- Demonstrates practical no-code AI agents

---

## Resources

- LangSmith Agent Builder Docs: https://docs.langchain.com/langsmith/agent-builder
- Video: https://www.youtube.com/watch?v=bzcAZJTxOrs
