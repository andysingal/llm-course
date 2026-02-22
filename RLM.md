RLMs are an inference technique where an LLM interacts with arbitrarily long prompts through an external REPL. The LLM can write code to explore, decompose, and transform the prompt. It can recursively invoke sub-agents to complete smaller subtasks. Crucially, sub-agent responses are not automatically loaded into the parent agent's context — they are returned as symbols or variables inside the parent's REPL.

## refo
[fast-RLM](https://github.com/avbiswas/fast-rlm)

[Implementing RLMs](https://www.k-a.in/RLM-py.html)
