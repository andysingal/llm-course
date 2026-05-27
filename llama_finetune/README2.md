[SFT_HF_TOOL_CHOICE](https://github.com/samugit83/TheGradientPath/tree/master)

A curated learning journey through modern machine learning and artificial intelligence.

This repository blends concise Python scripts, richly commented Jupyter notebooks, and step-by-step video tutorials to help you build intuition from first principles to state-of-the-art models. Every concept is paired with runnable code so you can tinker, break things, and understand the gradients under the hood.

[text-to-lora](https://github.com/SakanaAI/text-to-lora)


[Tinker Cookbook - Complete Training Patterns](https://github.com/sundial-org/skills/blob/main/skills/tinker/SKILL.md)

Tinker Cookbook provides two levels of abstraction for fine-tuning language models:

- High-Level Cookbook API: Declarative configuration with chz, structured dataset builders, automatic training loops
- Low-Level Tinker API: Manual control over training steps, direct ServiceClient usage, custom training loops
Choose based on your needs:

Use Cookbook for standard SFT workflows with built-in datasets and patterns
Use Low-Level API for custom training logic, research experiments, or fine-grained control


My Fine-tuning Stack for Small Language Models (2B to 15B Models)

It costs me around $150 to generate a fresh dataset (~150M) and fine-tune the model.

- > Codex 5.5= orchestrator / operator
- > Deekseek v4 pro /Kimi 2.6= data gen. engine (dirt cheap)
- > Qwen 3.5 = best model to fine-tune (4B, 9B, 27B)
- > Unsloth = faster, cheaper fine-tuning framework.
- > Colab = Cheapest cloud GPU (A100 80GB for $0.66/hr)
- > G Drive = to save datasets (good codex + colab integration)
- > Huggingface = To host datasets + Models

<img width="512" height="497" alt="Screenshot 2026-05-26 at 8 41 16 PM" src="https://github.com/user-attachments/assets/e48fa2bd-3570-4ef9-a28f-ff0422aa8c6f" />
