[research_agent](https://github.com/langchain-ai/deepagents/blob/master/examples/research/research_agent.py)

[LangChain DeepAgents × Local LLM](https://zenn.dev/retrieva_tech/articles/5a1d7123baaa61)

```
 Terminal1: OpenAI互換APIをローカルで公開
$ export OLLAMA_HOST=127.0.0.1:11434
$ ollama serve

 Terminal2: モデルの取得
$ export OLLAMA_HOST=127.0.0.1:11434
$ ollama pull gpt-oss:20b

$ curl http://127.0.0.1:11435/v1/models
{"object":"list","data":[{"id":"gpt-oss:20b","object":"model","created":1762493511,"owned_by":"library"},{"id":"hf.co/lmstudio-community/gpt-oss-20b-GGUF:latest","object":"model","created":1762322897,"owned_by":"lmstudio-community"}]}

```

