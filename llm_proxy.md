A few design decisions I made:

• Keep the API OpenAI-compatible so existing tools work without modification.
• Store provider configuration in YAML instead of hardcoding routing logic.
• Support automatic failover when a provider returns rate limits or server errors.
• Route web search requests separately instead of forcing every model to implement search.
• Add a dashboard so I could see latency, failures, and provider health while debugging.


```
Client (Claude Code / n8n / Hermes Agent)
↓
jc-proxy
↓
Gemini / Groq / OpenRouter / Cloudflare Workers AI
```

[jc-proxy](https://github.com/iniyavanjambulingam/jc-proxy)

A lightweight OpenAI & Anthropic compatible API gateway with intelligent provider routing, automatic failover, tool calling support, and streaming. Specifically optimized for n8n AI Agents and Claude Code.

