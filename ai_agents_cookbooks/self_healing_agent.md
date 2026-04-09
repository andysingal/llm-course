[How to Build Self-Healing AI Agents with Monocle, Okahu MCP and OpenCode](https://dev.to/astrodevil/how-to-build-self-healing-ai-agents-with-monocle-okahu-mcp-and-opencode-1g4e)

By the end, you'll have a working demo where:

- A buggy Text-to-SQL application fails its test suite
- An agent queries its own traces from Okahu Cloud via MCP
- The agent identifies and fixes bugs based on trace analysis
- All tests pass, without a human reading logs or prompting fixes

These traces include:

- LLM calls: Inputs, outputs, model name, token usage
- App traces: OpenTelemetry compatible for exporting traces/spans from an application.
- Tool invocations: Agent framework tool calls and responses
- Errors and latency: Exception details and timing data

