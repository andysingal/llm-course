All you need to know about Parameter Efficient Fine-Tuning (PEFT) • [http://peft.aman.ai](https://aman.ai/primers/ai/parameter-efficient-fine-tuning/) 

- Parameter Efficient Fine-Tuning (PEFT) methods are crucial for foundation models such as LLMs because they allow for adapting these large models to specific tasks without needing to update all the parameters. This reduces computational costs and memory requirements, making it more feasible to customize these models for diverse applications with limited resources.
- Here is a primer that covers the A-to-Z of PEFT methods, what to use when, hyperparameters, performance vs. efficiency trade-offs, etc.

➡️ Overview
➡️ Advantages (+Practical Use-cases)
➡️ PEFT Methods based on Prompt Modifications
- 🔹 Soft Prompt Tuning - Soft Prompt vs. Prompting
- 🔹 Prefix Tuning
- 🔹 Hard Prompt Tuning
- 🔹 Adapters (What is an Adapter Module?, Deciding the Value of m, LLaMA-Adapters)
➡️ PEFT Methods based on Reparameterization
- 🔹 Low Rank Adaptation (LoRA) 
- 🔹 Quantized Low-Rank Adaptation (QLoRA)
- 🔹 Quantization-Aware Low-Rank Adaptation (QA-LoRA)
- 🔹 Refined Low-Rank Adaptation (ReLoRA)
- 🔹 Weight-Decomposed Low-Rank Adaptation (DoRA)
- 🔹 Low-Rank Linear Subspace Representation Finetuning (LoReFT)
- ➡️ Summary of LoRA Techniques (LoRA, QLoRA, QA-LoRA, ReLoRA, DoRA, LoftQ, LongLoRA, MultiLoRA, LQ-LoRA, LoRA-FA, Tied-LoRA, GLoRA)
- ➡️ Which PEFT Technique to Choose: A Mental Model
- 🔹 Soft Prompt Tuning
- 🔹 Prefix Tuning
- 🔹 Adapters
- 🔹 LoRA
- 🔹 QA-LoRA
- 🔹 ReLoRA
- ➡️ Comparison of Popular PEFT Methods
- ➡️ Practical Tips for Finetuning LLMs Using LoRA
- ➡️ Related: Surgical Fine-tuning
