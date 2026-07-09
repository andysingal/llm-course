[LangChain + MCP + RAG + Ollama = The Key To Powerful Agentic AI](https://gaodalie.substack.com/p/langchain-mcp-rag-ollama-the-key)

[How to Build an MCP Server in 5 Lines of Python](https://huggingface.co/blog/gradio-mcp)

[CAMEL-AI-mcp](https://www.camel-ai.org/blogs/camel-ai-agent-mcp-integration)

[Desktop Extensions: One-click MCP server installation for Claude Desktop](https://www.anthropic.com/engineering/desktop-extensions)

[Create a Local MCP Stack to Investigate Apache Spark Job Failures Privately](https://medium.com/@fatikir15/create-a-local-mcp-stack-to-investigate-apache-spark-job-failures-privately-9b5ece62ffad)


##Integrating MCPs
[Pipedream](https://mcp.pipedream.com/developers)

Run your own MCP server for over 2,500 apps and APIs. You can run the servers locally with npx @pipedream/mcp or host the servers yourself to use them within your app or company.


[Top MCP Servers That Turn Claude Into a Productivity Machine](https://x.com/zodchiii/status/2041804097628582294)

- There are over 10,000 MCP servers listed across directories right now. Most of them are weekend projects that break the first time you try them.
- I tested dozens over last year of vibecoding and kept the ones that actually work, are actively maintained, and solve a real problem. 
- These are the MCP servers worth installing, sorted by what they do.


[Specify MCP Servers in LLM Calls](https://blog.dailydoseofds.com/p/specify-mcp-servers-in-llm-calls)

<img width="698" alt="Screenshot 2025-06-09 at 8 49 04 PM" src="https://github.com/user-attachments/assets/62b56ce1-a97b-40f1-b86c-9b9dccd11748" />


[PM/EMでもClaude Code](https://qiita.com/iwa-set/items/4d22dc8b4b8078d3db91)

```
from mcp.server.fastmcp import FastMCP
from sentence_transformers import SentenceTransformer
import lancedb

mcp = FastMCP("knowledge-search")

# Lazy initialization（初回呼び出し時にロード）
_model = None
_table = None

def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("intfloat/multilingual-e5-base")
    return _model

@mcp.tool()
def search_knowledge(query: str, limit: int = 10,
                     source_type: str | None = None,
                     project: str | None = None) -> dict:
    """プロジェクト横断の意味検索"""
    model = _get_model()
    table = _get_table()
    query_vec = model.encode(
        [f"query: {query}"], normalize_embeddings=True, convert_to_numpy=True
    )[0]
    q = table.search(query_vec.tolist()).limit(limit)
    # source_type / project でフィルタ
    if source_type:
        q = q.where(f"source_type = '{source_type}'")
    if project:
        q = q.where(f"project = '{project}'")
    rows = q.to_list()
    results = []
    for r in rows:
        similarity = max(0.0, 1.0 - r.get("_distance", 0.0) / 2)
        results.append({
            "score": round(similarity, 4),
            "project": r.get("project", ""),
            "source_file": r.get("source_file", ""),
            "source_type": r.get("source_type", ""),
            "date": r.get("date", ""),
            "text": r.get("text", ""),
        })
    return {"query": query, "count": len(results), "results": results}

@mcp.tool()
def get_context(source_file: str, chunk_index: int, window: int = 3) -> dict:
    """検索結果の前後チャンクを取得"""
    table = _get_table()
    rows = table.search().where(f"source_file = '{source_file}'") \
                .select(["chunk_index", "header_path", "text"]).limit(10000).to_list()
    rows.sort(key=lambda r: r["chunk_index"])
    selected = [r for r in rows
                if chunk_index - window <= r["chunk_index"] <= chunk_index + window]
    return {"source_file": source_file, "chunks": selected}

@mcp.tool()
def reindex(projects: str | None = None, meetings: str | None = None) -> dict:
    """インデックスを再構築（ingest.py を実行）"""
    global _table
    _table = None  # 再構築後にテーブルを再読み込みさせる
    cmd = [sys.executable, str(INGEST_SCRIPT), "--rebuild"]
    if projects:
        cmd.extend(["--projects", projects])
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=21600)
    return {"status": "ok" if result.returncode == 0 else "error"}

if __name__ == "__main__":
    mcp.run()
```

[Model Context Protocol Explained in 3 Levels of Difficulty](https://machinelearningmastery.com/model-context-protocol-explained-in-3-levels-of-difficulty/)

- Why connecting models to external systems without a shared standard creates an integration problem that grows with every new client or tool.
- How the host, client, and server work together, and what happens when a model’s request flows through an MCP server.
- The transport options, security risks, and deployment choices that matter once an MCP server is running in production.

[How to Build an MCP Server with FastMCP for Your Local AI Agent](https://www.freecodecamp.org/news/build-an-mcp-server-with-fastmcp-for-local-ai-agent/)

- I'll show you how to build an MCP server with FastMCP, connect your local AI agent to use tools from the local MCP server that you built, and add support for remote MCP server
- MCP improves this by giving tools a standard interface that any MCP-compatible client can use. Write the tool once as an MCP server, and any compatible client can reuse it. And because MCP is a network protocol, those tools don't even have to run on your machine. Someone else can host an MCP server, and your agent can use its tools the same way it uses your local ones.
- FastMCP is a Python library that makes writing an MCP server feel like writing a FastAPI app. You decorate functions with @mcp.tool, and FastMCP handles the protocol details: JSON-RPC messages, tool schema generation from your type hints and docstrings, and the transport layer.
- On the LangChain side, langchain-mcp-adapters is a library that connects to one or more MCP servers and loads their tools into a format LangChain v1's create_agent can use directly.
- The motivation behind this project is to create sharable tools and to reuse tools others have already built. I wanted to create tools like current_time and word_count and share them across every agent I build.
- For this project, I'll use FastMCP to build a local MCP server with two tools, connect to DeepWiki's free public MCP server for GitHub repo lookups, use langchain-mcp-adapters to load both into a LangChain v1 agent, and Ollama to run the local Qwen model.

The flow has three processes.

- The local MCP server is a standalone Python script that exposes current_time and word_count. It runs as a subprocess of the agent, over stdio.

- The remote MCP server is DeepWiki's public service that exposes three tools (read_wiki_structure, read_wiki_contents, ask_question) for asking questions about any GitHub repo, over HTTP.

- The agent is the coordinating script that connects to both, merges their tools into a single list, and runs the interactive loop.

```mcp_server.py```
```py
from datetime import datetime
from fastmcp import FastMCP

mcp = FastMCP("local-tools")


@mcp.tool
def current_time() -> str:
    """Return the current local date and time.
    Use this when the user asks what time or date it is.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@mcp.tool
def word_count(text: str) -> int:
    """Count the number of words in a piece of text.
    Use this when the user asks how long a piece of writing is
    or asks you to count the words in something they've shared.
    Returns the word count as an integer.
    """
    return len(text.split())


if __name__ == "__main__":
    # Run the MCP server over stdio.
    mcp.run()
```
Since this tools_server.py will be run in stdio mode as a subprocess, we don't need to start it separately. The agent will run it automatically.

```Agent```
The agent code does three things. First, the configuration at the top defines the model, the system prompt, and the URL of the remote MCP server. The build_agent() function connects to both MCP servers, loads their tools into a single list, and creates a LangChain v1 agent. The main() function runs the interactive loop.

```
import asyncio

from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient

# Local Ollama model to use for the chat agent.
CHAT_MODEL = "qwen3.5:4b"

# Hosted remote MCP server we'll connect to over HTTP.
DEEPWIKI_MCP_URL = "https://mcp.deepwiki.com/mcp"

# System prompt that tells the model what tools it has and how to behave.
SYSTEM_PROMPT = (
    "You are a helpful assistant with access to tools for checking the current time, "
    "counting words, and looking up information about GitHub repositories. "
    "Use tools when the user's request needs information you don't already have. "
    "If a tool returns an error, tell the user plainly and do not retry with made-up arguments. "
    "If the question doesn't need a tool, just answer directly."
)


async def build_agent(client: MultiServerMCPClient):
    # Load tools from all connected MCP servers.
    # This is async because MCP communication happens over I/O.
    tools = await client.get_tools()
    print(f"Loaded {len(tools)} tools: {[t.name for t in tools]}")

    # Create the local Ollama chat model.
    model = ChatOllama(model=CHAT_MODEL, temperature=0)

    # Build a LangChain agent with the local model and all MCP tools.
    return create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )


async def main():
    # Create one MCP client that connects to two servers:
    #
    # 1. "tools" is a local MCP server started as a subprocess over stdio.LangChain will launch `python mcp_server.py` for us.
    # 2. "deepwiki" is a hosted MCP server we connect to over HTTP.
    client = MultiServerMCPClient({
        "tools": {
            "command": "python",
            "args": ["mcp_server.py"],
            "transport": "stdio",
        },
        "deepwiki": {
            "url": DEEPWIKI_MCP_URL,
            "transport": "streamable_http",
        },
    })

    # Build the agent after the MCP client is ready and tools are loaded.
    agent = await build_agent(client)

    print("\nReady! Ask the agent something.")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()
        if not question or question.lower() in {"exit", "quit"}:
            break

        # Send the user's message to the agent.
        # We use `ainvoke()` because the agent may call async MCP tools.
        result = await agent.ainvoke({
            "messages": [{"role": "user", "content": question}],
        })

        # Walk through the returned messages and print any tool calls
        # the agent made during this turn.
        for msg in result["messages"]:
            tool_calls = getattr(msg, "tool_calls", None)
            if tool_calls:
                for call in tool_calls:
                    print(f"[tool call] {call['name']}({call['args']})")

        # The final message in the list is the agent's final answer.
        print(f"\nAnswer: {result['messages'][-1].content}\n")


if __name__ == "__main__":
    # Run the async program.
    asyncio.run(main())
```

