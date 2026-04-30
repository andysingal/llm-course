[docker-ollama](https://github.com/hwdsl2/docker-ollama)

Docker image to run an Ollama local LLM server. Provides an OpenAI-compatible API for running large language models locally. Based on Debian Trixie (slim). Designed to be simple, private, and secure by default.

Features:

- Secure by default — all API requests require a Bearer token (auto-generated on first start)
- Auto-generates an API key on first start, stored in the persistent volume
- First-start model pre-pull via OLLAMA_MODELS environment variable
- Model management via a helper script (ollama_manage)
- OpenAI-compatible API — point any OpenAI SDK or app at your local server with a one-line change
- Caddy reverse proxy enforces Bearer token auth on all API requests (except / health check)
- NVIDIA GPU (CUDA) acceleration for faster inference (:cuda image tag)
- Automatically built and published via GitHub Actions
- Persistent model storage via a Docker volume
- Lightweight image (~70MB); multi-arch: linux/amd64, linux/arm64

