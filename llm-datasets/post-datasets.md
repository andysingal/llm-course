[AgentInstruct](https://huggingface.co/blog/mlabonne/agentic-datagen)

The AgentInstruct pipeline consists of four main steps:

1. Seed Collection: Assemble a diverse collection of raw seeds, such as textbook chapters, web articles, and code snippets. These seeds serve as the foundation for generating new instructions.
2. Content Transformation: One or more specialized agents modify each seed into an intermediate representation that simplifies instruction creation. These agents are designed to perform tasks like generating argument passages, debates, conversations, meeting transcripts, poems, satirical content, etc.
3. Seed Instruction Generation: Multiple agents take the transformed seed and generate diverse instructions based on a pre-defined taxonomy of instruction types. For example, in the domain of reading comprehension, the taxonomy includes 43 question types, ranging from literal comprehension to critical analysis and inference.
4. Instruction Refinement: The final stage involves iteratively enhancing the complexity and quality of the generated instructions. This is achieved through suggester-editor agent pairs. Suggester agents propose ways to increase instruction complexity, while editor agents modify the instructions accordingly.




[Data Flywheels for LLM Applications](https://www.sh-reya.com/blog/ai-engineering-flywheel/)

ideas for data flywheels are grounded in several observations:

1. Humans need to be in the loop for evaluation regularly, as human preferences on LLM outputs change over time.
2. Fine-tuning models come with significant overhead, and many teams prefer LLM APIs for rapid iteration and simple deployment. LLM APIs do not always listen to instructions in the prompt, especially over large batches of inputs, and there thus needs to be validators on LLM outputs.
3. LLM-as-a-judge is increasingly popular. LLMs are getting cheaper, better, and faster.
4. Empirical evidence shows that few-shot examples are most effective for improving prompt performance. As such, LLM-as-a-judge can be aligned with human preferences—given the right few-shot examples.
