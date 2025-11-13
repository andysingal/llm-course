[The Reasoning Course](https://huggingface.co/reasoning-course)

[Deepseek-reasoning](https://www.53ai.com/news/RAG/2025030783124.html)

[ReZero](https://github.com/menloresearch/ReZero?tab=readme-ov-file#quick-demo-)

[thinking-nonthinking-model-qwen](https://qwen.readthedocs.io/zh-cn/latest/_sources/inference/transformers.md.txt)

Add to the user (or the system) message, `/no_think` to disable thinking and `/think` to enable thinking.
This method is stateful, meaning the model will follow the most recent instruction in multi-turn conversations.

<img width="581" alt="Screenshot 2025-06-29 at 10 19 31 AM" src="https://github.com/user-attachments/assets/302f0626-3e1a-44fd-a6f3-34e3288ecf64" />

[VibeThinker](https://github.com/WeiboAI/VibeThinker)

VibeThinker-1.5B is a 1.5B-parameter dense model that challenges the prevailing notion that small models inherently lack robust reasoning capabilities.

### Resources:

- [Res1](https://github.com/deansaco/r1-reasoning-rag.git)
- [res2-qwen](https://note.com/npaka/n/n43abd5843fe7)
- [res3-qwen3-CRAG](https://github.com/jacoblee93/corrective-local-rag-qwen?tab=readme-ov-file)
- [res4-qwen-llamacpp](https://qwen.readthedocs.io/en/latest/run_locally/llama.cpp.html)
- [Magistral-Reasoning](https://chat.mistral.ai/chat)

## Tips
One of the most underutilized ways to get far better results from reasoning models like Claude 4, o3, etc:

Add constraints.

Make it super clear to the model what it can and cannot do. By explicitly defining boundaries (things it must avoid, or criteria it must satisfy), you eliminate ambiguity and guide the reasoning process more directly toward your intended outcome.

Constraints act as guardrails, reducing 'laziness' and goal drift.

For example, instead of saying:

"Come up with ideas to grow my app."

You might say:

"Come up with exactly three growth strategies that cost under $100 each, take less than two hours per week to execute, and can reliably generate at least 1,000 new users within 30 days. Avoid strategies involving paid ads or influencer sponsorships."

Notice the immediate clarity? You've removed guesswork and set crystal-clear expectations. This pushes the reasoning model to do exactly what you want, instead of just getting somewhat close to your goals.

Constraints are leverage. Use them.
