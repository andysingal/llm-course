[Mesh LLM](https://github.com/Mesh-LLM/mesh-llm)

Mesh LLM lets you pool spare GPU capacity across machines and expose the result as one OpenAI-compatible API.

If a model fits on one machine, it runs there. If it does not, Mesh LLM automatically spreads the work across the mesh:

- Dense models use pipeline parallelism.
- MoE models use expert sharding with zero cross-node inference traffic.
- Models collaborate during inference — a text-only model consults a vision peer, an uncertain model gets a second opinion from a different architecture.
- Every node gets the same local API at http://localhost:9337/v1.
