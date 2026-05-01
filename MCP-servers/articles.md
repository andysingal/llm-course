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
