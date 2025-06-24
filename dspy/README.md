DSPy is a framework for algorithmically optimizing LM prompts and weights, especially when LMs are used one or more times within a pipeline. To use LMs to build a complex system without DSPy, you generally have to: (1) break the problem down into steps, (2) prompt your LM well until each step works well in isolation, (3) tweak the steps to work well together, (4) generate synthetic examples to tune each step, and (5) use these examples to finetune smaller LMs to cut costs. Currently, this is hard and messy: every time you change your pipeline, your LM, or your data, all prompts (or finetuning steps) may need to change.

To make this more systematic and much more powerful, DSPy does two things. First, it separates the flow of your program (modules) from the parameters (LM prompts and weights) of each step. Second, DSPy introduces new optimizers, which are LM-driven algorithms that can tune the prompts and/or the weights of your LM calls, given a metric you want to maximize.

DSPy can routinely teach powerful models like GPT-3.5 or GPT-4 and local models like T5-base or Llama2-13b to be much more reliable at tasks, i.e. having higher quality and/or avoiding specific failure patterns. DSPy optimizers will "compile" the same program into different instructions, few-shot prompts, and/or weight updates (finetunes) for each LM. This is a new paradigm in which LMs and their prompts fade into the background as optimizable pieces of a larger system that can learn from data. tldr; less prompting, higher scores, and a more systematic approach to solving hard tasks with LMs.

<img width="570" alt="Screenshot 2024-11-19 at 8 06 32 PM" src="https://github.com/user-attachments/assets/de2d46ae-f189-4dfb-82e1-6dc1e2007a0b">


Courses:
[Coursera-dspy](https://learn.deeplearning.ai/courses/dspy-build-optimize-agentic-apps/lesson/wwje4/debug-your-dspy-agent-with-mlflow-tracing)


Resources:
- https://gist.github.com/jrknox1977
- https://www.lycee.ai/blog/getting-started-with-dspy
- https://github.com/PhiBrandon/resume_extraction_dspy/blob/main/start.py 
- [Mental-Health-Conversations-Using-DSPy-and-Qdrant](https://github.com/manas95826/Mental-Health-Conversations-Using-DSPy-and-Qdrant/blob/main/app.py)
- [Multi-Hop Retrieval](https://dspy.ai/tutorials/multihop_search/)
- [Financial Analysis with DSPy ReAct and Yahoo Finance News](https://dspy.ai/tutorials/yahoo_finance_react/)
