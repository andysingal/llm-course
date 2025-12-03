[llm-council](https://github.com/karpathy/llm-council)

![header](https://github.com/user-attachments/assets/eeb08948-13d1-4a7e-97fa-d446f78e38ef)

LLM Council - Multi-model AI with democratic voting (Enhanced fork with 5 production features)
Resources
I've been working on an enhanced version of Karpathy's LLM Council that adds production-ready features while keeping the original vision intact.

What is LLM Council?
Instead of asking one LLM, you ask multiple models simultaneously. They each respond, then anonymously rank each other's answers, and a chairman synthesizes the final response. Think of it as "democratic AI decision-making."

What I Added (5 Features):
🎯 TOON Integration - 30-60% token savings with optimized data format

💾 Multi-Database Support - JSON (default), PostgreSQL, or MySQL

💬 Context & Follow-ups - Natural multi-turn conversations with memory

🛠️ AI Tools - Calculator, Wikipedia, ArXiv, DuckDuckGo, Yahoo Finance \

⚙️ Conversation Management - Delete, edit titles, temporary chat mode

Tech Stack:
Backend: FastAPI, LangChain, SQLAlchemy, ChromaDB

Frontend: React + Vite with Server-Sent Events

Models: Any via OpenRouter (GPT-5.1, Gemini, Claude, Grok, etc.)

Free Features:
All 5 free tools enabled by default

Local embeddings with HuggingFace (no API needed)

JSON storage (zero setup)

Optional: Tavily search, OpenAI embeddings

[Democracy-council](https://github.com/Reeteshrajesh/llm-council)
