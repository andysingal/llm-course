[Docker×OllamaでRAG](https://zenn.dev/hatyibei/articles/feba2e63f65b67)

```py
# Launch with GPU support
docker compose --profile gpu up -d --build

# Pull the model (first time only)
docker compose exec ollama ollama pull llama3

# Register a document
mkdir -p data/docs
printf "## Password Change Procedure\n1. Open Settings\n2. Select Security\n3. Enter New Password\n" > data/docs/sample_manual.md
make ingest

# Send a query
curl -s -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question":"How do I change my password?"}' | python3 -m json.tool
```
