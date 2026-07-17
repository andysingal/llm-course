Kubernetes (Helm)
Deploy the AI-Q blueprint to a Kubernetes cluster using the Helm charts included in the repository.

Prerequisites
Kubernetes cluster (EKS, GKE, AKS, or a local cluster such as Kind or Minikube).

kubectl configured with cluster access.

[helm v3.x installed](https://docs.nvidia.com/aiq-blueprint/2.2.0-rc1/deployment/kubernetes.html)

API keys for the models and tools you plan to use (refer to Installation – API Key Setup).

```
kubectl create namespace ns-aiq --dry-run=client -o yaml | kubectl apply -f -

```

```
kubectl create secret generic aiq-credentials -n ns-aiq \
  --from-literal=NVIDIA_API_KEY="$NGC_API_KEY" \
  --from-literal=TAVILY_API_KEY="$TAVILY_API_KEY" \
  --from-literal=DB_USER_NAME="aiq" \
  --from-literal=DB_USER_PASSWORD="aiq_dev"
```


[Example: Full Pipeline (Foundational RAG)](https://docs.nvidia.com/aiq-blueprint/2.2.0-rc1/examples/full-pipeline-web.html)

The complete AI-Q blueprint configuration with all features enabled: intent classification, shallow and deep research agents, knowledge retrieval (Foundational RAG), paper search, web search, clarifier with human-in-the-loop clarification, and the async jobs API with SSE streaming.

This is based on ```configs/config_web_frag.yml```, which is the default for Helm deployments.

```
# config_web_frag.yml (annotated)
# Full pipeline: Web mode with Foundational RAG knowledge layer

# ===========================================================================
# General settings
# ===========================================================================
general:
  use_uvloop: true  # Use uvloop for better async performance (Linux/macOS)

  telemetry:
    logging:
      console:
        _type: console
        level: INFO
    # Uncomment for tracing:
    # tracing:
    #   phoenix:
    #     _type: phoenix
    #     endpoint: http://localhost:6006/v1/traces
    #     project: dev

  # ---------------------------------------------------------------------------
  # Front-end: AI-Q API plugin
  # ---------------------------------------------------------------------------
  # This enables the async jobs API, SSE streaming, and Knowledge API.
  # Without this section, `nat serve` uses NeMo Agent Toolkit's default WebSocket front-end.
  front_end:
    _type: aiq_api
    runner_class: aiq_api.plugin.AIQAPIWorker

    # Async job database (JobStore + EventStore)
    # SQLite for local dev, PostgreSQL for production
    db_url: ${NAT_JOB_STORE_DB_URL:-sqlite+aiosqlite:///./jobs.db}

    # Completed jobs are cleaned up after this duration
    expiry_seconds: 86400  # 24 hours (range: 600 to 604800)

    # CORS settings for the frontend UI
    cors:
      allow_origin_regex: 'http://localhost(:\d+)?|http://127.0.0.1(:\d+)?'
      allow_methods: [GET, POST, DELETE, OPTIONS]
      allow_headers: ["*"]
      allow_credentials: true
      expose_headers: ["*"]

# ===========================================================================
# LLMs
# ===========================================================================
# Three LLM configurations for different roles:
# - Intent classification (moderate creativity for routing decisions)
# - Research (low temperature for factual output)
# - Deep research orchestrator (high temperature for diverse planning)
llms:
  nemotron_llm_intent:
    _type: nim
    model_name: nvidia/nemotron-3-super-120b-a12b
    base_url: "https://integrate.api.nvidia.com/v1"
    temperature: 0.5    # Moderate: needs to reason about intent
    top_p: 0.9
    max_tokens: 4096
    num_retries: 5
    chat_template_kwargs:
      enable_thinking: true

  nemotron_super_llm:
    _type: nim
    model_name: nvidia/nemotron-3-super-120b-a12b
    base_url: "https://integrate.api.nvidia.com/v1"
    temperature: 0.1    # Low: factual research output
    top_p: 0.3
    max_tokens: 16384
    num_retries: 5
    chat_template_kwargs:
      enable_thinking: true

# ===========================================================================
# Functions (tools and agents)
# ===========================================================================
functions:
  # -------------------------------------------------------------------------
  # Search tools
  # -------------------------------------------------------------------------
  web_search_tool:
    _type: tavily_web_search
    max_results: 5
    max_content_length: 1000

  advanced_web_search_tool:
    _type: tavily_web_search
    max_results: 2
    advanced_search: true   # Full page content extraction

  paper_search_tool:
    _type: paper_search
    max_results: 5
    serper_api_key: ${SERPER_API_KEY}

  # -------------------------------------------------------------------------
  # Knowledge retrieval (Foundational RAG)
  # -------------------------------------------------------------------------
  # This enables the Knowledge API endpoints (/v1/collections, /v1/documents)
  # and gives agents access to uploaded document collections.
  knowledge_search:
    _type: knowledge_retrieval
    backend: foundational_rag
    collection_name: ${COLLECTION_NAME:-test_collection}
    top_k: 5
    rag_url: ${RAG_SERVER_URL:-http://localhost:8081}
    ingest_url: ${RAG_INGEST_URL:-http://localhost:8082}
    timeout: 300

  # -------------------------------------------------------------------------
  # Intent classifier
  # -------------------------------------------------------------------------
  # Routes queries to shallow or deep research based on complexity.
  # Has access to tools for context-aware routing decisions.
  intent_classifier:
    _type: intent_classifier
    llm: nemotron_llm_intent
    tools:
      - web_search_tool
      - paper_search_tool
      - knowledge_search

  # -------------------------------------------------------------------------
  # Clarifier agent (human-in-the-loop)
  # -------------------------------------------------------------------------
  # For deep research: asks clarifying questions before handing off to the
  # deep_research_agent.
  clarifier_agent:
    _type: clarifier_agent
    llm: nemotron_super_llm
    tools:
      - web_search_tool
      - knowledge_search
    max_turns: 3                  # Max clarification rounds
    log_response_max_chars: 2000
    verbose: true

  # -------------------------------------------------------------------------
  # Shallow research agent
  # -------------------------------------------------------------------------
  # Single-turn ReAct agent for quick queries.
  shallow_research_agent:
    _type: shallow_research_agent
    llm: nemotron_super_llm
    tools:
      - web_search_tool
      - knowledge_search
    max_llm_turns: 10
    max_tool_iterations: 5

  # -------------------------------------------------------------------------
  # Deep research agent
  # -------------------------------------------------------------------------
  # Multi-loop orchestrator that plans research, delegates to sub-agents,
  # and synthesizes comprehensive reports.
  deep_research_agent:
    _type: deep_research_agent
    orchestrator_llm: nemotron_super_llm
    tools:
      - paper_search_tool
      - advanced_web_search_tool
      - knowledge_search

# ===========================================================================
# Workflow
# ===========================================================================
# The chat_deepresearcher_agent is the meta-routing workflow:
# 1. Intent classifier determines shallow vs deep
# 2. Shallow queries go directly to shallow_research_agent
# 3. Deep queries go through clarifier -> deep_research_agent
workflow:
  _type: chat_deepresearcher_agent
  enable_escalation: true          # Allow shallow -> deep escalation
  enable_clarifier: true           # Enable clarification flow for deep research
  use_async_deep_research: true    # Run deep research asynchronously
  checkpoint_db: ${AIQ_CHECKPOINT_DB:-./checkpoints.db}

```

### Required Environment Variables
```
# Core (required)
export NVIDIA_API_KEY="nvapi-..."    # pragma: allowlist secret
export TAVILY_API_KEY="tvly-..."     # pragma: allowlist secret
export SERPER_API_KEY="..."

# Knowledge layer (required if using Foundational RAG)
export RAG_SERVER_URL="http://localhost:8081"
export RAG_INGEST_URL="http://localhost:8082"

# Optional: production database
# export NAT_JOB_STORE_DB_URL="postgresql+asyncpg://user:pass@host:5432/aiq_jobs"  # pragma: allowlist secret
```


