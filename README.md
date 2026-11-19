Secure your agents at: CodeAstra.dev

## AI Agent Privacy Notice

Astra Sentinel found a possible pattern where sensitive user, customer, or patient data may be passed directly into an AI agent or LLM context.

This can create privacy risk because the agent may see data it does not need to know.

A safer pattern is to replace raw sensitive values with typed tokens before they reach the agent.

Example:

Before: Book appointment for John Smith, DOB 04/12/1988
After: Book appointment for [CVT:NAME:patient_name], DOB [CVT:DOB:patient_dob]

The agent can still perform the workflow, but it never sees the raw sensitive data.

Detected pattern examples:
```json
[
  {
    "pattern": "unprotected_ai_context",
    "evidence": "assistantagent(name='retriever', llm_config=llm_config_autogen, system_message=\"only execute the function query_graphrag to look for context. \\n                    output 'terminate' when an answer has been provided.\", max_consecutive_auto_reply=1, human_input_mode='never', description='retriever agent')"
  }
]
```

This notice was generated from a privacy scan. Please review before merging.

Secure your agents at: CodeAstra.dev

---

# Awesome-llm-and-aigc
[![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)

🚀🚀🚀 This repository lists some awesome public projects about Large Language Model, Vision Foundation Model, AI Generated Content, the related Datasets and Applications.

## Contents
- [Awesome-llm-and-aigc](#awesome-llm-and-aigc)
  - [Summary](#summary)
    - [Frameworks](#frameworks)
      - [Official Version](#official-version)
        - [Large Language Model](#large-language-model)
        - [Vision Foundation Model](#vision-foundation-model)
        - [AI Generated Content](#ai-generated-content)
      - [Application Development Platform](#application-development-platform)
      - [Fine-Tuning Framework](#fine-tuning-framework)
      - [RAG Framework](#rag-framework)
      - [LLM Inference Framework](#llm-inference-framework)
        - [LLM Inference Benchmark](#llm-inference-benchmark)
        - [LLM Deployment Engine](#llm-deployment-engine)
        - [C Implementation](#c-implementation)
        - [CPP Implementation](#cpp-implementation)
        - [Mojo Implementation](#mojo-implementation)
        - [Rust Implementation](#rust-implementation)
        - [zig Implementation](#zig-implementation)
        - [Go Implementation](#go-implementation)
      - [Vector Database](#vector-database)
    - [Awesome List](#awesome-list)
    - [Paper Overview](#paper-overview)
    - [Learning Resources](#learning-resources)
    - [Community](#community)
  - [Prompts](#prompts)
  - [Open API](#open-api)
    - [Python API](#python-api)
    - [Rust API](#rust-api)
    - [Csharp API](#csharp-api)
    - [Node.js API](#node.js-api)
  - [Applications](#applications)
    - [IDE](#ide)
    - [Chatbot](#chatbot)
    - [Embodied AI](#embodied-ai)
    - [Code Assistant](#code-assistant)
    - [Translator](#translator)
    - [Local knowledge Base](#local-knowledge-base)
    - [Question Answering System](#question-answering-system)
    - [Academic Field](#academic-field)
    - [Medical Field](#medical-field)
    - [Mental Health Field](#mental-health-field)
    - [Legal Field](#legal-field)
    - [Financial Field](#Financial-field)
    - [Math Field](#math-field)
    - [Music Field](#music-field)
    - [Speech and audio Field](#speech-and-audio-field)
    - [Humor Generation](#humor-generation)
    - [Animation Field](#animation-field)
    - [Food Field](#food-field)
    - [Tool Learning](#tool-learning)
    - [Autonomous Driving Field](#autonomous-driving-field)
    - [Adversarial Attack Field](#adversarial-attack-field)
    - [Multi-Agent Collaboration](#multi-agent-collaboration)
    - [AI Avatar](#ai-avatar)
    - [GUI](#gui)
  - [Datasets](#datasets)
    - [Open Datasets Platform](#open-datasets-platform)
    - [Text Datasets](#text-datasets)
    - [Multimodal Datasets](#multimodal-datasets)
    - [SFT Datasets](#sft-datasets)
  - [Blogs](#blogs)
  - [Videos](#videos)
  - [Jobs and Interview](#jobs-and-interview)


## Summary

  - ### Frameworks

    - #### Official Version

      - ##### Large Language Model
        ###### 大语言模型（LLM）

        - GPT-1 : "Improving Language Understanding by Generative Pre-Training". (**[cs.ubc.ca, 2018](https://www.cs.ubc.ca/~amuham01/LING530/papers/radford2018improving.pdf)**).

        - [GPT-2](https://github.com/openai/gpt-2) <img src="https://img.shields.io/github/stars/openai/gpt-2?style=social"/> : "Language Models are Unsupervised Multitask Learners". (**[OpenAI blog, 2019](https://d4mucfpksywv.cloudfront.net/better-language-models/language-models.pdf)**). [Better language models and their implications](https://openai.com/research/better-language-models).

        - [GPT-3](https://github.com/openai/gpt-3) <img src="https://img.shields.io/github/stars/openai/gpt-3?style=social"/> : "GPT-3: Language Models are Few-Shot Learners". (**[arXiv 2020](https://arxiv.org/abs/2005.14165)**).

        - InstructGPT : "Training language models to follow instructions with human feedback". (**[arXiv 2022](https://arxiv.org/abs/2203.02155)**). "Aligning language models to follow instructions". (**[OpenAI blog, 2022](https://openai.com/research/instruction-following)**).

        - [ChatGPT](https://chat.openai.com/): [Optimizing Language Models for Dialogue](https://openai.com/blog/chatgpt).

        - [GPT-4](https://openai.com/product/gpt-4): GPT-4 is OpenAI’s most advanced system, producing safer and more useful responses. "Sparks of Artificial General Intelligence: Early experiments with GPT-4". (**[arXiv 2023](https://arxiv.org/abs/2303.12712)**). "GPT-4 Architecture, Infrastructure, Training Dataset, Costs, Vision, MoE". (**[SemianAlysis, 2023](https://www.semianalysis.com/p/gpt-4-architecture-infrastructure)**).

        - [Llama 2](https://github.com/facebookresearch/llama) <img src="https://img.shields.io/github/stars/facebookresearch/llama?style=social"/> : Inference code for LLaMA models. "LLaMA: Open and Efficient Foundation Language Models". (**[arXiv 2023](https://arxiv.org/abs/2302.13971)**). "Llama 2: Open Foundation and Fine-Tuned Chat Models". (**[ai.meta.com, 2023-07-18](https://ai.meta.com/research/publications/llama-2-open-foundation-and-fine-tuned-chat-models/)**). (**[2023-07-18, Llama 2 is here - get it on Hugging Face](https://huggingface.co/blog/llama2)**).

        - [Llama 3](https://github.com/meta-llama/llama3) <img src="https://img.shields.io/github/stars/meta-llama/llama3?style=social"/> : The official Meta Llama 3 GitHub site.

        - [Gemma](https://github.com/google/gemma_pytorch) <img src="https://img.shields.io/github/stars/google/gemma_pytorch?style=social"/> : The official PyTorch implementation of Google's Gemma models. [ai.google.dev/gemma](https://ai.google.dev/gemma)

        - [Grok-1](https://github.com/xai-org/grok-1) <img src="https://img.shields.io/github/stars/xai-org/grok-1?style=social"/> : This repository contains JAX example code for loading and running the Grok-1 open-weights model.

        - [Claude](https://www.anthropic.com/product) : Claude is a next-generation AI assistant based on Anthropic’s research into training helpful, honest, and harmless AI systems.

        - [Whisper](https://github.com/openai/whisper) <img src="https://img.shields.io/github/stars/openai/whisper?style=social"/> : Whisper is a general-purpose speech recognition model. It is trained on a large dataset of diverse audio and is also a multitasking model that can perform multilingual speech recognition, speech translation, and language identification. "Robust Speech Recognition via Large-Scale Weak Supervision". (**[arXiv 2022](https://arxiv.org/abs/2212.04356)**).

        - [OpenChat](https://github.com/imoneoi/openchat) <img src="https://img.shields.io/github/stars/imoneoi/openchat?style=social"/> : OpenChat: Advancing Open-source Language Models with Imperfect Data. [huggingface.co/openchat/openchat](https://huggingface.co/openchat/openchat)

        - [GPT-Engineer](https://github.com/AntonOsika/gpt-engineer) <img src="https://img.shields.io/github/stars/AntonOsika/gpt-engineer?style=social"/> : Specify what you want it to build, the AI asks for clarification, and then builds it. GPT Engineer is made to be easy to adapt, extend, and make your agent learn how you want your code to look. It generates an entire codebase based on a prompt.

        - [StableLM](https://github.com/Stability-AI/StableLM) <img src="https://img.shields.io/github/stars/Stability-AI/StableLM?style=social"/> : StableLM: Stability AI Language Models.

        - [JARVIS](https://github.com/microsoft/JARVIS) <img src="https://img.shields.io/github/stars/microsoft/JARVIS?style=social"/> : JARVIS, a system to connect LLMs with ML community. "HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in HuggingFace". (**[arXiv 2023](https://arxiv.org/abs/2303.17580)**).

        - [MiniGPT-4](https://github.com/Vision-CAIR/MiniGPT-4) <img src="https://img.shields.io/github/stars/Vision-CAIR/MiniGPT-4?style=social"/> : MiniGPT-4: Enhancing Vision-language Understanding with Advanced Large Language Models. [minigpt-4.github.io](https://minigpt-4.github.io/)

        - [minGPT](https://github.com/karpathy/minGPT) <img src="https://img.shields.io/github/stars/karpathy/minGPT?style=social"/> : A minimal PyTorch re-implementation of the OpenAI GPT (Generative Pretrained Transformer) training.

        - [nanoGPT](https://github.com/karpathy/nanoGPT) <img src="https://img.shields.io/github/stars/karpathy/nanoGPT?style=social"/> : The simplest, fastest repository for training/finetuning medium-sized GPTs.

        - [MicroGPT](https://github.com/muellerberndt/micro-gpt) <img src="https://img.shields.io/github/stars/muellerberndt/micro-gpt?style=social"/> : A simple and effective autonomous agent compatible with GPT-3.5-Turbo and GPT-4. MicroGPT aims to be as compact and reliable as possible.

        - [Dolly](https://github.com/databrickslabs/dolly) <img src="https://img.shields.io/github/stars/databrickslabs/dolly?style=social"/> : Databricks’ Dolly, a large language model trained on the Databricks Machine Learning Platform. [Hello Dolly: Democratizing the magic of ChatGPT with open models](https://www.databricks.com/blog/2023/03/24/hello-dolly-democratizing-magic-chatgpt-open-models.html)

        - [LMFlow](https://github.com/OptimalScale/LMFlow) <img src="https://img.shields.io/github/stars/OptimalScale/LMFlow?style=social"/> : An extensible, convenient, and efficient toolbox for finetuning large machine learning models, designed to be user-friendly, speedy and reliable, and accessible to the entire community. Large Language Model for All. [optimalscale.github.io/LMFlow/](https://optimalscale.github.io/LMFlow/)

        - [Colossal-AI](https://github.com/hpcaitech/ColossalAI) <img src="https://img.shields.io/github/stars/hpcaitech/ColossalAI?style=social"/> : Making big AI models cheaper, easier, and scalable. [www.colossalai.org](www.colossalai.org). "Colossal-AI: A Unified Deep Learning System For Large-Scale Parallel Training". (**[arXiv 2021](https://arxiv.org/abs/2110.14883)**).

        - [Lit-LLaMA](https://github.com/Lightning-AI/lit-llama) <img src="https://img.shields.io/github/stars/Lightning-AI/lit-llama?style=social"/> : ⚡ Lit-LLaMA. Implementation of the LLaMA language model based on nanoGPT. Supports flash attention, Int8 and GPTQ 4bit quantization, LoRA and LLaMA-Adapter fine-tuning, pre-training. Apache 2.0-licensed.

        - [GPT-4-LLM](https://github.com/Instruction-Tuning-with-GPT-4/GPT-4-LLM) <img src="https://img.shields.io/github/stars/Instruction-Tuning-with-GPT-4/GPT-4-LLM?style=social"/> : "Instruction Tuning with GPT-4". (**[arXiv 2023](https://arxiv.org/abs/2304.03277)**). [instruction-tuning-with-gpt-4.github.io/](https://instruction-tuning-with-gpt-4.github.io/)

        - [Stanford Alpaca](https://github.com/tatsu-lab/stanford_alpaca) <img src="https://img.shields.io/github/stars/tatsu-lab/stanford_alpaca?style=social"/> : Stanford Alpaca: An Instruction-following LLaMA Model.

        - [feizc/Visual-LLaMA](https://github.com/feizc/Visual-LLaMA) <img src="https://img.shields.io/github/stars/feizc/Visual-LLaMA?style=social"/> : Open LLaMA Eyes to See the World. This project aims to optimize LLaMA model for visual information understanding like GPT-4 and further explore the potentional of large language model.

        - [Lightning-AI/lightning-colossalai](https://github.com/Lightning-AI/lightning-colossalai) <img src="https://img.shields.io/github/stars/Lightning-AI/lightning-colossalai?style=social"/> : Efficient Large-Scale Distributed Training with [Colossal-AI](https://colossalai.org/) and [Lightning AI](https://lightning.ai/).

        - [GPT4All](https://github.com/nomic-ai/gpt4all) <img src="https://img.shields.io/github/stars/nomic-ai/gpt4all?style=social"/> : GPT4All: An ecosystem of open-source on-edge large language models. GTP4All is an ecosystem to train and deploy powerful and customized large language models that run locally on consumer grade CPUs.

        - [ChatALL](https://github.com/sunner/ChatALL) <img src="https://img.shields.io/github/stars/sunner/ChatALL?style=social"/> :  Concurrently chat with ChatGPT, Bing Chat, bard, Alpaca, Vincuna, Claude, ChatGLM, MOSS, iFlytek Spark, ERNIE and more, discover the best answers. [chatall.ai](http://chatall.ai/)

        - [1595901624/gpt-aggregated-edition](https://github.com/1595901624/gpt-aggregated-edition) <img src="https://img.shields.io/github/stars/1595901624/gpt-aggregated-edition?style=social"/> : 聚合ChatGPT官方版、ChatGPT免费版、文心一言、Poe、chatchat等多平台，支持自定义导入平台。

        - [FreedomIntelligence/LLMZoo](https://github.com/FreedomIntelligence/LLMZoo) <img src="https://img.shields.io/github/stars/FreedomIntelligence/LLMZoo?style=social"/> : ⚡LLM Zoo is a project that provides data, models, and evaluation benchmark for large language models.⚡ [Tech Report](https://github.com/FreedomIntelligence/LLMZoo/blob/main/assets/llmzoo.pdf)

        - [shm007g/LLaMA-Cult-and-More](https://github.com/shm007g/LLaMA-Cult-and-More) <img src="https://img.shields.io/github/stars/shm007g/LLaMA-Cult-and-More?style=social"/> : News about 🦙 Cult and other AIGC models.

        - [X-PLUG/mPLUG-Owl](https://github.com/X-PLUG/mPLUG-Owl) <img src="https://img.shields.io/github/stars/X-PLUG/mPLUG-Owl?style=social"/> : mPLUG-Owl🦉: Modularization Empowers Large Language Models with Multimodality.

        - [i-Code](https://github.com/microsoft/i-Code) <img src="https://img.shields.io/github/stars/microsoft/i-Code?style=social"/> : The ambition of the i-Code project is to build integrative and composable multimodal Artificial Intelligence. The "i" stands for integrative multimodal learning. "CoDi: Any-to-Any Generation via Composable Diffusion". (**[arXiv 2023](https://arxiv.org/abs/2305.11846)**).

        - [WorkGPT](https://github.com/h2oai/h2ogpt) <img src="https://img.shields.io/github/stars/h2oai/h2ogpt?style=social"/> : WorkGPT is an agent framework in a similar fashion to AutoGPT or LangChain.

        - [h2oGPT](https://github.com/team-openpm/workgpt) <img src="https://img.shields.io/github/stars/team-openpm/workgpt?style=social"/> : h2oGPT is a large language model (LLM) fine-tuning framework and chatbot UI with document(s) question-answer capabilities. "h2oGPT: Democratizing Large Language Models". (**[arXiv 2023](https://arxiv.org/abs/2306.08161)**).

        - [LongLLaMA ](https://github.com/CStanKonrad/long_llama) <img src="https://img.shields.io/github/stars/CStanKonrad/long_llama?style=social"/> : LongLLaMA is a large language model capable of handling long contexts. It is based on OpenLLaMA and fine-tuned with the Focused Transformer (FoT) method.

        - [LLaMA-Adapter](https://github.com/OpenGVLab/LLaMA-Adapter) <img src="https://img.shields.io/github/stars/OpenGVLab/LLaMA-Adapter?style=social"/> : Fine-tuning LLaMA to follow Instructions within 1 Hour and 1.2M Parameters. LLaMA-Adapter: Efficient Fine-tuning of LLaMA 🚀

        - [DemoGPT](https://github.com/melih-unsal/DemoGPT) <img src="https://img.shields.io/github/stars/melih-unsal/DemoGPT?style=social"/> : Create 🦜️🔗 LangChain apps by just using prompts with the power of Llama 2 🌟 Star to support our work! | 只需使用句子即可创建 LangChain 应用程序。 给个star支持我们的工作吧！DemoGPT: Auto Gen-AI App Generator with the Power of Llama 2. ⚡ With just a prompt, you can create interactive Streamlit apps via 🦜️🔗 LangChain's transformative capabilities & Llama 2.⚡ [demogpt.io](https://www.demogpt.io/)

        - [Lamini](https://github.com/lamini-ai/lamini) <img src="https://img.shields.io/github/stars/lamini-ai/lamini?style=social"/> : Lamini: The LLM engine for rapidly customizing models 🦙

        - [xorbitsai/inference](https://github.com/xorbitsai/inference) <img src="https://img.shields.io/github/stars/xorbitsai/inference?style=social"/> : Xorbits Inference (Xinference) is a powerful and versatile library designed to serve LLMs, speech recognition models, and multimodal models, even on your laptop. It supports a variety of models compatible with GGML, such as llama, chatglm, baichuan, whisper, vicuna, orac, and many others.

        - [epfLLM/Megatron-LLM](https://github.com/epfLLM/Megatron-LLM) <img src="https://img.shields.io/github/stars/epfLLM/Megatron-LLM?style=social"/> : distributed trainer for LLMs.

        - [AmineDiro/cria](https://github.com/AmineDiro/cria) <img src="https://img.shields.io/github/stars/AmineDiro/cria?style=social"/> : OpenAI compatible API for serving LLAMA-2 model.

        - [Llama-2-Onnx](https://github.com/microsoft/Llama-2-Onnx) <img src="https://img.shields.io/github/stars/microsoft/Llama-2-Onnx?style=social"/> : Llama 2 Powered By ONNX.

        - [gpt-llm-trainer](https://github.com/mshumer/gpt-llm-trainer) <img src="https://img.shields.io/github/stars/mshumer/gpt-llm-trainer?style=social"/> : The goal of this project is to explore an experimental new pipeline to train a high-performing task-specific model. We try to abstract away all the complexity, so it's as easy as possible to go from idea -> performant fully-trained model.





        - [Qwen｜通义千问](https://github.com/QwenLM/Qwen) <img src="https://img.shields.io/github/stars/QwenLM/Qwen?style=social"/> : The official repo of Qwen (通义千问) chat & pretrained large language model proposed by Alibaba Cloud.

        - [Qwen1.5](https://github.com/QwenLM/Qwen1.5) <img src="https://img.shields.io/github/stars/QwenLM/Qwen1.5?style=social"/> : Qwen1.5 is the improved version of Qwen, the large language model series developed by Qwen team, Alibaba Cloud.

        - [ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B) <img src="https://img.shields.io/github/stars/THUDM/ChatGLM-6B?style=social"/> : ChatGLM-6B: An Open Bilingual Dialogue Language Model | 开源双语对话语言模型。 ChatGLM-6B 是一个开源的、支持中英双语的对话语言模型，基于 [General Language Model (GLM)](https://github.com/THUDM/GLM) 架构，具有 62 亿参数。 "GLM: General Language Model Pretraining with Autoregressive Blank Infilling". (**[ACL 2022](https://aclanthology.org/2022.acl-long.26/)**).  "GLM-130B: An Open Bilingual Pre-trained Model". (**[ICLR 2023](https://openreview.net/forum?id=-Aw0rrrPUF)**).

        - [ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B) <img src="https://img.shields.io/github/stars/THUDM/ChatGLM2-6B?style=social"/> : ChatGLM2-6B: An Open Bilingual Chat LLM | 开源双语对话语言模型。ChatGLM2-6B 是开源中英双语对话模型 ChatGLM-6B 的第二代版本，在保留了初代模型对话流畅、部署门槛较低等众多优秀特性的基础之上，ChatGLM2-6B 引入了更强大的性能、更强大的性能、更高效的推理、更开放的协议。

        - [ChatGLM3](https://github.com/THUDM/ChatGLM3) <img src="https://img.shields.io/github/stars/THUDM/ChatGLM3?style=social"/> : ChatGLM3 series: Open Bilingual Chat LLMs | 开源双语对话语言模型。

        - [InternLM｜书生·浦语](https://github.com/InternLM/InternLM) <img src="https://img.shields.io/github/stars/InternLM/InternLM?style=social"/> : Official release of InternLM2 7B and 20B base and chat models. 200K context support. [internlm.intern-ai.org.cn/](https://internlm.intern-ai.org.cn/)

        - [Baichuan-7B｜百川-7B](https://github.com/baichuan-inc/Baichuan-7B) <img src="https://img.shields.io/github/stars/baichuan-inc/Baichuan-7B?style=social"/> : A large-scale 7B pretraining language model developed by BaiChuan-Inc. Baichuan-7B 是由百川智能开发的一个开源可商用的大规模预训练语言模型。基于 Transformer 结构，在大约 1.2 万亿 tokens 上训练的 70 亿参数模型，支持中英双语，上下文窗口长度为 4096。在标准的中文和英文 benchmark（C-Eval/MMLU）上均取得同尺寸最好的效果。[huggingface.co/baichuan-inc/baichuan-7B](https://huggingface.co/baichuan-inc/Baichuan-7B)

        - [Baichuan-13B｜百川-13B](https://github.com/baichuan-inc/Baichuan-13B) <img src="https://img.shields.io/github/stars/baichuan-inc/Baichuan-13B?style=social"/> : A 13B large language model developed by Baichuan Intelligent Technology. Baichuan-13B 是由百川智能继 Baichuan-7B 之后开发的包含 130 亿参数的开源可商用的大规模语言模型，在权威的中文和英文 benchmark 上均取得同尺寸最好的效果。本次发布包含有预训练 (Baichuan-13B-Base) 和对齐 (Baichuan-13B-Chat) 两个版本。[huggingface.co/baichuan-inc/Baichuan-13B-Chat](https://huggingface.co/baichuan-inc/Baichuan-13B-Chat)

        - [Baichuan2](https://github.com/baichuan-inc/Baichuan2) <img src="https://img.shields.io/github/stars/baichuan-inc/Baichuan2?style=social"/> : A series of large language models developed by Baichuan Intelligent Technology. Baichuan 2 是百川智能推出的新一代开源大语言模型，采用 2.6 万亿 Tokens 的高质量语料训练。Baichuan 2 在多个权威的中文、英文和多语言的通用、领域 benchmark 上取得同尺寸最佳的效果。本次发布包含有 7B、13B 的 Base 和 Chat 版本，并提供了 Chat 版本的 4bits 量化。[huggingface.co/baichuan-inc](https://huggingface.co/baichuan-inc). "Baichuan 2: Open Large-scale Language Models". (**[arXiv 2023](https://arxiv.org/abs/2309.10305)**).


        - [MOSS](https://github.com/OpenLMLab/MOSS) <img src="https://img.shields.io/github/stars/OpenLMLab/MOSS?style=social"/> : An open-source tool-augmented conversational language model from Fudan University. MOSS是一个支持中英双语和多种插件的开源对话语言模型，moss-moon系列模型具有160亿参数，在FP16精度下可在单张A100/A800或两张3090显卡运行，在INT4/8精度下可在单张3090显卡运行。MOSS基座语言模型在约七千亿中英文以及代码单词上预训练得到，后续经过对话指令微调、插件增强学习和人类偏好训练具备多轮对话能力及使用多种插件的能力。[txsun1997.github.io/blogs/moss.html](https://txsun1997.github.io/blogs/moss.html)

        - [BayLing｜百聆](https://github.com/ictnlp/BayLing) <img src="https://img.shields.io/github/stars/OpenLMLab/MOSS?style=social"/> : “百聆”是一个具有增强的语言对齐的英语/中文大语言模型，具有优越的英语/中文能力，在多项测试中取得ChatGPT 90%的性能。BayLing is an English/Chinese LLM equipped with advanced language alignment, showing superior capability in English/Chinese generation, instruction following and multi-turn interaction. [nlp.ict.ac.cn/bayling](http://nlp.ict.ac.cn/bayling). "BayLing: Bridging Cross-lingual Alignment and Instruction Following through Interactive Translation for Large Language Models". (**[arXiv 2023](https://arxiv.org/abs/2306.10968)**).

        - [FlagAI｜悟道·天鹰（Aquila）](https://github.com/FlagAI-Open/FlagAI) <img src="https://img.shields.io/github/stars/FlagAI-Open/FlagAI?style=social"/> : FlagAI (Fast LArge-scale General AI models) is a fast, easy-to-use and extensible toolkit for large-scale model. Our goal is to support training, fine-tuning, and deployment of large-scale models on various downstream tasks with multi-modality.


        - [YuLan-Chat｜玉兰](https://github.com/RUC-GSAI/YuLan-Chat/) <img src="https://img.shields.io/github/stars/RUC-GSAI/YuLan-Chat?style=social"/> : YuLan-Chat models are chat-based large language models, which are developed by the researchers in GSAI, Renmin University of China (YuLan, which represents Yulan Magnolia, is the campus flower of Renmin University of China). The newest version is developed by continually-pretraining and instruction-tuning [LLaMA-2](https://github.com/facebookresearch/llama) with high-quality English and Chinese data. YuLan-Chat系列模型是中国人民大学高瓴人工智能学院师生共同开发的支持聊天的大语言模型（名字"玉兰"取自中国人民大学校花）。 最新版本基于LLaMA-2进行了中英文双语的继续预训练和指令微调。


        - [智海-录问](https://github.com/zhihaiLLM/wisdomInterrogatory) <img src="https://img.shields.io/github/stars/zhihaiLLM/wisdomInterrogatory?style=social"/> : 智海-录问(wisdomInterrogatory)是由浙江大学、阿里巴巴达摩院以及华院计算三家单位共同设计研发的法律大模型。核心思想：以“普法共享和司法效能提升”为目标，从推动法律智能化体系入司法实践、数字化案例建设、虚拟法律咨询服务赋能等方面提供支持，形成数字化和智能化的司法基座能力。

        - [活字](https://github.com/HIT-SCIR/huozi) <img src="https://img.shields.io/github/stars/HIT-SCIR/huozi?style=social"/> : 活字是由哈工大自然语言处理研究所多位老师和学生参与开发的一个开源可商用的大规模预训练语言模型。 该模型基于 Bloom 结构的70 亿参数模型，支持中英双语，上下文窗口长度为 2048。 在标准的中文和英文基准以及主观评测上均取得同尺寸中优异的结果。

        - [MiLM-6B](https://github.com/XiaoMi/MiLM-6B) <img src="https://img.shields.io/github/stars/XiaoMi/MiLM-6B?style=social"/> : MiLM-6B 是由小米开发的一个大规模预训练语言模型，参数规模为64亿。在 C-Eval 和 CMMLU 上均取得同尺寸最好的效果。

        - [Chinese LLaMA and Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca) <img src="https://img.shields.io/github/stars/ymcui/Chinese-LLaMA-Alpaca?style=social"/> : 中文LLaMA&Alpaca大语言模型+本地CPU/GPU训练部署 (Chinese LLaMA & Alpaca LLMs)。"Efficient and Effective Text Encoding for Chinese LLaMA and Alpaca". (**[arXiv 2023](https://arxiv.org/abs/2304.08177)**).

        - [Chinese-LLaMA-Alpaca-2](https://github.com/ymcui/Chinese-LLaMA-Alpaca-2) <img src="https://img.shields.io/github/stars/ymcui/Chinese-LLaMA-Alpaca-2?style=social"/> : 中文 LLaMA-2 & Alpaca-2 大模型二期项目 (Chinese LLaMA-2 & Alpaca-2 LLMs).

        - [FlagAlpha/Llama2-Chinese](https://github.com/FlagAlpha/Llama2-Chinese) <img src="https://img.shields.io/github/stars/FlagAlpha/Llama2-Chinese?style=social"/> : Llama中文社区，最好的中文Llama大模型，完全开源可商用。

        - [michael-wzhu/Chinese-LlaMA2](https://github.com/michael-wzhu/Chinese-LlaMA2) <img src="https://img.shields.io/github/stars/michael-wzhu/Chinese-LlaMA2?style=social"/> : Repo for adapting Meta LlaMA2 in Chinese! META最新发布的LlaMA2的汉化版！ （完全开源可商用）

        - [CPM-Bee](https://github.com/OpenBMB/CPM-Bee) <img src="https://img.shields.io/github/stars/OpenBMB/CPM-Bee?style=social"/> : CPM-Bee是一个完全开源、允许商用的百亿参数中英文基座模型，也是[CPM-Live](https://live.openbmb.org/)训练的第二个里程碑。

        - [PandaLM](https://github.com/WeOpenML/PandaLM) <img src="https://img.shields.io/github/stars/WeOpenML/PandaLM?style=social"/> : PandaLM: Reproducible and Automated Language Model Assessment.

        - [SpeechGPT](https://github.com/0nutation/SpeechGPT) <img src="https://img.shields.io/github/stars/0nutation/SpeechGPT?style=social"/> : "SpeechGPT: Empowering Large Language Models with Intrinsic Cross-Modal Conversational Abilities". (**[arXiv 2023](https://arxiv.org/abs/2305.11000)**).

        - [GPT2-Chinese](https://github.com/Morizeyao/GPT2-Chinese) <img src="https://img.shields.io/github/stars/Morizeyao/GPT2-Chinese?style=social"/> : Chinese version of GPT2 training code, using BERT tokenizer.

        - [Chinese-Tiny-LLM](https://github.com/Chinese-Tiny-LLM/Chinese-Tiny-LLM) <img src="https://img.shields.io/github/stars/Chinese-Tiny-LLM/Chinese-Tiny-LLM?style=social"/> : "Chinese Tiny LLM: Pretraining a Chinese-Centric Large Language Model". (**[arXiv 2024](https://arxiv.org/abs/2404.04167)**).

        - [潘多拉 (Pandora)](https://github.com/pengzhile/pandora) <img src="https://img.shields.io/github/stars/pengzhile/pandora?style=social"/> : 潘多拉，一个让你呼吸顺畅的ChatGPT。Pandora, a ChatGPT that helps you breathe smoothly.

        - [百度-文心大模型](https://wenxin.baidu.com/) : 百度全新一代知识增强大语言模型，文心大模型家族的新成员，能够与人对话互动，回答问题，协助创作，高效便捷地帮助人们获取信息、知识和灵感。

        - [百度智能云-千帆大模型](https://cloud.baidu.com/product/wenxinworkshop) : 百度智能云千帆大模型平台一站式企业级大模型平台，提供先进的生成式AI生产及应用全流程开发工具链。

        - [华为云-盘古大模型](https://www.huaweicloud.com/product/pangu.html) : 盘古大模型致力于深耕行业，打造金融、政务、制造、矿山、气象、铁路等领域行业大模型和能力集，将行业知识know-how与大模型能力相结合，重塑千行百业，成为各组织、企业、个人的专家助手。"Accurate medium-range global weather forecasting with 3D neural networks". (**[Nature 2023](https://www.nature.com/articles/s41586-023-06185-3)**).

        - [商汤科技-日日新SenseNova](https://techday.sensetime.com/?utm_source=baidu-sem-pc&utm_medium=cpc&utm_campaign=PC-%E6%8A%80%E6%9C%AF%E4%BA%A4%E6%B5%81%E6%97%A5-%E4%BA%A7%E5%93%81%E8%AF%8D-%E6%97%A5%E6%97%A5%E6%96%B0&utm_content=%E6%97%A5%E6%97%A5%E6%96%B0&utm_term=%E6%97%A5%E6%97%A5%E6%96%B0SenseNova&e_creative=73937788324&e_keywordid=594802524403) : 日日新（SenseNova），是商汤科技宣布推出的大模型体系，包括自然语言处理模型“商量”（SenseChat）、文生图模型“秒画”和数字人视频生成平台“如影”（SenseAvatar）等。

        - [科大讯飞-星火认知大模型](https://xinghuo.xfyun.cn/) : 新一代认知智能大模型，拥有跨领域知识和语言理解能力，能够基于自然对话方式理解与执行任务。

        - [字节跳动-豆包](https://www.doubao.com/) : 豆包。

        - [CrazyBoyM/llama3-Chinese-chat](https://github.com/CrazyBoyM/llama3-Chinese-chat) <img src="https://img.shields.io/github/stars/CrazyBoyM/llama3-Chinese-chat?style=social"/> : Llama3 中文版。








      - ##### Vision Foundation Model
        ###### 视觉大模型（VFM）

        - [Visual ChatGPT](https://github.com/microsoft/visual-chatgpt) <img src="https://img.shields.io/github/stars/microsoft/visual-chatgpt?style=social"/> : Visual ChatGPT connects ChatGPT and a series of Visual Foundation Models to enable sending and receiving images during chatting. "Visual ChatGPT: Talking, Drawing and Editing with Visual Foundation Models". (**[arXiv 2023](https://arxiv.org/abs/2303.04671)**).

        - [InternImage](https://github.com/OpenGVLab/InternImage) <img src="https://img.shields.io/github/stars/OpenGVLab/InternImage?style=social"/> : "InternImage: Exploring Large-Scale Vision Foundation Models with Deformable Convolutions". (**[CVPR 2023](https://arxiv.org/abs/2211.05778)**).

        - [GLIP](https://github.com/microsoft/GLIP) <img src="https://img.shields.io/github/stars/microsoft/GLIP?style=social"/> : "Grounded Language-Image Pre-training". (**[CVPR 2022](https://arxiv.org/abs/2112.03857)**).

        - [GLIPv2](https://github.com/microsoft/GLIP) <img src="https://img.shields.io/github/stars/microsoft/GLIP?style=social"/> : "GLIPv2: Unifying Localization and Vision-Language Understanding". (**[arXiv 2022](https://arxiv.org/abs/2206.05836)**).

        - [DINO](https://github.com/IDEA-Research/DINO) <img src="https://img.shields.io/github/stars/IDEA-Research/DINO?style=social"/> : "DINO: DETR with Improved DeNoising Anchor Boxes for End-to-End Object Detection". (**[ICLR 2023](https://arxiv.org/abs/2203.03605)**).

        - [DINOv2](https://github.com/facebookresearch/dinov2) <img src="https://img.shields.io/github/stars/facebookresearch/dinov2?style=social"/> : "DINOv2: Learning Robust Visual Features without Supervision". (**[arXiv 2023](https://arxiv.org/abs/2304.07193)**).

        - [Grounding DINO](https://github.com/IDEA-Research/GroundingDINO) <img src="https://img.shields.io/github/stars/IDEA-Research/GroundingDINO?style=social"/> : "Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection". (**[arXiv 2023](https://arxiv.org/abs/2303.05499)**). "知乎「三分钟热度」《[十分钟解读Grounding DINO-根据文字提示检测任意目标](https://zhuanlan.zhihu.com/p/627646794)》"。

        - [SAM](https://github.com/facebookresearch/segment-anything) <img src="https://img.shields.io/github/stars/facebookresearch/segment-anything?style=social"/> : The repository provides code for running inference with the Segment Anything Model (SAM), links for downloading the trained model checkpoints, and example notebooks that show how to use the model. "Segment Anything". (**[arXiv 2023](https://arxiv.org/abs/2304.02643)**).

        - [Grounded-SAM](https://github.com/IDEA-Research/Grounded-Segment-Anything) <img src="https://img.shields.io/github/stars/IDEA-Research/Grounded-Segment-Anything?style=social"/> : Marrying Grounding DINO with Segment Anything & Stable Diffusion & Tag2Text & BLIP & Whisper & ChatBot - Automatically Detect , Segment and Generate Anything with Image, Text, and Audio Inputs. We plan to create a very interesting demo by combining [Grounding DINO](https://github.com/IDEA-Research/GroundingDINO) and [Segment Anything](https://github.com/facebookresearch/segment-anything) which aims to detect and segment Anything with text inputs!

        - [SEEM](https://github.com/UX-Decoder/Segment-Everything-Everywhere-All-At-Once) <img src="https://img.shields.io/github/stars/UX-Decoder/Segment-Everything-Everywhere-All-At-Once?style=social"/> : We introduce SEEM that can Segment Everything Everywhere with Multi-modal prompts all at once. SEEM allows users to easily segment an image using prompts of different types including visual prompts (points, marks, boxes, scribbles and image segments) and language prompts (text and audio), etc. It can also work with any combinations of prompts or generalize to custom prompts! "Segment Everything Everywhere All at Once". (**[arXiv 2023](https://arxiv.org/abs/2304.06718)**).

        - [SAM3D](https://github.com/DYZhang09/SAM3D) <img src="https://img.shields.io/github/stars/DYZhang09/SAM3D?style=social"/> : "SAM3D: Zero-Shot 3D Object Detection via [Segment Anything](https://github.com/facebookresearch/segment-anything) Model". (**[arXiv 2023](https://arxiv.org/abs/2306.02245)**).

        - [ImageBind](https://github.com/facebookresearch/ImageBind) <img src="https://img.shields.io/github/stars/facebookresearch/ImageBind?style=social"/> : "ImageBind: One Embedding Space To Bind Them All". (**[CVPR 2023](https://arxiv.org/abs/2305.05665)**).

        - [Track-Anything](https://github.com/gaomingqi/Track-Anything) <img src="https://img.shields.io/github/stars/gaomingqi/Track-Anything?style=social"/> : Track-Anything is a flexible and interactive tool for video object tracking and segmentation, based on Segment Anything, XMem, and E2FGVI. "Track Anything: Segment Anything Meets Videos". (**[arXiv 2023](https://arxiv.org/abs/2304.11968)**).

        - [qianqianwang68/omnimotion](https://github.com/qianqianwang68/omnimotion) <img src="https://img.shields.io/github/stars/qianqianwang68/omnimotion?style=social"/> : "Tracking Everything Everywhere All at Once". (**[arXiv 2023](https://arxiv.org/abs/2306.05422)**).

        - [LLaVA](https://github.com/haotian-liu/LLaVA) <img src="https://img.shields.io/github/stars/haotian-liu/LLaVA?style=social"/> : 🌋 LLaVA: Large Language and Vision Assistant. Visual instruction tuning towards large language and vision models with GPT-4 level capabilities. [llava.hliu.cc](https://llava.hliu.cc/). "Visual Instruction Tuning". (**[arXiv 2023](https://arxiv.org/abs/2304.08485)**).

        - [M3I-Pretraining](https://github.com/OpenGVLab/M3I-Pretraining) <img src="https://img.shields.io/github/stars/OpenGVLab/M3I-Pretraining?style=social"/> : "Towards All-in-one Pre-training via Maximizing Multi-modal Mutual Information". (**[arXiv 2022](https://arxiv.org/abs/2211.09807)**).

        - [BEVFormer](https://github.com/fundamentalvision/BEVFormer) <img src="https://img.shields.io/github/stars/fundamentalvision/BEVFormer?style=social"/> : BEVFormer: a Cutting-edge Baseline for Camera-based Detection. "BEVFormer: Learning Bird's-Eye-View Representation from Multi-Camera Images via Spatiotemporal Transformers". (**[arXiv 2022](https://arxiv.org/abs/2203.17270)**).

        - [Uni-Perceiver](https://github.com/fundamentalvision/Uni-Perceiver) <img src="https://img.shields.io/github/stars/fundamentalvision/Uni-Perceiver?style=social"/> : "Uni-Perceiver: Pre-training Unified Architecture for Generic Perception for Zero-shot and Few-shot Tasks". (**[CVPR 2022](https://openaccess.thecvf.com/content/CVPR2022/html/Zhu_Uni-Perceiver_Pre-Training_Unified_Architecture_for_Generic_Perception_for_Zero-Shot_and_CVPR_2022_paper.html)**).

        - [AnyLabeling](https://github.com/vietanhdev/anylabeling) <img src="https://img.shields.io/github/stars/vietanhdev/anylabeling?style=social"/> : 🌟 AnyLabeling 🌟. Effortless data labeling with AI support from YOLO and Segment Anything! Effortless data labeling with AI support from YOLO and Segment Anything!

        - [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) <img src="https://img.shields.io/github/stars/CVHub520/X-AnyLabeling?style=social"/> : 💫 X-AnyLabeling 💫. Effortless data labeling with AI support from Segment Anything and other awesome models!

        - [Label Anything](https://github.com/open-mmlab/playground/tree/main/label_anything) <img src="https://img.shields.io/github/stars/open-mmlab/playground?style=social"/> : OpenMMLab PlayGround: Semi-Automated Annotation with Label-Studio and SAM.

        - [RevCol](https://github.com/megvii-research/RevCol) <img src="https://img.shields.io/github/stars/megvii-research/RevCol?style=social"/> : "Reversible Column Networks". (**[arXiv 2023](https://arxiv.org/abs/2212.11696)**).

        - [Macaw-LLM](https://github.com/lyuchenyang/Macaw-LLM) <img src="https://img.shields.io/github/stars/lyuchenyang/Macaw-LLM?style=social"/> : Macaw-LLM: Multi-Modal Language Modeling with Image, Audio, Video, and Text Integration.

        - [SAM-PT](https://github.com/SysCV/sam-pt) <img src="https://img.shields.io/github/stars/SysCV/sam-pt?style=social"/> : SAM-PT: Extending SAM to zero-shot video segmentation with point-based tracking. "Segment Anything Meets Point Tracking". (**[arXiv 2023](https://arxiv.org/abs/2307.01197)**).

        - [Video-LLaMA](https://github.com/DAMO-NLP-SG/Video-LLaMA) <img src="https://img.shields.io/github/stars/DAMO-NLP-SG/Video-LLaMA?style=social"/> : "Video-LLaMA: An Instruction-tuned Audio-Visual Language Model for Video Understanding". (**[arXiv 2023](https://arxiv.org/abs/2306.02858)**).

        - [MobileSAM](https://github.com/ChaoningZhang/MobileSAM) <img src="https://img.shields.io/github/stars/ChaoningZhang/MobileSAM?style=social"/> : "Faster Segment Anything: Towards Lightweight SAM for Mobile Applications". (**[arXiv 2023](https://arxiv.org/abs/2306.14289)**).

        - [BuboGPT](https://github.com/magic-research/bubogpt) <img src="https://img.shields.io/github/stars/magic-research/bubogpt?style=social"/> : "BuboGPT: Enabling Visual Grounding in Multi-Modal LLMs". (**[arXiv 2023](https://arxiv.org/abs/2307.08581)**).









      - ##### AI Generated Content
        ###### 人工智能生成内容（AIGC）

        - [Sora](https://openai.com/sora) : Sora is an AI model that can create realistic and imaginative scenes from text instructions.

        - [Open Sora Plan](https://github.com/PKU-YuanGroup/Open-Sora-Plan) <img src="https://img.shields.io/github/stars/PKU-YuanGroup/Open-Sora-Plan?style=social"/> : This project aim to reproducing [Sora](https://openai.com/sora) (Open AI T2V model), but we only have limited resource. We deeply wish the all open source community can contribute to this project. 本项目希望通过开源社区的力量复现Sora，由北大-兔展AIGC联合实验室共同发起，当前我们资源有限仅搭建了基础架构，无法进行完整训练，希望通过开源社区逐步增加模块并筹集资源进行训练，当前版本离目标差距巨大，仍需持续完善和快速迭代，欢迎Pull request！！！[Project Page](https://pku-yuangroup.github.io/Open-Sora-Plan/) [中文主页](https://pku-yuangroup.github.io/Open-Sora-Plan/blog_cn.html)

        - [Mini Sora](https://github.com/mini-sora/minisora) <img src="https://img.shields.io/github/stars/mini-sora/minisora?style=social"/> : The Mini Sora project aims to explore the implementation path and future development direction of Sora.

        - [EMO](https://github.com/HumanAIGC/EMO) <img src="https://img.shields.io/github/stars/HumanAIGC/EMO?style=social"/> : "EMO: Emote Portrait Alive - Generating Expressive Portrait Videos with Audio2Video Diffusion Model under Weak Conditions". (**[arXiv 2024](https://arxiv.org/abs/2402.17485)**).

        - [Stable Diffusion](https://github.com/CompVis/stable-diffusion) <img src="https://img.shields.io/github/stars/CompVis/stable-diffusion?style=social"/> : Stable Diffusion is a latent text-to-image diffusion model. Stable Diffusion was made possible thanks to a collaboration with [Stability AI](https://stability.ai/) and [Runway](https://runwayml.com/) and builds upon our previous work "High-Resolution Image Synthesis with Latent Diffusion Models". (**[CVPR 2022](https://openaccess.thecvf.com/content/CVPR2022/html/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.html)**).

        - [Stable Diffusion Version 2](https://github.com/Stability-AI/stablediffusion) <img src="https://img.shields.io/github/stars/Stability-AI/stablediffusion?style=social"/> : This repository contains [Stable Diffusion](https://github.com/CompVis/stable-diffusion) models trained from scratch and will be continuously updated with new checkpoints. "High-Resolution Image Synthesis with Latent Diffusion Models". (**[CVPR 2022](https://openaccess.thecvf.com/content/CVPR2022/html/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.html)**).

        - [StableStudio](https://github.com/Stability-AI/StableStudio) <img src="https://img.shields.io/github/stars/Stability-AI/StableStudio?style=social"/> : StableStudio by [Stability AI](https://stability.ai/). 👋 Welcome to the community repository for StableStudio, the open-source version of [DreamStudio](https://dreamstudio.ai/).

        - [AudioCraft](https://github.com/facebookresearch/audiocraft) <img src="https://img.shields.io/github/stars/facebookresearch/audiocraft?style=social"/> : Audiocraft is a library for audio processing and generation with deep learning. It features the state-of-the-art EnCodec audio compressor / tokenizer, along with MusicGen, a simple and controllable music generation LM with textual and melodic conditioning.

        - [InvokeAI](https://github.com/invoke-ai/InvokeAI) <img src="https://img.shields.io/github/stars/invoke-ai/InvokeAI?style=social"/> : Invoke AI - Generative AI for Professional Creatives. Professional Creative Tools for Stable Diffusion, Custom-Trained Models, and more. [invoke-ai.github.io/InvokeAI/](https://invoke-ai.github.io/InvokeAI/)

        - [DragGAN](https://github.com/XingangPan/DragGAN) <img src="https://img.shields.io/github/stars/XingangPan/DragGAN?style=social"/> : "Stable Diffusion Training with MosaicML. This repo contains code used to train your own Stable Diffusion model on your own data". (**[SIGGRAPH 2023](https://vcai.mpi-inf.mpg.de/projects/DragGAN/)**).

        - [AudioGPT](https://github.com/AIGC-Audio/AudioGPT) <img src="https://img.shields.io/github/stars/AIGC-Audio/AudioGPT?style=social"/> : AudioGPT: Understanding and Generating Speech, Music, Sound, and Talking Head.

        - [PandasAI](https://github.com/gventuri/pandas-ai) <img src="https://img.shields.io/github/stars/gventuri/pandas-ai?style=social"/> : Pandas AI is a Python library that adds generative artificial intelligence capabilities to Pandas, the popular data analysis and manipulation tool. It is designed to be used in conjunction with Pandas, and is not a replacement for it.

        - [mosaicml/diffusion](https://github.com/mosaicml/diffusion) <img src="https://img.shields.io/github/stars/mosaicml/diffusion?style=social"/> : Stable Diffusion Training with MosaicML. This repo contains code used to train your own Stable Diffusion model on your own data.

        - [VisorGPT](https://github.com/Sierkinhane/VisorGPT) <img src="https://img.shields.io/github/stars/Sierkinhane/VisorGPT?style=social"/> : Customize spatial layouts for conditional image synthesis models, e.g., ControlNet, using GPT. "VisorGPT: Learning Visual Prior via Generative Pre-Training". (**[arXiv 2023](https://arxiv.org/abs/2305.13777)**).

        - [ControlNet](https://github.com/lllyasviel/ControlNet) <img src="https://img.shields.io/github/stars/lllyasviel/ControlNet?style=social"/> : Let us control diffusion models! "Adding Conditional Control to Text-to-Image Diffusion Models". (**[arXiv 2023](https://arxiv.org/abs/2302.05543)**).

        - [Fooocus](https://github.com/lllyasviel/Fooocus) <img src="https://img.shields.io/github/stars/lllyasviel/Fooocus?style=social"/> : Fooocus is an image generating software. Fooocus is a rethinking of Stable Diffusion and Midjourney’s designs. "微信公众号「GitHubStore」《[Fooocus : 集Stable Diffusion 和 Midjourney 优点于一身的开源AI绘图软件](https://mp.weixin.qq.com/s/adyXek6xcz5aOPAGqZBrvg)》"。

        - [MindDiffuser](https://github.com/ReedOnePeck/MindDiffuser) <img src="https://img.shields.io/github/stars/ReedOnePeck/MindDiffuser?style=social"/> : "MindDiffuser: Controlled Image Reconstruction from Human Brain Activity with Semantic and Structural Diffusion". (**[arXiv 2023](https://arxiv.org/abs/2308.04249)**).



        - [Midjourney](https://www.midjourney.com/) : Midjourney is an independent research lab exploring new mediums of thought and expanding the imaginative powers of the human species.

        - [DreamStudio](https://dreamstudio.ai/) : Effortless image generation for creators with big dreams.

        - [Firefly](https://www.adobe.com/sensei/generative-ai/firefly.html) : Adobe Firefly: Experiment, imagine, and make an infinite range of creations with Firefly, a family of creative generative AI models coming to Adobe products.

        - [Jasper](https://www.jasper.ai/) : Meet Jasper. On-brand AI content wherever you create.

        - [Copy.ai](https://www.copy.ai/) : Whatever you want to ask, our chat has the answers.

        - [Peppertype.ai](https://www.peppercontent.io/peppertype-ai/) : Leverage the AI-powered platform to ideate, create, distribute, and measure your content and prove your content marketing ROI.

        - [ChatPPT](https://chat-ppt.com/) : ChatPPT来袭命令式一键生成PPT。




    - #### Application Development Platform
      ##### 应用程序开发平台

        - [LangChain](https://github.com/langchain-ai/langchain) <img src="https://img.shields.io/github/stars/hwchase17/langchain?style=social"/> :  🦜️🔗 LangChain. ⚡ Building applications with LLMs through composability ⚡ [python.langchain.com](https://python.langchain.com/docs/get_started/introduction.html)

        - [Dify](https://github.com/langgenius/dify) <img src="https://img.shields.io/github/stars/langgenius/dify?style=social"/> : An Open-Source Assistants API and GPTs alternative. Dify.AI is an LLM application development platform. It integrates the concepts of Backend as a Service and LLMOps, covering the core tech stack required for building generative AI-native applications, including a built-in RAG engine. [dify.ai](https://dify.ai/)

        - [AutoChain](https://github.com/Forethought-Technologies/AutoChain) <img src="https://img.shields.io/github/stars/Forethought-Technologies/AutoChain?style=social"/> :  AutoChain: Build lightweight, extensible, and testable LLM Agents. [autochain.forethought.ai](https://autochain.forethought.ai/)

        - [Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT) <img src="https://img.shields.io/github/stars/Significant-Gravitas/Auto-GPT?style=social"/> : Auto-GPT: An Autonomous GPT-4 Experiment. Auto-GPT is an experimental open-source application showcasing the capabilities of the GPT-4 language model. This program, driven by GPT-4, chains together LLM "thoughts", to autonomously achieve whatever goal you set. As one of the first examples of GPT-4 running fully autonomously, Auto-GPT pushes the boundaries of what is possible with AI. [agpt.co](https://news.agpt.co/)

        - [LiteChain](https://github.com/rogeriochaves/litechain) <img src="https://img.shields.io/github/stars/rogeriochaves/litechain?style=social"/> : Build robust LLM applications with true composability 🔗. [rogeriochaves.github.io/litechain/](https://rogeriochaves.github.io/litechain/)

        - [Open-Assistant](https://github.com/LAION-AI/Open-Assistant) <img src="https://img.shields.io/github/stars/LAION-AI/Open-Assistant?style=social"/> : OpenAssistant is a chat-based assistant that understands tasks, can interact with third-party systems, and retrieve information dynamically to do so. [open-assistant.io](https://open-assistant.io/)


    - #### Fine-Tuning Framework
      ##### 微调框架

        - [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) <img src="https://img.shields.io/github/stars/hiyouga/LLaMA-Factory?style=social"/> : Unify Efficient Fine-Tuning of 100+ LLMs. Fine-tuning a large language model can be easy as...



    - #### RAG Framework
      ##### 检索增强生成框架

        - [LlamaIndex](https://github.com/run-llama/llama_index) <img src="https://img.shields.io/github/stars/run-llama/llama_index?style=social"/> : LlamaIndex is a data framework for your LLM applications. [docs.llamaindex.ai](https://docs.llamaindex.ai/)

        - [Embedchain](https://github.com/embedchain/embedchain) <img src="https://img.shields.io/github/stars/embedchain/embedchain?style=social"/> : The Open Source RAG framework. [docs.embedchain.ai](https://docs.embedchain.ai/)

        - [QAnything](https://github.com/netease-youdao/QAnything) <img src="https://img.shields.io/github/stars/netease-youdao/QAnything?style=social"/> : Question and Answer based on Anything. [qanything.ai](https://qanything.ai/)

        - [R2R](https://github.com/SciPhi-AI/R2R) <img src="https://img.shields.io/github/stars/SciPhi-AI/R2R?style=social"/> : A framework for rapid development and deployment of production-ready RAG systems. [docs.sciphi.ai](https://docs.sciphi.ai/)

        - [langchain-ai/rag-from-scratch](https://github.com/langchain-ai/rag-from-scratch) <img src="https://img.shields.io/github/stars/langchain-ai/rag-from-scratch?style=social"/> : Retrieval augmented generation (RAG) comes is a general methodology for connecting LLMs with external data sources. These notebooks accompany a video series will build up an understanding of RAG from scratch, starting with the basics of indexing, retrieval, and generation.


    - #### LLM Inference Framework
      ##### 大语言模型推理框架


        - ##### LLM Inference Benchmark

            - [ninehills/llm-inference-benchmark](https://github.com/ninehills/llm-inference-benchmark) <img src="https://img.shields.io/github/stars/ninehills/llm-inference-benchmark?style=social"/> : LLM Inference benchmark.


        - ##### LLM Deployment Engine

            - [vllm-project/vllm](https://github.com/vllm-project/vllm) <img src="https://img.shields.io/github/stars/vllm-project/vllm?style=social"/> : A high-throughput and memory-efficient inference and serving engine for LLMs. [vllm.readthedocs.io](https://vllm.readthedocs.io/en/latest/)


            - [MLC LLM](https://github.com/mlc-ai/mlc-llm) <img src="https://img.shields.io/github/stars/mlc-ai/mlc-llm?style=social"/> : Enable everyone to develop, optimize and deploy AI models natively on everyone's devices. [mlc.ai/mlc-llm](https://mlc.ai/mlc-llm/)

            - [Lamini](https://github.com/lamini-ai/lamini) <img src="https://img.shields.io/github/stars/lamini-ai/lamini?style=social"/> : Lamini: The LLM engine for rapidly customizing models 🦙.

            - [datawhalechina/self-llm](https://github.com/datawhalechina/self-llm) <img src="https://img.shields.io/github/stars/datawhalechina/self-llm?style=social"/> :  《开源大模型食用指南》基于Linux环境快速部署开源大模型，更适合中国宝宝的部署教程。


        - ##### C Implementation

            - [llm.c](https://github.com/karpathy/llm.c) <img src="https://img.shields.io/github/stars/karpathy/llm.c?style=social"/> : LLM training in simple, pure C/CUDA. There is no need for 245MB of PyTorch or 107MB of cPython. For example, training GPT-2 (CPU, fp32) is ~1,000 lines of clean code in a single file. It compiles and runs instantly, and exactly matches the PyTorch reference implementation.

            - [llama2.c](https://github.com/karpathy/llama2.c) <img src="https://img.shields.io/github/stars/karpathy/llama2.c?style=social"/> : Inference Llama 2 in one file of pure C. Train the Llama 2 LLM architecture in PyTorch then inference it with one simple 700-line C file (run.c).


        - ##### CPP Implementation

            - [TensorRT](https://github.com/NVIDIA/TensorRT) <img src="https://img.shields.io/github/stars/NVIDIA/TensorRT?style=social"/> : NVIDIA® TensorRT™ is an SDK for high-performance deep learning inference on NVIDIA GPUs. This repository contains the open source components of TensorRT. [developer.nvidia.com/tensorrt](https://developer.nvidia.com/tensorrt)

            - [TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) <img src="https://img.shields.io/github/stars/NVIDIA/TensorRT-LLM?style=social"/> : TensorRT-LLM provides users with an easy-to-use Python API to define Large Language Models (LLMs) and build TensorRT engines that contain state-of-the-art optimizations to perform inference efficiently on NVIDIA GPUs. TensorRT-LLM also contains components to create Python and C++ runtimes that execute those TensorRT engines. [nvidia.github.io/TensorRT-LLM](https://nvidia.github.io/TensorRT-LLM)

            - [gemma.cpp](https://github.com/google/gemma.cpp) <img src="https://img.shields.io/github/stars/google/gemma.cpp?style=social"/> :  gemma.cpp is a lightweight, standalone C++ inference engine for the Gemma foundation models from Google.

            - [llama.cpp](https://github.com/ggerganov/llama.cpp) <img src="https://img.shields.io/github/stars/ggerganov/llama.cpp?style=social"/> : Inference of [LLaMA](https://github.com/facebookresearch/llama) model in pure C/C++.

            - [whisper.cpp](https://github.com/ggerganov/whisper.cpp) <img src="https://img.shields.io/github/stars/ggerganov/whisper.cpp?style=social"/> : High-performance inference of [OpenAI's Whisper](https://github.com/openai/whisper) automatic speech recognition (ASR) model.

            - [ChatGLM.cpp](https://github.com/li-plus/chatglm.cpp) <img src="https://img.shields.io/github/stars/li-plus/chatglm.cpp?style=social"/> : C++ implementation of [ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B) and [ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B).

            - [MegEngine/InferLLM](https://github.com/MegEngine/InferLLM) <img src="https://img.shields.io/github/stars/MegEngine/InferLLM?style=social"/> : InferLLM is a lightweight LLM model inference framework that mainly references and borrows from the llama.cpp project.

            - [DeployAI/nndeploy](https://github.com/DeployAI/nndeploy) <img src="https://img.shields.io/github/stars/DeployAI/nndeploy?style=social"/> : nndeploy是一款模型端到端部署框架。以多端推理以及基于有向无环图模型部署为内核，致力为用户提供跨平台、简单易用、高性能的模型部署体验。[nndeploy-zh.readthedocs.io/zh/latest/](https://nndeploy-zh.readthedocs.io/zh/latest/)

            - [zjhellofss/KuiperInfer (自制深度学习推理框架)](https://github.com/zjhellofss/KuiperInfer) <img src="https://img.shields.io/github/stars/zjhellofss/KuiperInfer?style=social"/> :  带你从零实现一个高性能的深度学习推理库，支持llama 、Unet、Yolov5、Resnet等模型的推理。Implement a high-performance deep learning inference library step by step.

            - [skeskinen/llama-lite](https://github.com/skeskinen/llama-lite) <img src="https://img.shields.io/github/stars/skeskinen/llama-lite?style=social"/> : Embeddings focused small version of Llama NLP model.

            - [Const-me/Whisper](https://github.com/Const-me/Whisper) <img src="https://img.shields.io/github/stars/Const-me/Whisper?style=social"/> : High-performance GPGPU inference of OpenAI's Whisper automatic speech recognition (ASR) model.

            - [wangzhaode/ChatGLM-MNN](https://github.com/wangzhaode/ChatGLM-MNN) <img src="https://img.shields.io/github/stars/wangzhaode/ChatGLM-MNN?style=social"/> : Pure C++, Easy Deploy ChatGLM-6B.

            - [ztxz16/fastllm](https://github.com/ztxz16/fastllm) <img src="https://img.shields.io/github/stars/ztxz16/fastllm?style=social"/> : 纯c++实现，无第三方依赖的大模型库，支持CUDA加速，目前支持国产大模型ChatGLM-6B，MOSS; 可以在安卓设备上流畅运行ChatGLM-6B。

            - [davidar/eigenGPT](https://github.com/davidar/eigenGPT) <img src="https://img.shields.io/github/stars/davidar/eigenGPT?style=social"/> : Minimal C++ implementation of GPT2.

            - [Tlntin/Qwen-TensorRT-LLM](https://github.com/Tlntin/Qwen-TensorRT-LLM) <img src="https://img.shields.io/github/stars/Tlntin/Qwen-TensorRT-LLM?style=social"/> : 使用TRT-LLM完成对Qwen-7B-Chat实现推理加速。

            - [FeiGeChuanShu/trt2023](https://github.com/FeiGeChuanShu/trt2023) <img src="https://img.shields.io/github/stars/FeiGeChuanShu/trt2023?style=social"/> : NVIDIA TensorRT Hackathon 2023复赛选题：通义千问Qwen-7B用TensorRT-LLM模型搭建及优化。

            - [TRT2022/trtllm-llama](https://github.com/TRT2022/trtllm-llama) <img src="https://img.shields.io/github/stars/TRT2022/trtllm-llama?style=social"/> : ☢️ TensorRT 2023复赛——基于TensorRT-LLM的Llama模型推断加速优化。

            - [AmeyaWagh/llama2.cpp](https://github.com/AmeyaWagh/llama2.cpp) <img src="https://img.shields.io/github/stars/AmeyaWagh/llama2.cpp?style=social"/> : Inference Llama 2 in C++.


        - ##### Mojo Implementation

            - [llama2.mojo](https://github.com/tairov/llama2.mojo) <img src="https://img.shields.io/github/stars/tairov/llama2.mojo?style=social"/> : Inference Llama 2 in one file of pure 🔥

            - [dorjeduck/llm.mojo](https://github.com/dorjeduck/llm.mojo) <img src="https://img.shields.io/github/stars/dorjeduck/llm.mojo?style=social"/> : port of Andrjey Karpathy's llm.c to Mojo.


        - ##### Rust Implementation

            - [Candle](https://github.com/huggingface/candle) <img src="https://img.shields.io/github/stars/huggingface/candle?style=social"/> : Minimalist ML framework for Rust.

            - [Safetensors](https://github.com/huggingface/safetensors) <img src="https://img.shields.io/github/stars/huggingface/safetensors?style=social"/> : Simple, safe way to store and distribute tensors. [huggingface.co/docs/safetensors](https://huggingface.co/docs/safetensors/index)

            - [Tokenizers](https://github.com/huggingface/tokenizers) <img src="https://img.shields.io/github/stars/huggingface/tokenizers?style=social"/> : 💥 Fast State-of-the-Art Tokenizers optimized for Research and Production. [huggingface.co/docs/tokenizers](https://huggingface.co/docs/tokenizers/index)

            - [Burn](https://github.com/burn-rs/burn) <img src="https://img.shields.io/github/stars/burn-rs/burn?style=social"/> : Burn - A Flexible and Comprehensive Deep Learning Framework in Rust. [burn-rs.github.io/](https://burn-rs.github.io/)

            - [dfdx](https://github.com/coreylowman/dfdx) <img src="https://img.shields.io/github/stars/coreylowman/dfdx?style=social"/> : Deep learning in Rust, with shape checked tensors and neural networks.

            - [luminal](https://github.com/jafioti/luminal) <img src="https://img.shields.io/github/stars/jafioti/luminal?style=social"/> : Deep learning at the speed of light. [www.luminalai.com/](https://www.luminalai.com/)

            - [crabml](https://github.com/crabml/crabml) <img src="https://img.shields.io/github/stars/crabml/crabml?style=social"/> : crabml is focusing on the reimplementation of GGML using the Rust programming language.

            - [TensorFlow Rust](https://github.com/tensorflow/rust) <img src="https://img.shields.io/github/stars/tensorflow/rust?style=social"/> : Rust language bindings for TensorFlow.

            - [tch-rs](https://github.com/LaurentMazare/tch-rs) <img src="https://img.shields.io/github/stars/LaurentMazare/tch-rs?style=social"/> : Rust bindings for the C++ api of PyTorch.

            - [rustai-solutions/candle_demo_openchat_35](https://github.com/rustai-solutions/candle_demo_openchat_35) <img src="https://img.shields.io/github/stars/rustai-solutions/candle_demo_openchat_35?style=social"/> : candle_demo_openchat_35.

            - [llama2.rs](https://github.com/srush/llama2.rs) <img src="https://img.shields.io/github/stars/srush/llama2.rs?style=social"/> : A fast llama2 decoder in pure Rust.

            - [Llama2-burn](https://github.com/Gadersd/llama2-burn) <img src="https://img.shields.io/github/stars/Gadersd/llama2-burn?style=social"/> : Llama2 LLM ported to Rust burn.

            - [gaxler/llama2.rs](https://github.com/gaxler/llama2.rs) <img src="https://img.shields.io/github/stars/gaxler/llama2.rs?style=social"/> : Inference Llama 2 in one file of pure Rust 🦀

            - [whisper-burn](https://github.com/Gadersd/whisper-burn) <img src="https://img.shields.io/github/stars/Gadersd/whisper-burn?style=social"/> : A Rust implementation of OpenAI's Whisper model using the burn framework.

            - [stable-diffusion-burn](https://github.com/Gadersd/stable-diffusion-burn) <img src="https://img.shields.io/github/stars/Gadersd/stable-diffusion-burn?style=social"/> : Stable Diffusion v1.4 ported to Rust's burn framework.

            - [coreylowman/llama-dfdx](https://github.com/coreylowman/llama-dfdx) <img src="https://img.shields.io/github/stars/coreylowman/llama-dfdx?style=social"/> : [LLaMa 7b](https://ai.facebook.com/blog/large-language-model-llama-meta-ai/) with CUDA acceleration implemented in rust. Minimal GPU memory needed!

            - [tazz4843/whisper-rs](https://github.com/tazz4843/whisper-rs) <img src="https://img.shields.io/github/stars/tazz4843/whisper-rs?style=social"/> : Rust bindings to [whisper.cpp](https://github.com/ggerganov/whisper.cpp).

            - [rustformers/llm](https://github.com/rustformers/llm) <img src="https://img.shields.io/github/stars/rustformers/llm?style=social"/> : Run inference for Large Language Models on CPU, with Rust 🦀🚀🦙.

            - [Chidori](https://github.com/ThousandBirdsInc/chidori) <img src="https://img.shields.io/github/stars/ThousandBirdsInc/chidori?style=social"/> : A reactive runtime for building durable AI agents. [docs.thousandbirds.ai](https://docs.thousandbirds.ai/).

            - [llm-chain](https://github.com/sobelio/llm-chain) <img src="https://img.shields.io/github/stars/sobelio/llm-chain?style=social"/> : llm-chain is a collection of Rust crates designed to help you work with Large Language Models (LLMs) more effectively. [llm-chain.xyz](https://llm-chain.xyz/)

            - [Atome-FE/llama-node](https://github.com/Atome-FE/llama-node) <img src="https://img.shields.io/github/stars/Atome-FE/llama-node?style=social"/> : Believe in AI democratization. llama for nodejs backed by llama-rs and llama.cpp, work locally on your laptop CPU. support llama/alpaca/gpt4all/vicuna model. [www.npmjs.com/package/llama-node](https://www.npmjs.com/package/llama-node)

            - [Noeda/rllama](https://github.com/Noeda/rllama) <img src="https://img.shields.io/github/stars/Noeda/rllama?style=social"/> : Rust+OpenCL+AVX2 implementation of LLaMA inference code.

            - [lencx/ChatGPT](https://github.com/lencx/ChatGPT) <img src="https://img.shields.io/github/stars/lencx/ChatGPT?style=social"/> : 🔮 ChatGPT Desktop Application (Mac, Windows and Linux). [NoFWL](https://app.nofwl.com/).

            - [Synaptrix/ChatGPT-Desktop](https://github.com/Synaptrix/ChatGPT-Desktop) <img src="https://img.shields.io/github/stars/Synaptrix/ChatGPT-Desktop?style=social"/> : Fuel your productivity with ChatGPT-Desktop - Blazingly fast and supercharged!

            - [Poordeveloper/chatgpt-app](https://github.com/Poordeveloper/chatgpt-app) <img src="https://img.shields.io/github/stars/Poordeveloper/chatgpt-app?style=social"/> : A ChatGPT App for all platforms. Built with Rust + Tauri + Vue + Axum.

            - [mxismean/chatgpt-app](https://github.com/mxismean/chatgpt-app) <img src="https://img.shields.io/github/stars/mxismean/chatgpt-app?style=social"/> : Tauri 项目：ChatGPT App.

            - [sonnylazuardi/chat-ai-desktop](https://github.com/sonnylazuardi/chat-ai-desktop) <img src="https://img.shields.io/github/stars/sonnylazuardi/chat-ai-desktop?style=social"/> : Chat AI Desktop App. Unofficial ChatGPT desktop app for Mac & Windows menubar using Tauri & Rust.

            - [yetone/openai-translator](https://github.com/yetone/openai-translator) <img src="https://img.shields.io/github/stars/yetone/openai-translator?style=social"/> : The translator that does more than just translation - powered by OpenAI.

            - [m1guelpf/browser-agent](https://github.com/m1guelpf/browser-agent) <img src="https://img.shields.io/github/stars/m1guelpf/browser-agent?style=social"/> : A browser AI agent, using GPT-4. [docs.rs/browser-agent](https://docs.rs/browser-agent/latest/browser_agent/)

            - [sigoden/aichat](https://github.com/sigoden/aichat) <img src="https://img.shields.io/github/stars/sigoden/aichat?style=social"/> : Using ChatGPT/GPT-3.5/GPT-4 in the terminal.

            - [uiuifree/rust-openai-chatgpt-api](https://github.com/uiuifree/rust-openai-chatgpt-api) <img src="https://img.shields.io/github/stars/uiuifree/rust-openai-chatgpt-api?style=social"/> : "rust-openai-chatgpt-api" is a Rust library for accessing the ChatGPT API, a powerful NLP platform by OpenAI. The library provides a simple and efficient interface for sending requests and receiving responses, including chat. It uses reqwest and serde for HTTP requests and JSON serialization.

            - [1595901624/gpt-aggregated-edition](https://github.com/1595901624/gpt-aggregated-edition) <img src="https://img.shields.io/github/stars/1595901624/gpt-aggregated-edition?style=social"/> : 聚合ChatGPT官方版、ChatGPT免费版、文心一言、Poe、chatchat等多平台，支持自定义导入平台。

            - [Cormanz/smartgpt](https://github.com/Cormanz/smartgpt) <img src="https://img.shields.io/github/stars/Cormanz/smartgpt?style=social"/> : A program that provides LLMs with the ability to complete complex tasks using plugins.

            - [femtoGPT](https://github.com/keyvank/femtoGPT) <img src="https://img.shields.io/github/stars/keyvank/femtoGPT?style=social"/> : femtoGPT is a pure Rust implementation of a minimal Generative Pretrained Transformer. [discord.gg/wTJFaDVn45](https://github.com/keyvank/femtoGPT)

            - [shafishlabs/llmchain-rs](https://github.com/shafishlabs/llmchain-rs) <img src="https://img.shields.io/github/stars/shafishlabs/llmchain-rs?style=social"/> : 🦀Rust + Large Language Models - Make AI Services Freely and Easily. Inspired by LangChain.

            - [flaneur2020/llama2.rs](https://github.com/flaneur2020/llama2.rs) <img src="https://img.shields.io/github/stars/flaneur2020/llama2.rs?style=social"/> : An rust reimplementatin of [https://github.com/karpathy/llama2.c](https://github.com/karpathy/llama2.c).

            - [Heng30/chatbox](https://github.com/Heng30/chatbox) <img src="https://img.shields.io/github/stars/Heng30/chatbox?style=social"/> : A Chatbot for OpenAI ChatGPT. Based on Slint-ui and Rust.

            - [fairjm/dioxus-openai-qa-gui](https://github.com/fairjm/dioxus-openai-qa-gui) <img src="https://img.shields.io/github/stars/fairjm/dioxus-openai-qa-gui?style=social"/> : a simple openai qa desktop app built with dioxus.

            - [purton-tech/bionicgpt](https://github.com/purton-tech/bionicgpt) <img src="https://img.shields.io/github/stars/purton-tech/bionicgpt?style=social"/> : Accelerate LLM adoption in your organisation. Chat with your confidential data safely and securely. [bionic-gpt.com](https://bionic-gpt.com/)

            - [InfiniTensor/transformer-rs](https://github.com/InfiniTensor/transformer-rs) <img src="https://img.shields.io/github/stars/InfiniTensor/transformer-rs?style=social"/> : 从 [YdrMaster/llama2.rs](https://github.com/YdrMaster/llama2.rs) 发展来的手写 transformer 模型项目。


        - #### Zig Implementation

            - [llama2.zig](https://github.com/cgbur/llama2.zig) <img src="https://img.shields.io/github/stars/cgbur/llama2.zig?style=social"/> : Inference Llama 2 in one file of pure Zig.

            - [renerocksai/gpt4all.zig](https://github.com/renerocksai/gpt4all.zig) <img src="https://img.shields.io/github/stars/renerocksai/gpt4all.zig?style=social"/> : ZIG build for a terminal-based chat client for an assistant-style large language model with ~800k GPT-3.5-Turbo Generations based on LLaMa.

            - [EugenHotaj/zig_inference](https://github.com/EugenHotaj/zig_inference) <img src="https://img.shields.io/github/stars/EugenHotaj/zig_inference?style=social"/> : Neural Network Inference Engine in Zig.


        - ##### Go Implementation

            - [Ollama](https://github.com/ollama/ollama/) <img src="https://img.shields.io/github/stars/ollama/ollama?style=social"/> : Get up and running with Llama 2, Mistral, Gemma, and other large language models. [ollama.com](https://ollama.com/)


            - [go-skynet/LocalAI](https://github.com/go-skynet/LocalAI) <img src="https://img.shields.io/github/stars/go-skynet/LocalAI?style=social"/> : 🤖 Self-hosted, community-driven, local OpenAI-compatible API. Drop-in replacement for OpenAI running LLMs on consumer-grade hardware. Free Open Source OpenAI alternative. No GPU required. LocalAI is an API to run ggml compatible models: llama, gpt4all, rwkv, whisper, vicuna, koala, gpt4all-j, cerebras, falcon, dolly, starcoder, and many other. [localai.io](https://localai.io/)


    - #### Vector Database
      ##### 向量数据库

        - [Qdrant](https://github.com/milvus-io/milvus) <img src="https://img.shields.io/github/stars/milvus-io/milvus?style=social"/> : Milvus is an open-source vector database built to power embedding similarity search and AI applications. Milvus makes unstructured data search more accessible, and provides a consistent user experience regardless of the deployment environment. [milvus.io](https://milvus.io/)

        - [Qdrant](https://github.com/qdrant/qdrant) <img src="https://img.shields.io/github/stars/qdrant/qdrant?style=social"/> : Qdrant - Vector Database for the next generation of AI applications. Also available in the cloud [https://cloud.qdrant.io/](https://cloud.qdrant.io/). [qdrant.tech](https://qdrant.tech/)




  - ### Awesome List

    - [Hannibal046/Awesome-LLM](https://github.com/Hannibal046/Awesome-LLM) <img src="https://img.shields.io/github/stars/Hannibal046/Awesome-LLM?style=social"/> : Awesome-LLM: a curated list of Large Language Model.

    - [DefTruth/Awesome-LLM-Inference](https://github.com/DefTruth/Awesome-LLM-Inference) <img src="https://img.shields.io/github/stars/DefTruth/Awesome-LLM-Inference?style=social"/> : 📖A curated list of Awesome LLM Inference Paper with codes, TensorRT-LLM, vLLM, streaming-llm, AWQ, SmoothQuant, WINT8/4, Continuous Batching, FlashAttention, PagedAttention etc.

    - [RUCAIBox/LLMSurvey](https://github.com/RUCAIBox/LLMSurvey) <img src="https://img.shields.io/github/stars/RUCAIBox/LLMSurvey?style=social"/> : The official GitHub page for the survey paper "A Survey of Large Language Models". (**[arXiv 2023](https://arxiv.org/abs/2303.18223)**). " 微信公众号「RUC AI Box」《[大模型综述升级啦](https://mp.weixin.qq.com/s/9YMUSSrGLSBKMFY3JYlaoQ)》"。

    - [jxzhangjhu/Awesome-LLM-RAG](https://github.com/jxzhangjhu/Awesome-LLM-RAG) <img src="https://img.shields.io/github/stars/jxzhangjhu/Awesome-LLM-RAG?style=social"/> : Awesome-LLM-RAG: a curated list of advanced retrieval augmented generation (RAG) in Large Language Models.

    - [vince-lam/awesome-local-llms](https://github.com/vince-lam/awesome-local-llms) <img src="https://img.shields.io/github/stars/vince-lam/awesome-local-llms?style=social"/> : Compare open-source local LLM inference projects by their metrics to assess popularity and activeness.

    - [BradyFU/Awesome-Multimodal-Large-Language-Models](https://github.com/BradyFU/Awesome-Multimodal-Large-Language-Models) <img src="https://img.shields.io/github/stars/BradyFU/Awesome-Multimodal-Large-Language-Models?style=social"/> : ✨✨Latest Papers and Datasets on Multimodal Large Language Models, and Their Evaluation. "A Survey on Multimodal Large Language Models". (**[arXiv 2023](https://arxiv.org/abs/2306.13549)**). " 微信公众号「我爱计算机视觉」《[中科大腾讯发布首篇《多模态大语言模型综述》](https://mp.weixin.qq.com/s/IiPZWEVdAJ4xrlgyWtDwng)》"。

    - [hymie122/RAG-Survey](https://github.com/hymie122/RAG-Survey) <img src="https://img.shields.io/github/stars/hymie122/RAG-Survey?style=social"/> : Collecting awesome papers of RAG for AIGC. We propose a taxonomy of RAG foundations, enhancements, and applications in paper "Retrieval-Augmented Generation for AI-Generated Content: A Survey". (**[arXiv 2024](https://arxiv.org/abs/2402.19473)**). " 微信公众号「数智笔记」《[2024检索增强生成RAG最新综述](https://mp.weixin.qq.com/s/F-shRy1m7wQIS87ujOS7Dw)》"。

    - [eugeneyan/open-llms](https://github.com/eugeneyan/open-llms) <img src="https://img.shields.io/github/stars/eugeneyan/open-llms?style=social"/> : 📋 A list of open LLMs available for commercial use.

    - [formulahendry/awesome-gpt](https://github.com/formulahendry/awesome-gpt) <img src="https://img.shields.io/github/stars/formulahendry/awesome-gpt?style=social"/> : A curated list of awesome projects and resources related to GPT, ChatGPT, OpenAI, LLM, and more.

    - [HqWu-HITCS/Awesome-Chinese-LLM](https://github.com/HqWu-HITCS/Awesome-Chinese-LLM) <img src="https://img.shields.io/github/stars/HqWu-HITCS/Awesome-Chinese-LLM?style=social"/> : 整理开源的中文大语言模型，以规模较小、可私有化部署、训练成本较低的模型为主，包括底座模型，垂直领域微调及应用，数据集与教程等。

    - [cedrickchee/awesome-transformer-nlp](https://github.com/cedrickchee/awesome-transformer-nlp) <img src="https://img.shields.io/github/stars/cedrickchee/awesome-transformer-nlp?style=social"/> : A curated list of NLP resources focused on Transformer networks, attention mechanism, GPT, BERT, ChatGPT, LLMs, and transfer learning.

    - [GT-RIPL/Awesome-LLM-Robotics](https://github.com/GT-RIPL/Awesome-LLM-Robotics) <img src="https://img.shields.io/github/stars/GT-RIPL/Awesome-LLM-Robotics?style=social"/> : A comprehensive list of papers using large language/multi-modal models for Robotics/RL, including papers, codes, and related websites.

    - [mikhail-bot/awesome-gpt3](https://github.com/mikhail-bot/awesome-gpt3) <img src="https://img.shields.io/github/stars/mikhail-bot/awesome-gpt3?style=social"/> :A Curated list of awesome GPT3 tools, libraries and resources.

    - [imaurer/awesome-decentralized-llm](https://github.com/imaurer/awesome-decentralized-llm) <img src="https://img.shields.io/github/stars/imaurer/awesome-decentralized-llm?style=social"/> : Repos and resources for running LLMs locally. (e.g. LLaMA, Cerebras, RWKV).

    - [csbl-br/awesome-compbio-chatgpt](https://github.com/csbl-br/awesome-compbio-chatgpt) <img src="https://img.shields.io/github/stars/csbl-br/awesome-compbio-chatgpt?style=social"/> : An awesome repository of community-curated applications of ChatGPT and other LLMs in computational biology!

    - [atfortes/LLM-Reasoning-Papers](https://github.com/atfortes/LLM-Reasoning-Papers) <img src="https://img.shields.io/github/stars/atfortes/LLM-Reasoning-Papers?style=social"/> : Collection of papers and resources on Reasoning in Large Language Models (LLMs), including Chain-of-Thought (CoT), Instruction-Tuning, and others.

    - [yzfly/Awesome-AGI](https://github.com/yzfly/Awesome-AGI) <img src="https://img.shields.io/github/stars/yzfly/Awesome-AGI?style=social"/> : A curated list of awesome AGI frameworks, software and resources.

    - [steven2358/awesome-generative-ai](https://github.com/steven2358/awesome-generative-ai) <img src="https://img.shields.io/github/stars/steven2358/awesome-generative-ai?style=social"/> : A curated list of modern Generative Artificial Intelligence projects and services.

    - [wshzd/Awesome-AIGC](https://github.com/wshzd/Awesome-AIGC) <img src="https://img.shields.io/github/stars/wshzd/Awesome-AIGC?style=social"/> : AIGC资料汇总学习，持续更新......

    - [doanbactam/awesome-stable-diffusion](https://github.com/doanbactam/awesome-stable-diffusion) <img src="https://img.shields.io/github/stars/doanbactam/awesome-stable-diffusion?style=social"/> : A curated list of awesome stable diffusion resources 🌟

    - [Yutong-Zhou-cv/Awesome-Text-to-Image](https://github.com/Yutong-Zhou-cv/Awesome-Text-to-Image) <img src="https://img.shields.io/github/stars/Yutong-Zhou-cv/Awesome-Text-to-Image?style=social"/> : (ෆ`꒳´ෆ) A Survey on Text-to-Image Generation/Synthesis.

    - [SeedV/generative-ai-roadmap](https://github.com/SeedV/generative-ai-roadmap) <img src="https://img.shields.io/github/stars/SeedV/generative-ai-roadmap?style=social"/> : 生成式AI的应用路线图 The roadmap of generative AI: use cases and applications.

    - [luban-agi/Awesome-AIGC-Tutorials](https://github.com/luban-agi/Awesome-AIGC-Tutorials) <img src="https://img.shields.io/github/stars/luban-agi/Awesome-AIGC-Tutorials?style=social"/> : Curated tutorials and resources for Large Language Models, AI Painting, and more.

    - [xx025/carrot](https://github.com/xx025/carrot) <img src="https://img.shields.io/github/stars/xx025/carrot?style=social"/> : Free ChatGPT Site List. [cc.ai55.cc](https://cc.ai55.cc/)

    - [LiLittleCat/awesome-free-chatgpt](https://github.com/LiLittleCat/awesome-free-chatgpt) <img src="https://img.shields.io/github/stars/LiLittleCat/awesome-free-chatgpt?style=social"/> : 🆓免费的 ChatGPT 镜像网站列表，持续更新。List of free ChatGPT mirror sites, continuously updated.

    - [lzwme/chatgpt-sites](https://github.com/lzwme/chatgpt-sites) <img src="https://img.shields.io/github/stars/lzwme/chatgpt-sites?style=social"/> : 搜集国内可用的 ChatGPT 在线体验免费网站列表。定时任务每日更新。[lzw.me/x/chatgpt-sites/](https://lzw.me/x/chatgpt-sites/)




  - ### Paper Overview

    - [RUCAIBox/LLMSurvey](https://github.com/RUCAIBox/LLMSurvey) <img src="https://img.shields.io/github/stars/RUCAIBox/LLMSurvey?style=social"/> : The official GitHub page for the survey paper "A Survey of Large Language Models". (**[arXiv 2023](https://arxiv.org/abs/2303.18223)**). " 微信公众号「RUC AI Box」《[大模型综述升级啦](https://mp.weixin.qq.com/s/9YMUSSrGLSBKMFY3JYlaoQ)》"。

    - [BradyFU/Awesome-Multimodal-Large-Language-Models](https://github.com/BradyFU/Awesome-Multimodal-Large-Language-Models) <img src="https://img.shields.io/github/stars/BradyFU/Awesome-Multimodal-Large-Language-Models?style=social"/> : ✨✨Latest Papers and Datasets on Multimodal Large Language Models, and Their Evaluation. "A Survey on Multimodal Large Language Models". (**[arXiv 2023](https://arxiv.org/abs/2306.13549)**). " 微信公众号「我爱计算机视觉」《[中科大腾讯发布首篇《多模态大语言模型综述》](https://mp.weixin.qq.com/s/IiPZWEVdAJ4xrlgyWtDwng)》"。

    - [hymie122/RAG-Survey](https://github.com/hymie122/RAG-Survey) <img src="https://img.shields.io/github/stars/hymie122/RAG-Survey?style=social"/> : Collecting awesome papers of RAG for AIGC. We propose a taxonomy of RAG foundations, enhancements, and applications in paper "Retrieval-Augmented Generation for AI-Generated Content: A Survey". (**[arXiv 2024](https://arxiv.org/abs/2402.19473)**). " 微信公众号「数智笔记」《[2024检索增强生成RAG最新综述](https://mp.weixin.qq.com/s/F-shRy1m7wQIS87ujOS7Dw)》"。

    - [daochenzha/data-centric-AI](https://github.com/daochenzha/data-centric-AI) <img src="https://img.shields.io/github/stars/daochenzha/data-centric-AI?style=social"/> : A curated, but incomplete, list of data-centric AI resources. "Data-centric Artificial Intelligence: A Survey". (**[arXiv 2023](https://arxiv.org/abs/2303.10158)**).

    - [KSESEU/LLMPapers](https://github.com/KSESEU/LLMPapers) <img src="https://img.shields.io/github/stars/KSESEU/LLMPapers?style=social"/> : Collection of papers and related works for Large Language Models (ChatGPT, GPT-3, Codex etc.).

    - "Challenges and Applications of Large Language Models". (**[arXiv 2023](https://arxiv.org/abs/2307.10169)**).

    - "A Survey on Vision Transformer". (**[IEEE TPAMI, 2022](https://ieeexplore.ieee.org/abstract/document/9716741)**).

    - "Transformers in Vision: A Survey". (**[CM computing surveys (CSUR), 2022](https://dl.acm.org/doi/abs/10.1145/3505244)**).




  - ### Learning Resources

    - [mlabonne/llm-course](https://github.com/mlabonne/llm-course) <img src="https://img.shields.io/github/stars/mlabonne/llm-course?style=social"/> :  Course to get into Large Language Models (LLMs) with roadmaps and Colab notebooks.[mlabonne.github.io/blog/](https://mlabonne.github.io/blog/)

    - [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) <img src="https://img.shields.io/github/stars/rasbt/LLMs-from-scratch?style=social"/> :  Implementing a ChatGPT-like LLM from scratch, step by step. [https://www.manning.com/books/build-a-large-language-model-from-scratch](https://www.manning.com/books/build-a-large-language-model-from-scratch)

    - [datawhalechina/llm-universe](https://github.com/datawhalechina/llm-universe) <img src="https://img.shields.io/github/stars/datawhalechina/llm-universe?style=social"/> : 动手学大模型应用开发。本项目是一个面向小白开发者的大模型应用开发教程，在线阅读地址：[https://datawhalechina.github.io/llm-universe/](https://datawhalechina.github.io/llm-universe/)

    - [datawhalechina/hugging-llm](https://github.com/datawhalechina/hugging-llm) <img src="https://img.shields.io/github/stars/datawhalechina/hugging-llm?style=social"/> :  HuggingLLM, Hugging Future. 蝴蝶书ButterflyBook. 配套视频教程：[https://b23.tv/hdnXn1L](https://www.bilibili.com/video/BV1ek4y1J7Rd/)

    - [DjangoPeng/openai-quickstart](https://github.com/DjangoPeng/openai-quickstart) <img src="https://img.shields.io/github/stars/DjangoPeng/openai-quickstart?style=social"/> : A comprehensive guide to understanding and implementing large language models with hands-on examples using LangChain for GenAI applications. 本项目旨在为所有对大型语言模型及其在生成式人工智能（AIGC）场景中应用的人们提供一站式学习资源。通过提供理论基础，开发基础，和实践示例，该项目对这些前沿主题提供了全面的指导。

    - [InternLM/Tutorial](https://github.com/InternLM/Tutorial) <img src="https://img.shields.io/github/stars/InternLM/Tutorial?style=social"/> : 书生·浦语大模型实战营。为了推动大模型在更多行业落地开花，让开发者们更高效的学习大模型的开发与应用，上海人工智能实验室重磅推出书生·浦语大模型实战营，为广大开发者搭建大模型学习和实践开发的平台，两周时间带你玩转大模型微调、部署与评测全链路。

    - [DLLXW/baby-llama2-chinese](https://github.com/DLLXW/baby-llama2-chinese) <img src="https://img.shields.io/github/stars/DLLXW/baby-llama2-chinese?style=social"/> : 用于从头预训练+SFT一个小参数量的中文LLaMa2的仓库；24G单卡即可运行得到一个具备简单中文问答能力的chat-llama2.

    - [charent/ChatLM-mini-Chinese](https://github.com/charent/ChatLM-mini-Chinese) <img src="https://img.shields.io/github/stars/charent/ChatLM-mini-Chinese?style=social"/> : 中文对话0.2B小模型（ChatLM-Chinese-0.2B），开源所有数据集来源、数据清洗、tokenizer训练、模型预训练、SFT指令微调、RLHF优化等流程的全部代码。支持下游任务sft微调，给出三元组信息抽取微调示例。

    - [charent/Phi2-mini-Chinese](https://github.com/charent/Phi2-mini-Chinese) <img src="https://img.shields.io/github/stars/charent/Phi2-mini-Chinese?style=social"/> : Phi2-Chinese-0.2B 从0开始训练自己的Phi2中文小模型，支持接入langchain加载本地知识库做检索增强生成RAG。Training your own Phi2 small chat model from scratch.

    - [jiahe7ay/MINI_LLM](https://github.com/jiahe7ay/MINI_LLM) <img src="https://img.shields.io/github/stars/jiahe7ay/MINI_LLM?style=social"/> : This is a repository used by individuals to experiment and reproduce the pre-training process of LLM.

    - [SmartFlowAI/Hand-on-RAG](https://github.com/SmartFlowAI/Hand-on-RAG) <img src="https://img.shields.io/github/stars/SmartFlowAI/Hand-on-RAG?style=social"/> : Hand on RAG.  顾名思义：手搓的RAG。

    - [liguodongiot/llm-action](https://github.com/liguodongiot/llm-action) <img src="https://img.shields.io/github/stars/liguodongiot/llm-action?style=social"/> :  本项目旨在分享大模型相关技术原理以及实战经验。

    - [km1994/LLMsNineStoryDemonTower](https://github.com/km1994/LLMsNineStoryDemonTower) <img src="https://img.shields.io/github/stars/km1994/LLMsNineStoryDemonTower?style=social"/> : 【LLMs九层妖塔】分享 LLMs在自然语言处理（ChatGLM、Chinese-LLaMA-Alpaca、小羊驼 Vicuna、LLaMA、GPT4ALL等）、信息检索（langchain）、语言合成、语言识别、多模态等领域（Stable Diffusion、MiniGPT-4、VisualGLM-6B、Ziya-Visual等）等 实战与经验。

    - [RahulSChand/llama2.c-for-dummies](https://github.com/RahulSChand/llama2.c-for-dummies) <img src="https://img.shields.io/github/stars/RahulSChand/llama2.c-for-dummies?style=social"/> :  Step by step explanation/tutorial of llama2.c

    - [liteli1987gmail/python_langchain_cn](https://github.com/liteli1987gmail/python_langchain_cn) <img src="https://img.shields.io/github/stars/liteli1987gmail/python_langchain_cn?style=social"/> : langchain中文网是langchain的python中文文档。[python.langchain.com.cn](https://python.langchain.com.cn/docs/)

    - [langchain-ai/rag-from-scratch](https://github.com/langchain-ai/rag-from-scratch) <img src="https://img.shields.io/github/stars/langchain-ai/rag-from-scratch?style=social"/> : Retrieval augmented generation (RAG) comes is a general methodology for connecting LLMs with external data sources. These notebooks accompany a video series will build up an understanding of RAG from scratch, starting with the basics of indexing, retrieval, and generation.

    - [phodal/aigc](https://github.com/phodal/aigc) <img src="https://img.shields.io/github/stars/phodal/aigc?style=social"/> : 《构筑大语言模型应用：应用开发与架构设计》一本关于 LLM 在真实世界应用的开源电子书，介绍了大语言模型的基础知识和应用，以及如何构建自己的模型。其中包括Prompt的编写、开发和管理，探索最好的大语言模型能带来什么，以及LLM应用开发的模式和架构设计。

    - [cystanford/aigc_LLM_engineering](https://github.com/cystanford/aigc_LLM_engineering) <img src="https://img.shields.io/github/stars/cystanford/aigc_LLM_engineering?style=social"/> : aigc_LLM_engineering.



  - ### Community

    - [Hugging Face](https://huggingface.co/) : The AI community building the future. The platform where the machine learning community collaborates on models, datasets, and applications.

    - [ModelScope | 魔塔社区](https://github.com/modelscope/modelscope) <img src="https://img.shields.io/github/stars/modelscope/modelscope?style=social"/> : [ModelScope](https://www.modelscope.cn/home) is built upon the notion of “Model-as-a-Service” (MaaS). It seeks to bring together most advanced machine learning models from the AI community, and streamlines the process of leveraging AI models in real-world applications. [ModelScope](https://www.modelscope.cn/home) 是一个“模型即服务”(MaaS)平台，旨在汇集来自AI社区的最先进的机器学习模型，并简化在实际应用中使用AI模型的流程。ModelScope库使开发人员能够通过丰富的API设计执行推理、训练和评估，从而促进跨不同AI领域的最先进模型的统一体验。[www.modelscope.cn/](https://www.modelscope.cn/)

    - [The official LangChain blog](https://blog.langchain.dev/) : LangChain. The official LangChain blog.




## Prompts
### 提示语（魔法）

  - [EmbraceAGI/LangGPT](https://github.com/EmbraceAGI/LangGPT) <img src="https://img.shields.io/github/stars/EmbraceAGI/LangGPT?style=social"/> : LangGPT: Empowering everyone to become a prompt expert!🚀 Structured Prompt，Language of GPT, 结构化提示词，结构化Prompt [feishu.langgpt.ai/](http://feishu.langgpt.ai/)

  - [PlexPt/awesome-chatgpt-prompts-zh](https://github.com/PlexPt/awesome-chatgpt-prompts-zh) <img src="https://img.shields.io/github/stars/PlexPt/awesome-chatgpt-prompts-zh?style=social"/> : ChatGPT 中文调教指南。各种场景使用指南。学习怎么让它听你的话。[chat.aimakex.com/](https://chat.aimakex.com/)

  - [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) <img src="https://img.shields.io/github/stars/f/awesome-chatgpt-prompts?style=social"/> : This repo includes ChatGPT prompt curation to use ChatGPT better.

  - [travistangvh/ChatGPT-Data-Science-Prompts](https://github.com/travistangvh/ChatGPT-Data-Science-Prompts) <img src="https://img.shields.io/github/stars/travistangvh/ChatGPT-Data-Science-Prompts?style=social"/> : 🚀 ChatGPT Prompts for Data Science! A repository of 60 useful data science prompts for ChatGPT.

  - [kevinamiri/Instructgpt-prompts](https://github.com/kevinamiri/Instructgpt-prompts) <img src="https://img.shields.io/github/stars/kevinamiri/Instructgpt-prompts?style=social"/> : A collection of ChatGPT and GPT-3.5 instruction-based prompts for generating and classifying text. [prompts.maila.ai/](https://prompts.maila.ai/)




## Open API

  - ### Python API

    - [gpt4free](https://github.com/xtekky/gpt4free) <img src="https://img.shields.io/github/stars/xtekky/gpt4free?style=social"/> : decentralising the Ai Industry, just some language model api's... [discord.gg/gpt4free](https://discord.gg/gpt4free)

    - [acheong08/ChatGPT](https://github.com/acheong08/ChatGPT) <img src="https://img.shields.io/github/stars/acheong08/ChatGPT?style=social"/> : Reverse Engineered ChatGPT API by OpenAI. Extensible for chatbots etc.

    - [wong2/chatgpt-google-extension](https://github.com/wong2/chatgpt-google-extension) <img src="https://img.shields.io/github/stars/wong2/chatgpt-google-extension?style=social"/> : A browser extension that enhance search engines with ChatGPT.

    - [acheong08/EdgeGPT](https://github.com/acheong08/EdgeGPT) <img src="https://img.shields.io/github/stars/acheong08/EdgeGPT?style=social"/> : Reverse engineered API of Microsoft's Bing Chat AI.


  - ### Rust API

    - [uiuifree/rust-openai-chatgpt-api](https://github.com/uiuifree/rust-openai-chatgpt-api) <img src="https://img.shields.io/github/stars/uiuifree/rust-openai-chatgpt-api?style=social"/> : "rust-openai-chatgpt-api" is a Rust library for accessing the ChatGPT API, a powerful NLP platform by OpenAI. The library provides a simple and efficient interface for sending requests and receiving responses, including chat. It uses reqwest and serde for HTTP requests and JSON serialization.



  - ### Csharp API

    - [betalgo/openai](https://github.com/betalgo/openai) <img src="https://img.shields.io/github/stars/betalgo/openai?style=social"/> : OpenAI ChatGPT, Whisper, GPT-3 , GPT-4, Azure OpenAI and DALL-E dotnet SDK. [betalgo.github.io/openai/](https://betalgo.github.io/openai/)

    - [OkGoDoIt/OpenAI-API-dotnet](https://github.com/OkGoDoIt/OpenAI-API-dotnet) <img src="https://img.shields.io/github/stars/OkGoDoIt/OpenAI-API-dotnet?style=social"/> : An unofficial C#/.NET SDK for accessing the OpenAI GPT-3 API. [www.nuget.org/packages/OpenAI/](https://www.nuget.org/packages/OpenAI/)

    - [RageAgainstThePixel/OpenAI-DotNet](https://github.com/RageAgainstThePixel/OpenAI-DotNet) <img src="https://img.shields.io/github/stars/RageAgainstThePixel/OpenAI-DotNet?style=social"/> : A Non-Official OpenAI RESTful API Client for dotnet.

    - [PawanOsman/ChatGPT.Net](https://github.com/PawanOsman/ChatGPT.Net) <img src="https://img.shields.io/github/stars/PawanOsman/ChatGPT.Net?style=social"/> : C# library for ChatGPT using official OpenAI API. [www.nuget.org/packages/ChatGPT.Net](https://www.nuget.org/packages/ChatGPT.Net)

    - [marcominerva/ChatGptNet](https://github.com/marcominerva/ChatGptNet) <img src="https://img.shields.io/github/stars/marcominerva/ChatGptNet?style=social"/> : A ChatGPT integration library for .NET.



  - ### Node.js API
    - [transitive-bullshit/chatgpt-api](https://github.com/transitive-bullshit/chatgpt-api) <img src="https://img.shields.io/github/stars/transitive-bullshit/chatgpt-api?style=social"/> : Node.js client for the unofficial ChatGPT API. 🔥











## Applications


  - ### IDE
    #### 集成开发环境

    - [Cursor](https://github.com/getcursor/cursor) <img src="https://img.shields.io/github/stars/getcursor/cursor?style=social"/> : An editor made for programming with AI 🤖. Long term, our plan is to build Cursor into the world's most productive development environment. [cursor.so](https://www.cursor.so/)


  - ### Chatbot
    #### 聊天机器人

    - [ChatHub](https://github.com/chathub-dev/chathub) <img src="https://img.shields.io/github/stars/chathub-dev/chathub?style=social"/> : ChatHub is an all-in-one chatbot client. [chathub.gg/?utm_source=github](https://chathub.gg/?utm_source=github)

    - [Ask-Anything](https://github.com/OpenGVLab/Ask-Anything) <img src="https://img.shields.io/github/stars/OpenGVLab/Ask-Anything?style=social"/> : [VideoChatGPT] ChatGPT with video understanding! And many more supported LMs such as miniGPT4, StableLM, and MOSS. [vchat.opengvlab.com/](https://vchat.opengvlab.com/). "VideoChat: Chat-Centric Video Understanding". (**[arXiv 2023](https://arxiv.org/abs/2305.06355)**).

    - [InternLM/HuixiangDou](https://github.com/InternLM/HuixiangDou) <img src="https://img.shields.io/github/stars/InternLM/HuixiangDou?style=social"/> : HuixiangDou: Overcoming Group Chat Scenarios with LLM-based Technical Assistance. "HuixiangDou" is a domain-specific knowledge assistant based on the LLM. “茴香豆”是一个基于 LLM 的领域知识助手。

    - [a16z-infra/llama2-chatbot](https://github.com/a16z-infra/llama2-chatbot) <img src="https://img.shields.io/github/stars/a16z-infra/llama2-chatbot?style=social"/> : LLaMA 2 Chatbot App ⚡

    - [fuergaosi233/wechat-chatgpt](https://github.com/fuergaosi233/wechat-chatgpt) <img src="https://img.shields.io/github/stars/fuergaosi233/wechat-chatgpt?style=social"/> : Use ChatGPT On Wechat via wechaty.


  - ### Role Play
    #### 角色扮演

    - [KMnO4-zx/xlab-huanhuan](https://github.com/KMnO4-zx/xlab-huanhuan) <img src="https://img.shields.io/github/stars/KMnO4-zx/xlab-huanhuan?style=social"/> : Chat-甄嬛是利用《甄嬛传》剧本中所有关于甄嬛的台词和语句，基于[InternLM2](https://github.com/InternLM/InternLM.git)进行LoRA微调或全量微调得到的模仿甄嬛语气的聊天语言模型。

    - [JimmyMa99/Roleplay-with-XiYou](https://github.com/JimmyMa99/Roleplay-with-XiYou) <img src="https://img.shields.io/github/stars/JimmyMa99/Roleplay-with-XiYou?style=social"/> : Roleplay-with-XiYou 西游角色扮演。基于《西游记》原文、白话文、ChatGPT生成数据制作的，以InternLM2微调的角色扮演多LLM聊天室。 本项目将介绍关于角色扮演类 LLM 的一切，从数据获取、数据处理，到使用 XTuner 微调并部署至 OpenXLab，再到使用 LMDeploy 部署，以 openai api 的方式接入简单的聊天室，并可以观看不同角色的 LLM 互相交流、互怼。




  - ### Embodied AI
    #### 具身智能

    - [BestAnHongjun/InternDog](https://github.com/BestAnHongjun/InternDog) <img src="https://img.shields.io/github/stars/BestAnHongjun/InternDog?style=social"/> : InternDog: 基于InternLM2大模型的离线具身智能导盲犬。



  - ### Code Assistant
    #### 代码助手

    - [GPT Pilot](https://github.com/Pythagora-io/gpt-pilot) <img src="https://img.shields.io/github/stars/Pythagora-io/gpt-pilot?style=social"/> : The first real AI developer. GPT Pilot doesn't just generate code, it builds apps! GPT Pilot is the core technology for the [Pythagora VS Code extension](https://bit.ly/3IeZxp6) that aims to provide the first real AI developer companion. Not just an autocomplete or a helper for PR messages but rather a real AI developer that can write full features, debug them, talk to you about issues, ask for review, etc.

    - [StarCoder](https://github.com/bigcode-project/starcoder) <img src="https://img.shields.io/github/stars/bigcode-project/starcoder?style=social"/> : 💫 StarCoder is a language model (LM) trained on source code and natural language text. Its training data incorporates more that 80 different programming languages as well as text extracted from GitHub issues and commits and from notebooks.

    - [CodeGeeX2](https://github.com/THUDM/CodeGeeX2) <img src="https://img.shields.io/github/stars/THUDM/CodeGeeX2?style=social"/> : CodeGeeX2: A More Powerful Multilingual Code Generation Model. [codegeex.cn](https://codegeex.cn/zh-CN)

    - [Code Llama](https://github.com/facebookresearch/codellama) <img src="https://img.shields.io/github/stars/facebookresearch/codellama?style=social"/> : Inference code for CodeLlama models.




  - ### Translator
    #### 翻译

    - [yetone/openai-translator](https://github.com/yetone/openai-translator) <img src="https://img.shields.io/github/stars/yetone/openai-translator?style=social"/> : The translator that does more than just translation - powered by OpenAI.

    - [0xpayne/gpt-migrate](https://github.com/0xpayne/gpt-migrate) <img src="https://img.shields.io/github/stars/0xpayne/gpt-migrate?style=social"/> : Easily migrate your codebase from one framework or language to another. [gpt-migrate.com](https://gpt-migrate.com/)



  - ### Local knowledge Base
    #### 本地知识库

    - [privateGPT](https://github.com/imartinez/privateGPT) <img src="https://img.shields.io/github/stars/imartinez/privateGPT?style=social"/> :Ask questions to your documents without an internet connection, using the power of LLMs. 100% private, no data leaves your execution environment at any point. You can ingest documents and ask questions without an internet connection! Built with [LangChain](https://github.com/langchain-ai/langchain), [GPT4All](https://github.com/nomic-ai/gpt4all), [LlamaCpp](https://github.com/ggerganov/llama.cpp), [Chroma](https://www.trychroma.com/) and [SentenceTransformers](https://www.sbert.net/).

    - [Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat) <img src="https://img.shields.io/github/stars/chatchat-space/Langchain-Chatchat?style=social"/> : lLangchain-Chatchat (formerly langchain-ChatGLM), local knowledge based LLM (like ChatGLM) QA app with langchain ｜ 基于 Langchain 与 ChatGLM 等语言模型的本地知识库问答。

    - [yanqiangmiffy/Chinese-LangChain](https://github.com/yanqiangmiffy/Chinese-LangChain) <img src="https://img.shields.io/github/stars/yanqiangmiffy/Chinese-LangChain?style=social"/> : Chinese-LangChain：中文langchain项目，基于ChatGLM-6b+langchain实现本地化知识库检索与智能答案生成。俗称：小必应，Q.Talk，强聊，QiangTalk。

    - [labring/FastGPT](https://github.com/labring/FastGPT) <img src="https://img.shields.io/github/stars/labring/FastGPT?style=social"/> : FastGPT is a knowledge-based question answering system built on the LLM. It offers out-of-the-box data processing and model invocation capabilities. Moreover, it allows for workflow orchestration through Flow visualization, thereby enabling complex question and answer scenarios! [fastgpt.run](https://fastgpt.run/)






  - ### Question Answering System
    #### 问答系统

    - [THUDM/WebGLM](https://github.com/THUDM/WebGLM) <img src="https://img.shields.io/github/stars/THUDM/WebGLM?style=social"/> : WebGLM: An Efficient Web-enhanced Question Answering System (KDD 2023). "WebGLM: Towards An Efficient Web-Enhanced Question Answering System with Human Preferences". (**[arXiv 2023](https://arxiv.org/abs/2306.07906)**).

    - [afaqueumer/DocQA](https://github.com/afaqueumer/DocQA) <img src="https://img.shields.io/github/stars/afaqueumer/DocQA?style=social"/> : Question Answering with Custom FIles using LLM. DocQA 🤖 is a web application built using Streamlit 🔥 and the LangChain 🦜🔗 framework, allowing users to leverage the power of LLMs for Generative Question Answering. 🌟

    - [rese1f/MovieChat](https://github.com/rese1f/MovieChat) <img src="https://img.shields.io/github/stars/rese1f/MovieChat?style=social"/> : 🔥 chat with over 10K frames of video! MovieChat can handle videos with >10K frames on a 24GB graphics card. MovieChat has a 10000× advantage over other methods in terms of the average increase in GPU memory cost per frame (21.3KB/f to ~200MB/f).




  - ### Academic Field
    #### 学术领域

    - [binary-husky/gpt_academic](https://github.com/binary-husky/gpt_academic) <img src="https://img.shields.io/github/stars/binary-husky/gpt_academic?style=social"/> : 为ChatGPT/GLM提供图形交互界面，特别优化论文阅读/润色/写作体验，模块化设计，支持自定义快捷按钮&函数插件，支持Python和C++等项目剖析&自译解功能，PDF/LaTex论文翻译&总结功能，支持并行问询多种LLM模型，支持chatglm2等本地模型。兼容文心一言, moss, llama2, rwkv, claude2, 通义千问, 书生, 讯飞星火等。

    - [kaixindelele/ChatPaper](https://github.com/kaixindelele/ChatPaper) <img src="https://img.shields.io/github/stars/kaixindelele/ChatPaper?style=social"/> : Use ChatGPT to summarize the arXiv papers. 全流程加速科研，利用chatgpt进行论文总结+润色+审稿+审稿回复。 💥💥💥面向全球，服务万千科研人的ChatPaper免费网页版正式上线：[https://chatpaper.org/](https://chatpaper.org/) 💥💥💥

    - [GPTZero](https://gptzero.me/): The World's #1 AI Detector with over 1 Million Users. Detect ChatGPT, GPT3, GPT4, Bard, and other AI models.

    - [BurhanUlTayyab/GPTZero](https://github.com/BurhanUlTayyab/GPTZero) <img src="https://img.shields.io/github/stars/BurhanUlTayyab/GPTZero?style=social"/> : An open-source implementation of [GPTZero](https://gptzero.me/). GPTZero is an AI model with some mathematical formulation to determine if a particular text fed to it is written by AI or a human being.

    - [BurhanUlTayyab/DetectGPT](https://github.com/BurhanUlTayyab/DetectGPT) <img src="https://img.shields.io/github/stars/BurhanUlTayyab/DetectGPT?style=social"/> : An open-source Pytorch implementation of [DetectGPT](https://arxiv.org/pdf/2301.11305.pdf). DetectGPT is an amazing method to determine whether a piece of text is written by large language models (like ChatGPT, GPT3, GPT2, BLOOM etc). However, we couldn't find any open-source implementation of it. Therefore this is the implementation of the paper. "DetectGPT: Zero-Shot Machine-Generated Text Detection using Probability Curvature". (**[arXiv 2023](https://arxiv.org/abs/2301.11305v1)**).

    - [WangRongsheng/ChatGenTitle](https://github.com/WangRongsheng/ChatGenTitle) <img src="https://img.shields.io/github/stars/WangRongsheng/ChatGenTitle?style=social"/> : 🌟 ChatGenTitle：使用百万arXiv论文信息在LLaMA模型上进行微调的论文题目生成模型。

    - [nishiwen1214/ChatReviewer](https://github.com/nishiwen1214/ChatReviewer) <img src="https://img.shields.io/github/stars/nishiwen1214/ChatReviewer?style=social"/> : ChatReviewer: use ChatGPT to review papers; ChatResponse: use ChatGPT to respond to reviewers. 💥💥💥ChatReviewer的第一版网页出来了！！！ 直接点击：[https://huggingface.co/spaces/ShiwenNi/ChatReviewer](https://huggingface.co/spaces/ShiwenNi/ChatReviewer)

    - [Shiling42/web-simulator-by-GPT4](https://github.com/Shiling42/web-simulator-by-GPT4) <img src="https://img.shields.io/github/stars/Shiling42/web-simulator-by-GPT4?style=social"/> : Online Interactive Physical Simulation Generated by GPT-4. [shilingliang.com/web-simulator-by-GPT4/](https://shilingliang.com/web-simulator-by-GPT4/)




  - ### Medical Field
    #### 医药领域

    - [本草[原名：华驼(HuaTuo)]](https://github.com/SCIR-HI/Huatuo-Llama-Med-Chinese) <img src="https://img.shields.io/github/stars/SCIR-HI/Huatuo-Llama-Med-Chinese?style=social"/> : Repo for BenTsao [original name: HuaTuo (华驼)], Llama-7B tuned with Chinese medical knowledge. 本草[原名：华驼(HuaTuo)]: 基于中文医学知识的LLaMA微调模型。本项目开源了经过中文医学指令精调/指令微调(Instruct-tuning) 的LLaMA-7B模型。我们通过医学知识图谱和GPT3.5 API构建了中文医学指令数据集，并在此基础上对LLaMA进行了指令微调，提高了LLaMA在医疗领域的问答效果。 "HuaTuo: Tuning LLaMA Model with Chinese Medical Knowledge". (**[arXiv 2023](https://arxiv.org/abs/2304.06975)**).

    - [MedSAM](https://github.com/bowang-lab/MedSAM) <img src="https://img.shields.io/github/stars/bowang-lab/MedSAM?style=social"/> : "Segment Anything in Medical Images". (**[arXiv 2023](https://arxiv.org/abs/2304.12306)**). "微信公众号「江大白」《[MedSAM在医学领域，图像分割中的落地应用（附论文及源码）](https://mp.weixin.qq.com/s/JJ0umIzJ5VKJ87A_jnDtOw)》"。

    - [LLaVA-Med](https://github.com/microsoft/LLaVA-Med) <img src="https://img.shields.io/github/stars/microsoft/LLaVA-Med?style=social"/> : "LLaVA-Med: Training a Large Language-and-Vision Assistant for Biomedicine in One Day". (**[arXiv 2023](https://arxiv.org/abs/2306.00890)**). "微信公众号「CVHub」《[微软发布医学多模态大模型LLaVA-Med | 基于LLaVA的医学指令微调](https://mp.weixin.qq.com/s/gzyVtbMArWDnfSzfCkxl9w)》"。

    - [MedicalGPT](https://github.com/shibing624/MedicalGPT) <img src="https://img.shields.io/github/stars/shibing624/MedicalGPT?style=social"/> : MedicalGPT: Training Your Own Medical GPT Model with ChatGPT Training Pipeline. 训练医疗大模型，实现包括二次预训练、有监督微调、奖励建模、强化学习训练。"微信公众号「KBQA沉思录」《[【中文医疗大模型】训练全流程源码剖析](https://mp.weixin.qq.com/s/DTHIxyDb9vG793hAKGLt2g)》"。

    - [MedQA-ChatGLM](https://github.com/WangRongsheng/MedQA-ChatGLM) <img src="https://img.shields.io/github/stars/WangRongsheng/MedQA-ChatGLM?style=social"/> : 🛰️ 基于真实医疗对话数据在ChatGLM上进行LoRA、P-Tuning V2、Freeze、RLHF等微调，我们的眼光不止于医疗问答。[www.wangrs.co/MedQA-ChatGLM/](https://www.wangrs.co/MedQA-ChatGLM/). "MedQA-ChatGLM: A Medical QA Model Fine-tuned on ChatGLM Using Multiple fine-tuning Method and Real Medical QA Data".

    - [xhu248/AutoSAM](https://github.com/xhu248/AutoSAM) <img src="https://img.shields.io/github/stars/xhu248/AutoSAM?style=social"/> : "How to Efficiently Adapt Large Segmentation Model(SAM) to Medical Images". (**[arXiv 2023](https://arxiv.org/abs/2306.13731)**).

    - [DoctorGPT](https://github.com/llSourcell/DoctorGPT) <img src="https://img.shields.io/github/stars/llSourcell/DoctorGPT?style=social"/> :   DoctorGPT is an LLM that can pass the US Medical Licensing Exam. It works offline, it's cross-platform, & your health data stays private.

    - [仲景](https://github.com/SupritYoung/Zhongjing) <img src="https://img.shields.io/github/stars/SupritYoung/Zhongjing?style=social"/> : 仲景：首个实现从预训练到 RLHF 全流程训练的中文医疗大模型。 "Zhongjing: Enhancing the Chinese Medical Capabilities of Large Language Model through Expert Feedback and Real-world Multi-turn Dialogue". (**[arXiv 2023](https://arxiv.org/abs/2308.03549)**).




  - ### Mental Health Field
    #### 心理健康领域

    - [MeChat](https://github.com/qiuhuachuan/smile) <img src="https://img.shields.io/github/stars/qiuhuachuan/smile?style=social"/> : 中文心理健康支持对话数据集(SmileChat)与大模型(MeChat)。 "SMILE: Single-turn to Multi-turn Inclusive Language Expansion via ChatGPT for Mental Health Support". (**[arXiv 2023](https://arxiv.org/abs/2305.00450)**).


    - [SmartFlowAI/EmoLLM](https://github.com/SmartFlowAI/EmoLLM) <img src="https://img.shields.io/github/stars/SmartFlowAI/EmoLLM?style=social"/> : EmoLLM-心理健康大模型是一系列能够支持 理解用户-支持用户-帮助用户 心理健康辅导链路的心理健康大模型，由 LLM指令微调而来。心理健康大模型、LLM、The Big Model of Mental Health、Finetune、InternLM2、Qwen、ChatGLM、Baichuan、DeepSeek、Mixtral。





  - ### Legal Field
    #### 法律领域

    - [ChatLaw](https://github.com/PKU-YuanGroup/ChatLaw) <img src="https://img.shields.io/github/stars/PKU-YuanGroup/ChatLaw?style=social"/> : ChatLaw-法律大模型。[chatlaw.cloud/lawchat/](https://chatlaw.cloud/lawchat/)

    - [LaWGPT](https://github.com/pengxiao-song/LaWGPT) <img src="https://img.shields.io/github/stars/pengxiao-song/LaWGPT?style=social"/> : 🎉 Repo for LaWGPT, Chinese-Llama tuned with Chinese Legal knowledge. LaWGPT 是一系列基于中文法律知识的开源大语言模型。该系列模型在通用中文基座模型（如 Chinese-LLaMA、ChatGLM 等）的基础上扩充法律领域专有词表、大规模中文法律语料预训练，增强了大模型在法律领域的基础语义理解能力。在此基础上，构造法律领域对话问答数据集、中国司法考试数据集进行指令精调，提升了模型对法律内容的理解和执行能力。





  - ### Financial Field
    #### 金融领域

    - [FinGPT](https://github.com/ai4finance-foundation/fingpt) <img src="https://img.shields.io/github/stars/ai4finance-foundation/fingpt?style=social"/> : Data-Centric FinGPT. Open-source for open finance! Revolutionize 🔥 We'll soon release the trained model. "微信公众号「AINLPer」《[FinGPT：一个「专用于金融领域」的开源大语言模型（LLM）框架，源码公开！](https://mp.weixin.qq.com/s/A9euFin675nxGGciiX6rJQ)》"。



  - ### Math Field
    #### 数学领域

    - [Progressive-Hint](https://github.com/chuanyang-Zheng/Progressive-Hint) <img src="https://img.shields.io/github/stars/chuanyang-Zheng/Progressive-Hint?style=social"/> : "Progressive-Hint Prompting Improves Reasoning in Large Language Models". (**[arXiv 2023](https://arxiv.org/abs/2304.09797)**).

    - [Goat](https://github.com/liutiedong/goat) <img src="https://img.shields.io/github/stars/liutiedong/goat?style=social"/> : "Goat: Fine-tuned LLaMA Outperforms GPT-4 on Arithmetic Tasks". (**[arXiv 2023](https://arxiv.org/abs/2305.14201)**). "微信公众号「AINLPer」《[近乎完美！最强算术语言模型: Goar-7B，干翻GPT-4，怒越PaLM-540B！24G可训练](https://mp.weixin.qq.com/s/_haINkHNV4bMszm9F41yXA)》"。

    - [AXYZdong/AMchat](https://github.com/AXYZdong/AMchat) <img src="https://img.shields.io/github/stars/AXYZdong/AMchat?style=social"/> : AMchat 高等数学大模型。AM (Advanced Mathematics) Chat is a large language model that integrates advanced mathematical knowledge, exercises in higher mathematics, and their solutions. AM (Advanced Mathematics) chat 高等数学大模型。一个集成数学知识和高等数学习题及其解答的大语言模型。



  - ### Music Field
    #### 音乐领域

    - [GuoYiFantastic/IMelodist](https://github.com/GuoYiFantastic/IMelodist) <img src="https://img.shields.io/github/stars/GuoYiFantastic/IMelodist?style=social"/> : 旋律大师-IMelodist. Music large model based on InternLM2-chat.


  - ### Speech and Audio Field
    #### 语音和音频领域

    - [flinkerlab/neural_speech_decoding](https://github.com/flinkerlab/neural_speech_decoding) <img src="https://img.shields.io/github/stars/flinkerlab/neural_speech_decoding?style=social"/> : Neural Speech Decoding. "A neural speech decoding framework leveraging deep learning and speech synthesis" (**[Nature, 2024](https://www.nature.com/articles/s42256-024-00824-8)**). "微信公众号「量子位」《[脑电合成自然语音！LeCun转发Nature子刊新成果，代码开源](https://mp.weixin.qq.com/s/BcV3-3glmdsVF--fpPRU2g)》"。


  - ### Humor Generation
    #### 讲幽默笑话

    - [CLoT](https://github.com/sail-sg/CLoT) <img src="https://img.shields.io/github/stars/sail-sg/CLoT?style=social"/> : Creative Leap-of-Thought (CLoT). Official Codebase of our Paper: "Let's Think Outside the Box: Exploring Leap-of-Thought in Large Language Models with Creative Humor Generation" (**[CVPR 2024](https://arxiv.org/abs/2312.02439)**). [zhongshsh.github.io/CLoT](https://zhongshsh.github.io/CLoT/). "微信公众号「NewBeeNLP」《[中山大学：“梗王”大模型，靠讲笑话登上CVPR](https://mp.weixin.qq.com/s/AeWCbKByO-fYFThSxOb43A)》"。






  - ### Animation Field
    #### 动漫领域

    - [SaaRaaS-1300/InternLM2_horowag](https://github.com/SaaRaaS-1300/InternLM2_horowag) <img src="https://img.shields.io/github/stars/SaaRaaS-1300/InternLM2_horowag?style=social"/> : 🍿InternLM2_Horowag🍿 🍏专门为 2024 书生·浦语大模型挑战赛 (春季赛) 准备的 Repo🍎收录了赫萝相关的微调模型。


  - ### Food Field
    #### 食品领域

    - [SmartFlowAI/TheGodOfCookery](https://github.com/SmartFlowAI/TheGodOfCookery) <img src="https://img.shields.io/github/stars/SmartFlowAI/TheGodOfCookery?style=social"/> : 食神（The God Of Cookery）。本项目名称为“食神”（ The God Of Cookery ），灵感来自喜剧大师周星驰主演的著名电影《食神》，旨在通过人工智能技术为用户提供烹饪咨询和食谱推荐，帮助用户更好地学习和实践烹饪技巧，降低烹饪门槛，实现《食神》电影中所讲的“只要用心，人人皆能做食神”。




  - ### Tool Learning
    #### 工具学习

    - [ToolBench](https://github.com/OpenBMB/ToolBench) <img src="https://img.shields.io/github/stars/OpenBMB/ToolBench?style=social"/> : An open platform for training, serving, and evaluating large language model for tool learning. [openbmb.github.io/ToolBench/](https://openbmb.github.io/ToolBench/). "ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs". (**[arXiv 2023](https://arxiv.org/abs/2307.16789)**).






  - ### Autonomous Driving Field
    #### 自动驾驶领域

    - [DriveVLM](hhttps://tsinghua-mars-lab.github.io/DriveVLM/) : "DriveVLM: The Convergence of Autonomous Driving and Large Vision-Language Models". (**[arXiv 2024](https://arxiv.org/abs/2402.12289)**).

    - [UniAD](https://github.com/OpenDriveLab/UniAD) <img src="https://img.shields.io/github/stars/OpenDriveLab/UniAD?style=social"/> : "Planning-oriented Autonomous Driving". (**[CVPR 2023](https://arxiv.org/abs/2212.10156)**).

    - [TransGPT|致远](https://github.com/DUOMO/TransGPT) <img src="https://img.shields.io/github/stars/DUOMO/TransGPT?style=social"/> : TransGPT是国内首款开源交通大模型，主要致力于在真实交通行业中发挥实际价值。它能够实现交通情况预测、智能咨询助手、公共交通服务、交通规划设计、交通安全教育、协助管理、交通事故报告和分析、自动驾驶辅助系统等功能。TransGPT作为一个通用常识交通大模型，可以为道路工程、桥梁工程、隧道工程、公路运输、水路运输、城市公共交通运输、交通运输经济、交通运输安全等行业提供通识常识。以此为基础，可以落脚到特定的交通应用场景中。







  - ### Adversarial Attack Field
    #### 对抗攻击领域

    - [llm-attacks/llm-attacks](https://github.com/llm-attacks/llm-attacks) <img src="https://img.shields.io/github/stars/llm-attacks/llm-attacks?style=social"/> : "Universal and Transferable Adversarial Attacks on Aligned Language Models". (**[arXiv 2023](https://arxiv.org/abs/2307.15043)**). [llm-attacks.org/](https://llm-attacks.org/). "微信公众号「新智元」《[ChatGPT羊驼家族全沦陷！CMU博士击破LLM护栏，人类毁灭计划脱口而出](https://mp.weixin.qq.com/s/9UaYiLoIaXixfE8Ka8um5A)》"。




  - ### Multi-Agent Collaboration
    #### 多智能体协作

    - [MetaGPT](https://github.com/geekan/MetaGPT) <img src="https://img.shields.io/github/stars/geekan/MetaGPT?style=social"/> : "MetaGPT: Meta Programming for Multi-Agent Collaborative Framework". (**[arXiv 2023](https://arxiv.org/abs/2308.00352)**).











  - ### AI Avatar
    #### AI数字生命

    - [RealChar](https://github.com/Shaunwei/RealChar) <img src="https://img.shields.io/github/stars/Shaunwei/RealChar?style=social"/> : 🎙️🤖Create, Customize and Talk to your AI Character/Companion in Realtime (All in One Codebase!). Have a natural seamless conversation with AI everywhere (mobile, web and terminal) using LLM OpenAI GPT3.5/4, Anthropic Claude2, Chroma Vector DB, Whisper Speech2Text, ElevenLabs Text2Speech🎙️🤖 [RealChar.ai/](https://realchar.ai/)

    - [FaceChain](https://github.com/modelscope/facechain) <img src="https://img.shields.io/github/stars/modelscope/facechain?style=social"/> : FaceChain is a deep-learning toolchain for generating your Digital-Twin. FaceChain is a deep-learning toolchain for generating your Digital-Twin. With a minimum of 1 portrait-photo, you can create a Digital-Twin of your own and start generating personal portraits in different settings (multiple styles now supported!). You may train your Digital-Twin model and generate photos via FaceChain's Python scripts, or via the familiar Gradio interface. FaceChain是一个可以用来打造个人数字形象的深度学习模型工具。用户仅需要提供最低三张照片即可获得独属于自己的个人形象数字替身。FaceChain支持在gradio的界面中使用模型训练和推理能力，也支持资深开发者使用python脚本进行训练推理。

    - [VirtualWife](https://github.com/yakami129/VirtualWife) <img src="https://img.shields.io/github/stars/yakami129/VirtualWife?style=social"/> : VirtualWife 是一个虚拟主播项目，目前支持在B站进行直播，用户可以自由更换VRM人物模型，大家可以将他作为一个虚拟主播入门demo，在上面扩展自己喜欢功能。

    - [GPT-vup](https://github.com/jiran214/GPT-vup) <img src="https://img.shields.io/github/stars/jiran214/GPT-vup?style=social"/> : GPT-vup Live2D数字人直播。GPT-vup BIliBili | 抖音 | AI | 虚拟主播。

    - [ChatVRM](https://github.com/pixiv/ChatVRM) <img src="https://img.shields.io/github/stars/pixiv/ChatVRM?style=social"/> : ChatVRMはブラウザで簡単に3Dキャラクターと会話ができるデモアプリケーションです。

    - [SillyTavern](https://github.com/SillyTavern/SillyTavern) <img src="https://img.shields.io/github/stars/SillyTavern/SillyTavern?style=social"/> : LLM Frontend for Power Users. [sillytavern.app](https://sillytavern.app/)

    - [HeyGen](https://www.heygen.com/) : Scale your video production with customizable AI avatars. "微信公众号「DataLearner」《[《流浪地球2》的数字生命计划可能快实现了！HeyGen即将发布下一代AI真人视频生成技术，效果逼真到无法几乎分辨！](https://mp.weixin.qq.com/s/70Fj9HCe3ruiI43WmMZLjQ)》"。






  - ### GUI
    #### 图形用户界面

    - [ChatGPT-Next-Web](https://github.com/Yidadaa/ChatGPT-Next-Web) <img src="https://img.shields.io/github/stars/Yidadaa/ChatGPT-Next-Web?style=social"/> : A well-designed cross-platform ChatGPT UI (Web / PWA / Linux / Win / MacOS). 一键拥有你自己的跨平台 ChatGPT 应用。

    - [ChatGPT-Admin-Web](https://github.com/AprilNEA/ChatGPT-Admin-Web) <img src="https://img.shields.io/github/stars/AprilNEA/ChatGPT-Admin-Web?style=social"/> : 带有用户管理和后台管理系统的 ChatGPT WebUI. [caw.sku.moe](https://caw.sku.moe/)

    - [lencx/ChatGPT](https://github.com/lencx/ChatGPT) <img src="https://img.shields.io/github/stars/lencx/ChatGPT?style=social"/> : 🔮 ChatGPT Desktop Application (Mac, Windows and Linux). [NoFWL](https://app.nofwl.com/).

    - [Synaptrix/ChatGPT-Desktop](https://github.com/Synaptrix/ChatGPT-Desktop) <img src="https://img.shields.io/github/stars/Synaptrix/ChatGPT-Desktop?style=social"/> : Fuel your productivity with ChatGPT-Desktop - Blazingly fast and supercharged!

    - [Poordeveloper/chatgpt-app](https://github.com/Poordeveloper/chatgpt-app) <img src="https://img.shields.io/github/stars/Poordeveloper/chatgpt-app?style=social"/> : A ChatGPT App for all platforms. Built with Rust + Tauri + Vue + Axum.

    - [sonnylazuardi/chat-ai-desktop](https://github.com/sonnylazuardi/chat-ai-desktop) <img src="https://img.shields.io/github/stars/sonnylazuardi/chat-ai-desktop?style=social"/> : Chat AI Desktop App. Unofficial ChatGPT desktop app for Mac & Windows menubar using Tauri & Rust.

    - [202252197/ChatGPT_JCM](https://github.com/202252197/ChatGPT_JCM) <img src="https://img.shields.io/github/stars/202252197/ChatGPT_JCM?style=social"/> : OpenAI Manage Web. OpenAI管理界面，聚合了OpenAI的所有接口进行界面操作。

    - [m1guelpf/browser-agent](https://github.com/m1guelpf/browser-agent) <img src="https://img.shields.io/github/stars/m1guelpf/browser-agent?style=social"/> : A browser AI agent, using GPT-4. [docs.rs/browser-agent](https://docs.rs/browser-agent/latest/browser_agent/)

    - [sigoden/aichat](https://github.com/sigoden/aichat) <img src="https://img.shields.io/github/stars/sigoden/aichat?style=social"/> : Using ChatGPT/GPT-3.5/GPT-4 in the terminal.

    - [wieslawsoltes/ChatGPT](https://github.com/wieslawsoltes/ChatGPT) <img src="https://img.shields.io/github/stars/wieslawsoltes/ChatGPT?style=social"/> : A ChatGPT C# client for graphical user interface runs on MacOS, Windows, Linux, Android, iOS and Browser. Powered by [Avalonia UI](https://www.avaloniaui.net/) framework. [wieslawsoltes.github.io/ChatGPT/](https://wieslawsoltes.github.io/ChatGPT/)

    - [sigoden/aichat](https://github.com/GaiZhenbiao/ChuanhuChatGPT) <img src="https://img.shields.io/github/stars/GaiZhenbiao/ChuanhuChatGPT?style=social"/> : GUI for ChatGPT API and any LLM. 川虎 Chat 🐯 Chuanhu Chat. 为ChatGPT/ChatGLM/LLaMA/StableLM/MOSS等多种LLM提供了一个轻快好用的Web图形界。

    - [amrrs/chatgpt-clone](https://github.com/amrrs/chatgpt-clone) <img src="https://img.shields.io/github/stars/amrrs/chatgpt-clone?style=social"/> :  Build Yo'own ChatGPT with OpenAI API & Gradio.

    - [llama2-webui](https://github.com/liltom-eth/llama2-webui) <img src="https://img.shields.io/github/stars/liltom-eth/llama2-webui?style=social"/> : Run Llama 2 locally with gradio UI on GPU or CPU from anywhere (Linux/Windows/Mac). Supporting Llama-2-7B/13B/70B with 8-bit, 4-bit. Supporting GPU inference (6 GB VRAM) and CPU inference.

    - [ricklamers/gpt-code-ui](https://github.com/ricklamers/gpt-code-ui) <img src="https://img.shields.io/github/stars/ricklamers/gpt-code-ui?style=social"/> : An open source implementation of OpenAI's ChatGPT Code interpreter.

    - [mckaywrigley/chatbot-ui](https://github.com/mckaywrigley/chatbot-ui) <img src="https://img.shields.io/github/stars/mckaywrigley/chatbot-ui?style=social"/> :An open source ChatGPT UI. [chatbotui.com](https://chatbotui.com/)

    - [chieapp/chie](https://github.com/chieapp/chie) <img src="https://img.shields.io/github/stars/chieapp/chie?style=social"/> : An extensive desktop app for ChatGPT and other LLMs. [chie.app](https://chie.app/)

    - [cLangUI](https://github.com/ahmadbilaldev/langui) <img src="https://img.shields.io/github/stars/ahmadbilaldev/langui?style=social"/> : AUI for your AI. Open Source Tailwind components tailored for your GPT, generative AI, and LLM projects.

    - [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) <img src="https://img.shields.io/github/stars/AUTOMATIC1111/stable-diffusion-webui?style=social"/> : Stable Diffusion web UI. A browser interface based on Gradio library for Stable Diffusion.

    - [Mikubill/sd-webui-controlnet](https://github.com/Mikubill/sd-webui-controlnet) <img src="https://img.shields.io/github/stars/Mikubill/sd-webui-controlnet?style=social"/> : ControlNet for Stable Diffusion WebUI. The WebUI extension for ControlNet and other injection-based SD controls.

    - [oobabooga/text-generation-webui](https://github.com/oobabooga/text-generation-webui) <img src="https://img.shields.io/github/stars/oobabooga/text-generation-webui?style=social"/> : Text generation web UI. A gradio web UI for running Large Language Models like LLaMA, llama.cpp, GPT-J, Pythia, OPT, and GALACTICA.

    - [SolidUI](https://github.com/CloudOrc/SolidUI) <img src="https://img.shields.io/github/stars/CloudOrc/SolidUI?style=social"/> : AI-generated visualization prototyping and editing platform.

    - [AIdea](https://github.com/mylxsw/aidea) <img src="https://img.shields.io/github/stars/mylxsw/aidea?style=social"/> : AIdea 是一款支持 GPT 以及国产大语言模型通义千问、文心一言等，支持 Stable Diffusion 文生图、图生图、 SDXL1.0、超分辨率、图片上色的全能型 APP。

    - [Chainlit](https://github.com/Chainlit/chainlit) <img src="https://img.shields.io/github/stars/Chainlit/chainlit?style=social"/> : Build Python LLM apps in minutes ⚡️ Chainlit lets you create ChatGPT-like UIs on top of any Python code in minutes! [docs.chainlit.io](https://docs.chainlit.io/overview)



## Datasets
### 数据集

  - ### Open Datasets Platform
    #### 开放数据集平台

    - [OpenDataLab](https://opendatalab.org.cn/) : 为大模型提供高质量的开放数据集！

  - ### Text Datasets
    #### 文本数据集

    - [Leymore/ruozhiba](https://github.com/Leymore/ruozhiba) <img src="https://img.shields.io/github/stars/Leymore/ruozhiba?style=social"/> : 从百度[弱智吧](https://tieba.baidu.com/f?kw=%E5%BC%B1%E6%99%BA)上收集的一系列帖子。旨在启发人们娱乐性使用 ChatGPT 等 LLM 时的思路。


  - ### Multimodal Datasets
    #### 多模态数据集

    - [Youku-mPLUG](https://github.com/X-PLUG/Youku-mPLUG) <img src="https://img.shields.io/github/stars/X-PLUG/Youku-mPLUG?style=social"/> : "Youku-mPLUG: A 10 Million Large-scale Chinese Video-Language Dataset for Pre-training and Benchmarks". (**[arXiv 2023](https://arxiv.org/abs/2306.04362)**). "微信公众号「我爱计算机视觉」《[YouKu-mPLUG 最大中文视频语言数据集，助力增强多模态大型模型性能](https://mp.weixin.qq.com/s/iJoaKCykO09R3jTCylRTVA)》"。

    - [Intern · WanJuan｜书生·万卷](https://github.com/opendatalab/WanJuan1.0) <img src="https://img.shields.io/github/stars/opendatalab/WanJuan1.0?style=social"/> : Intern · WanJuan Multimodal Corpus. 万卷1.0多模态语料。

    - [matrix-alpha/Accountable-Textual-Visual-Chat](https://github.com/matrix-alpha/Accountable-Textual-Visual-Chat) <img src="https://img.shields.io/github/stars/matrix-alpha/Accountable-Textual-Visual-Chat?style=social"/> : "Accountable Textual-Visual Chat Learns to Reject Human Instructions in Image Re-creation". (**[arXiv 2023](https://arxiv.org/abs/2303.05983)**). [https://matrix-alpha.github.io/](https://matrix-alpha.github.io/)



  - ### SFT Datasets
    #### SFT数据集

    - [chaoswork/sft_datasets](https://github.com/chaoswork/sft_datasets) <img src="https://img.shields.io/github/stars/chaoswork/sft_datasets?style=social"/> : 开源SFT数据集整理,随时补充。







## Blogs

  - 微信公众号「NVIDIA英伟达」
    - [2023-10-27，现已公开发布！欢迎使用 NVIDIA TensorRT-LLM 优化大语言模型推理](https://mp.weixin.qq.com/s/QaSbvyAmI6XXtr0y6W4LNQ)
  - 微信公众号「Hugging Face」
    - [2023-08-16，关于 Llama 2 的一切资源，我们都帮你整理好了](https://mp.weixin.qq.com/s/-01Dg9ZVfPYM4mZ4iKt8Cw)
    - [2023-08-24，社区供稿 | 推理 1760 亿参数的 BLOOMZ，性能时延仅 3.7 秒](https://mp.weixin.qq.com/s/LNEK5DK3p03qHeMxpht7GQ)
    - [2023-08-24，使用 AutoGPTQ 和 transformers 让大语言模型更轻量化](https://mp.weixin.qq.com/s/uaIxZFpcVTsKE_uA-V37bQ)
    - [2023-08-28，Hugging News #0821: Hugging Face 完成 2.35 亿美元 D 轮融资](https://mp.weixin.qq.com/s/s0lzSI5qZ5oJm5O0lh_5mg)
    - [2024-02-22，欢迎 Gemma: Google 最新推出开源大语言模型](https://mp.weixin.qq.com/s/E52nPpWrhnU7wMLpOhVz5Q)
  - 微信公众号「腾讯研究院」
    - [2024-03-04，从诊室到云端：医疗大模型的应用挑战与未来探索](https://mp.weixin.qq.com/s/BoDq30q0K0kEKYzZhn71sQ)
    - [2024-04-19，万字实录：中美大模型生态及技术趋势](https://mp.weixin.qq.com/s/pIOm2QZbuE6AvgW_ucdWBw)
  - 微信公众号「腾讯技术工程」
    - [2023-08-17，一文入门最热的LLM应用开发框架LangChain](https://mp.weixin.qq.com/s/bYzNNL3F0998Do2Jl0PQtw)
  - 微信公众号「微软科技」
    - [2023-02-16，揭秘ChatGPT走红背后的独门云科技！](https://mp.weixin.qq.com/s/qYZ7G5uLHTiLG8AonIch8g)
    - [2023-07-26，Llama 2 登陆 Azure 和 Windows，微软与 Meta 拓展人工智能合作伙伴关系](https://mp.weixin.qq.com/s/pQLd5ZVNLdhnguPmmaDlCg)
  - 微信公众号「微软亚洲研究院」
    - [2023-08-16，ResNet四位作者获得2023未来科学大奖](https://mp.weixin.qq.com/s/PKXW-RqIuHQXjTuanqdAbQ)
  - 微信公众号「Azure云科技」
    - [2023-02-15，微软 Azure 作为 OpenAI 独家云服务提供商，助力企业致胜人工智能时代](https://mp.weixin.qq.com/s/SCmWX4uz3Ici2Shy6r1x7Q)
  - 微信公众号「InternLM」
    - [2024-03-05，你一票我一票，首期书生·浦语大模型实战营明星项目就出道！](https://mp.weixin.qq.com/s/-MpBhlV-kLMUf4lMeFoFlw)
    - [2024-03-25，首届书生·浦源大模型挑战赛圆满收官，实战营学员大放异彩！](https://mp.weixin.qq.com/s/_n0OyGsYxlO9arUak8cMNg)
    - [2024-03-26，LLM问答助手茴香豆发布web版，零开发集成微信&飞书群](https://mp.weixin.qq.com/s/Ru-JS-3QQVIRsdREjiDurg)
    - [2024-04-02，InternLM2技术报告——社区翻译版](https://mp.weixin.qq.com/s/IUUj_CWUJPdrhLq1XAR-KA)
  - 微信公众号「GLM大模型」
    - [2023-06-25，【发布】ChatGLM2-6B：性能大幅提升，8-32k上下文，推理提速42%](https://mp.weixin.qq.com/s/_h9ls_gHIgHho1RBwUlhsA)
    - [2023-07-14，【公告】ChatGLM2-6B，免费商用](https://mp.weixin.qq.com/s/pNMcR2c6kFV1TVaI8wzHRg)
    - [2023-07-25，【发布】代码模型 CodeGeeX2-6B 开源，最低6GB显存，性能优于StarCoder](https://mp.weixin.qq.com/s/qw31ThM4AjG6RrjNwsfZwg)
  - 微信公众号「量子位」
    - [2023-02-05，教ChatGPT学会看图的方法来了](https://mp.weixin.qq.com/s/OyLnRKgsklzQ09y9irtdQg)
    - [2023-02-12，ChatGPT背后模型被证实具有人类心智！斯坦福新研究炸了，知名学者：“这一天终于来了”](https://mp.weixin.qq.com/s/zgrJVFvkqG69BrQCky193A)
    - [2023-02-13，让ChatGPT长“手”！Meta爆火新论文，让语言模型学会自主使用工具](https://mp.weixin.qq.com/s/nca9jMOXgMKfhA8bo0FQvw)
    - [2023-02-15，ChatGPT低成本复现流程开源！任意单张消费级显卡可体验，显存需求低至1.62GB](https://mp.weixin.qq.com/s/GcqFifmpE3_VvuAcJPsf-A)
    - [2023-03-15，GPT-4发布！ChatGPT大升级！太太太太强了！](https://mp.weixin.qq.com/s/6u33Xnp4oEHq26WR4W1kdg)
    - [2023-03-15，微软为ChatGPT打造专用超算！砸下几亿美元，上万张英伟达A100打造](https://mp.weixin.qq.com/s/jae8CoMWMKqLVhApqBcTfg)
    - [2023-05-08，MathGPT来了！专攻数学大模型，解题讲题两手抓](https://mp.weixin.qq.com/s/RUnJ2T9BueDnDCu91m8uPQ)
    - [2023-05-19，前哈工大教授开发的ChatALL火了！可同时提问17个聊天模型，ChatGPT/Bing/Bard/文心/讯飞都OK](https://mp.weixin.qq.com/s/1ERc9nBKMz9H_7hO02ky6w)
    - [2023-05-19，ChatGPT突然上线APP！iPhone可用、速度更快，GPT-4用量限制疑似取消](https://mp.weixin.qq.com/s/TPeViQhBPrcUqWf7LbWsNg)
    - [2023-05-28，「大一统」大模型论文爆火，4种模态任意输入输出，华人本科生5篇顶会一作，网友：近期最不可思议的论文](https://mp.weixin.qq.com/s/Mg_qnawkYSWnRHk4LIEIsQ)
    - [2023-06-22，CVPR最佳论文颁给自动驾驶大模型！中国团队第一单位，近10年三大视觉顶会首例](https://mp.weixin.qq.com/s/bWaqD8GNGRrLxE1F_7r1fA)
    - [2023-07-11，王小川大模型25天再升级！13B版本开源免费可商用，3090即可部署](https://mp.weixin.qq.com/s/sFVAgypEptxa6qCYcHix9g)
    - [2023-07-12，Transformer八子谷歌一个也没留住！最后一名作者已宣布离职创业](https://mp.weixin.qq.com/s/1Lu57q-l69-A4WCABGBhgg)
    - [2023-07-19，开源大模型重击OpenAI！小扎放出LLaMA2炸裂科技圈，联手微软高通冲击市场格局](https://mp.weixin.qq.com/s/GYu0ajE3eKO3TyFwHqGFgw)
    - [2023-07-31，何恺明官宣加入MIT，正式回归学术界！](https://mp.weixin.qq.com/s/x2P0G6-Zm0tivmWLTYTprw)
    - [2023-08-05，马斯克xAI创始成员国内首发声：ChatGPT时代「乱世出英雄」，下一步要多用数学科学数据训练](https://mp.weixin.qq.com/s/DncxAtjV47sMqpnxG0azgQ)
    - [2023-08-07，Llama2等30+模型接入千帆大模型平台，推理成本降50%！还有超全Prompt模板开放体验](https://mp.weixin.qq.com/s/OBgl6-QOX-6cOsnl6waKxw)
    - [2023-08-16，OpenAI进军内容审核行业，学校图书馆已经用ChatGPT筛选色情描述了](https://mp.weixin.qq.com/s/Bp62epgjN0XcBs6AoGUk7A)
    - [2024-03-28，微软亚研院新作：让大模型一口气调用数百万个API！](https://mp.weixin.qq.com/s/fy9lw3QwOMryFMOEmTXfUA)
    - [2024-04-04，弱智吧竟成最佳中文AI训练数据？！中科院等：8项测试第一，远超知乎豆瓣小红书](https://mp.weixin.qq.com/s/iq5lGyh9Y5P7NXLUS3-giA)
    - [2024-04-12，谷歌爆改Transformer，“无限注意力”让1B小模型读完10部小说，114倍信息压缩](https://mp.weixin.qq.com/s/Hkt9TMf6e1Wp2xziw878WQ)
    - [2024-04-17，脑电合成自然语音！LeCun转发Nature子刊新成果，代码开源](https://mp.weixin.qq.com/s/BcV3-3glmdsVF--fpPRU2g)
    - [2024-04-19，Llama 3突然来袭！开源社区再次沸腾：GPT-4级别模型可以自由访问的时代到来](https://mp.weixin.qq.com/s/r6aradJU83GvvVwkFkLXKQ)
  - 微信公众号「机器之心」
    - [2023-02-15，开源方案复现ChatGPT流程！1.62GB显存即可体验，单机训练提速7.73倍](https://mp.weixin.qq.com/s/j8gvD_4ViRE4WQaQlcnmrQ)
    - [2023-02-19，跟李沐学ChatGPT背后技术：67分钟读透InstructGPT论文](https://mp.weixin.qq.com/s/s5WrGn_dQyHrsZP8qsI2ag)
    - [2023-02-21，复旦发布中国版ChatGPT：MOSS开启测试冲上热搜，服务器挤爆](https://mp.weixin.qq.com/s/LjwSozikB6CK5zh2Nd2JHw)
    - [2023-03-13，清华朱军团队开源首个基于Transformer的多模态扩散大模型，文图互生、改写全拿下](https://mp.weixin.qq.com/s/B68hXlFxA9L5jiWiMrEEiA)
    - [2023-03-14，真·ChatGPT平替：无需显卡，MacBook、树莓派就能运行LLaMA](https://mp.weixin.qq.com/s/7bRwX047jkZC53KYbhKARw)
    - [2023-03-15，GPT-4震撼发布：多模态大模型，直接升级ChatGPT、必应，开放API，游戏终结了？](https://mp.weixin.qq.com/s/kA7FBZsT6SIvwIkRwFS-xw)
    - [2023-04-02，3090单卡5小时，每个人都能训练专属ChatGPT，港科大开源LMFlow](https://mp.weixin.qq.com/s/LCGQyNA6sHcdfIIARSNlww)
    - [2023-04-06，CV不存在了？Meta发布「分割一切」AI 模型，CV或迎来GPT-3时刻](https://mp.weixin.qq.com/s/-LWG3rOz60VWiwdYG3iaWQ)
    - [2023-05-14，GPT-4拿下最难数学推理数据集新SOTA，新型Prompting让大模型推理能力狂升](https://mp.weixin.qq.com/s/y8u40qIXm3oWZkvgKOV17Q)
    - [2023-05-20，有手就行？把大象P转身只需拖动鼠标，华人一作DragGAN爆火](https://mp.weixin.qq.com/s/wCvfcmv8OhGqo_fxxZUpKw)
    - [2023-05-21，北京出手通用人工智能：产业创新伙伴计划公布，要推动大模型产业加速落地](https://mp.weixin.qq.com/s/gmclRnJvFnFIc6V-zU67ng)
    - [2023-06-08，给语言大模型加上综合视听能力，达摩院开源Video-LLaMA](https://mp.weixin.qq.com/s/fU_21S5huOJDhrMRcqDcBQ)
    - [2023-06-09，智源「悟道3.0」大模型系列问世，这次不拼参数，开源开放成为主角](https://mp.weixin.qq.com/s/kKqSa0sQOuRuQF7gDy7tIw)
    - [2023-06-10，随时随地，追踪每个像素，连遮挡都不怕的「追踪一切」视频算法来了](https://mp.weixin.qq.com/s/IqcvtfTekSKELLIjX7qRCQ)
    - [2023-06-17，llama.cpp作者创业，用纯C语言框架降低大模型运行成本](https://mp.weixin.qq.com/s/rRx0lhIKIPNumxKBk9tqag)
    - [2023-06-20，650亿参数，8块GPU就能全参数微调：邱锡鹏团队把大模型门槛打下来了](https://mp.weixin.qq.com/s/339iXf2bimusfq6zQmFpWw)
    - [2023-07-08，大语言模型的视觉天赋：GPT也能通过上下文学习解决视觉任务](https://mp.weixin.qq.com/s/CRlQ922r43E_jQSQxlqsDw)
    - [2023-07-09，ChatGPT神器Code Interpreter终于开放，到底怎么用？这里有一份保姆级教程](https://mp.weixin.qq.com/s/VFApvnH1yCxsWCcUP6cSEg)
    - [2023-07-16，获星1.9k，LLM微调神器Lamini上演速度与激情，免费可用](https://mp.weixin.qq.com/s/0I7WpR0rOCfqzb5_z_wzJA)
    - [2023-07-19，更强的Llama 2开源，可直接商用：一夜之间，大模型格局变了](https://mp.weixin.qq.com/s/klFWFXCbjGaWZ7HO1KFZag)
    - [2023-07-20，iPhone、Mac上都能跑，刷屏的Llama 2究竟性能如何？](https://mp.weixin.qq.com/s/q4xVrfAsCzfdeRoquCV5cg)
    - [2023-07-23，我为什么放弃了 LangChain？](https://mp.weixin.qq.com/s/Iwe6M391b2BBWae-HmOIJQ)
    - [2023-07-23，开源的Llama 2背后，有这些年轻华人的力量](https://mp.weixin.qq.com/s/miwc-beG2vrGG1oryCmtpw)
    - [2023-07-31，大神回归学界：何恺明宣布加入 MIT](https://mp.weixin.qq.com/s/MwPMBESMtVTjjAfjGQPsLA)
    - [2023-08-09，百川发布530亿大模型，融入搜索能力：第一时间内测体验已来](https://mp.weixin.qq.com/s/z0xUQH7GRd-YaMFTmynKkg)
    - [2023-08-18，字节跳动类ChatGPT产品「豆包」邀测，我们先试了一下](https://mp.weixin.qq.com/s/DG-Dq9bAz1HpVpF5qxgoug)
    - [2023-08-18，扩散模型「读脑术」，自动化所MindDiffuser清晰重建人脑视觉画面](https://mp.weixin.qq.com/s/FUvd2cU1LjBSERANko88nw)
    - [2023-08-18，稚晖君人形机器人问世：大模型加持，会自己换胳膊，要上生产线造车](https://mp.weixin.qq.com/s/cgfbJgl9enzGXGTb6q6FGA)
    - [2023-08-24，千亿级、数学专用，MathGPT大模型开始公测了](https://mp.weixin.qq.com/s/Atm0RtifVdbZVkt4FE7rOg)
    - [2024-02-23，2770亿美元，英伟达创史上最大单日涨幅，黄仁勋：生成式AI已到临界点](https://mp.weixin.qq.com/s/Wb4ZU-lYoS6Kj0gNezMlaA)
    - [2024-02-23，Stable Diffusion 3震撼发布，采用Sora同源技术，文字终于不乱码了](https://mp.weixin.qq.com/s/KOjeMQJoTLQt6uDBGRMXeQ)
    - [2024-02-23，清华叉院、理想提出DriveVLM，视觉大语言模型提升自动驾驶能力](https://mp.weixin.qq.com/s/v6f29qeZAZOi4NdnwRlvZw)
    - [2024-04-09，纯C语言手搓GPT-2，前OpenAI、特斯拉高管新项目火了](https://mp.weixin.qq.com/s/YMuq9Jo9Nibl1QFbLNxazg)
    - [2024-04-19，开源大模型Llama 3王者归来！最大底牌4000亿参数，性能直逼GPT-4](https://mp.weixin.qq.com/s/KCyL8WTzXutPQ_k0Vl9Vwg)
  - 微信公众号「图灵人工智能」
    - [2023-02-04，盖茨盛赞ChatGPT：人工智能历史意义不亚于“PC或互联网诞生”](https://mp.weixin.qq.com/s/51v_fUjQe3EewwOIxlLghw)
    - [2023-02-06，ChatGPT专题|ChatGPT之父传奇：8岁会编程，16岁出柜，2个月做到月活过亿](https://mp.weixin.qq.com/s/jodwa-a644vECTnrRqCuAA)
    - [2023-02-08，ChatGPT专题|为什么ChatGPT这么强？—— 一文读懂ChatGPT原理！](https://mp.weixin.qq.com/s/QNuKQ2Mgfn5K22JuUe2dHA)
    - [2023-02-11，ChatGPT专题|万字拆解！追溯ChatGPT各项能力的起源](https://mp.weixin.qq.com/s/4l0ADjdsCxSVvBeVKxSqWA)
    - [2023-02-15，ChatGPT专题|ChatGPT是第一个真正意义的人工通用智能](https://mp.weixin.qq.com/s/V7gptx740dDtVyQAgdhnqA)
    - [2023-02-16，ChatGPT专题|ChatGPT 算法原理](https://mp.weixin.qq.com/s/aIzwuATN71etbUrrQWYOkA)
    - [2023-02-16，ChatGPT专题|由ChatGPT反思大语言模型（LLM）的技术精要](https://mp.weixin.qq.com/s/SthaVFuAzvPnpCVdwaZYdA)
    - [2023-02-17，ChatGPT专题|ChatGPT背后真正的英雄：OpenAI首席科学家Ilya Sutskever的信仰之跃](https://mp.weixin.qq.com/s/EnRAcqiugR_xr7Mn0WJXLA)
    - [2023-02-18，ChatGPT专题|ChatGPT学了一门清华慕课，还拿到了课程证书](https://mp.weixin.qq.com/s/enaw41QEyiJ0ecNmjyEctw)
    - [2023-02-18，ChatGPT专题|关于GPT，人工智能，以及人的一些思考](https://mp.weixin.qq.com/s/SBpnmsc11C4fcH5xeftQdQ)
    - [2023-02-19，ChatGPT 专题：万字长文解释 ChatGPT 在做什么，以及为什么它能发挥作用？](https://mp.weixin.qq.com/s/gt0YxLG9ZW2wIg5rzfBhKw)
    - [2023-05-14，清华大学邓志东教授——通用大模型：深度学习的极限发展](https://mp.weixin.qq.com/s/J-JMBiBDBqXmfDWwKbze5g)
    - [2023-05-21，从 GPU 到 ChatGPT](https://mp.weixin.qq.com/s/oobtNmLlvwZyheAk5jADmA)
    - [2023-07-29，语言模型的前世今生与GPT的人生哲学](https://mp.weixin.qq.com/s/uHyz2Rt05GtH6GRRgCFUGQ)
    - [2023-08-06，张钹院士：GPT时代的人工智能安全](https://mp.weixin.qq.com/s/FJ-jhD_b7o-5D4ikKcNcEw)
    - [2023-08-15，谷歌发现大模型「领悟」现象！训练久了突然不再死记硬背，多么痛的领悟](https://mp.weixin.qq.com/s/d9K5fkgmvIkGQRPGIiSPaA)
    - [2023-08-17，谷歌：大模型不仅有涌现能力，训练时间长了还有「领悟」能力](https://mp.weixin.qq.com/s/FEuViHRAYvQvKS5iCtX86Q)
  - 微信公众号「硅星人」
    - [2022-12-03，行走的代码生成器：chatGPT要让谷歌和程序员“下岗”了](https://mp.weixin.qq.com/s/DXzZ_5RrRbVe5bWkpwFV6Q)
    - [2023-01-18，微软下个十年的想象力，藏在ChatGPT里](https://mp.weixin.qq.com/s/xjNipZ77I3eKbeYU5ZztZQ)
    - [2023-01-28，ChatGPT又赢了：带动股价涨三倍，成考试神器](https://mp.weixin.qq.com/s/BCfI_IhbIvLaAphYheM7yQ)
    - [2023-02-07，搜索大变天！谷歌推出Bard对抗ChatGPT，打响保卫战](https://mp.weixin.qq.com/s/33-Cg7Vn3Pmzuv_2IMHLzg)
    - [2023-02-16，谁拖了中国ChatGPT的后腿？](https://mp.weixin.qq.com/s/66ILghJKHjQhEVJ3r1xi7A)
    - [2023-02-24，OpenAI造就硅谷新“黑帮”：ChatGPT爆火背后的神秘大佬、技术版图和资本故事](https://mp.weixin.qq.com/s/eMwGbvxE_pCr1r1k18_yrA)
    - [2023-02-25，英伟达再度站上风口](https://mp.weixin.qq.com/s/_OM1_Pf1GLHW3zuF-3F93Q)
    - [2023-03-03，ChatGPT的战争不会浓缩于一个晚上](https://mp.weixin.qq.com/s/GJ94vpO9sRrXttdBo9oD2w)
    - [2023-03-15，OpenAI发布GPT-4：能识图能算税，ChatGPT摆脱Chat，再次进化](https://mp.weixin.qq.com/s/JahPijUPjxrzuLhq0esIUg)
    - [2023-03-17，GPT-4撑腰，Office全家桶集体升级，微软向谷歌丢出“王炸”](https://mp.weixin.qq.com/s/Ef_4FesHTP83NjZ3Knu5pA)
    - [2023-03-22，对抗ChatGPT，谷歌Bard公测炸场了：巨头开启AI对决](https://mp.weixin.qq.com/s/TkfaTNFz4bM6EnHygNymqw)
    - [2023-03-25，联网之后的ChatGPT，已经远不止“iPhone时刻”那么简单](https://mp.weixin.qq.com/s/_vn4RAqtRaNlBNP9W1sQcA)
    - [2023-03-30，AI太强，人类危险？马斯克、图灵奖得主紧急呼吁暂停GPT-4模型后续研发](https://mp.weixin.qq.com/s/QrrVefyvrOQ8IbAVzWA-6w)
    - [2023-04-01，OpenAI秘史公开：马斯克和奥特曼的战争，与钱无关](https://mp.weixin.qq.com/s/h_juJuhjVt8z-uu4qjaUFw)
    - [2023-04-05，这些让人惊呼好用的神器背后，原来都是ChatGPT](https://mp.weixin.qq.com/s/KL6OFAhPfr_OC80I_W6b3g)
    - [2023-04-07，Meta新模型“分割一切”：抠图完成究极进化，计算机视觉迎来GPT-3时刻](https://mp.weixin.qq.com/s/UUSmg6M5F6FJDs2i_-98dQ)
    - [2023-06-30，AI创投圈嗨爆了：成立仅一年超级黑马融资13亿美元，大热门却只筹到2500万？](https://mp.weixin.qq.com/s/s195icDInYks4f4ICLpgLQ)
    - [2023-07-07，开发者看过来：GPT-4 API接口全面开放了！](https://mp.weixin.qq.com/s/BFbZVmwogrTJCtm28Y-wkQ)
    - [2023-07-19，Meta“搞大事”了：发布GPT“平替”Llama 2，开源、免费、还可商用！](https://mp.weixin.qq.com/s/RIpYez1K-Q6_CCRpPT4aLQ)
  - 微信公众号「通用人工智能联盟」
    - [2023-01-31，通用人工智能技术综述（一）](https://mp.weixin.qq.com/s/s1A0dHDs0ptNLIKXNivB8g)
    - [2023-02-01，通用人工智能技术综述（二）](https://mp.weixin.qq.com/s/dBAHHdcQPbogxyOv-yTvzg)
    - [2023-02-02，通用人工智能综述（三）](https://mp.weixin.qq.com/s/PjUPumRc9fFCmien71odsw)
    - [2023-02-04，通用人工智能技术综述（四）](https://mp.weixin.qq.com/s/3w-T6V9h3zgJUFxb2D7FXQ)
    - [2023-02-08，通用人工智能技术综述（五）](https://mp.weixin.qq.com/s/Bz4-AQ6UcFKTCSKoDwUrcg)
    - [2023-02-12，ChatGPT的开发及部署成本略析](https://mp.weixin.qq.com/s/cqfUl2lBGhWtVj6NbWbuew)
  - 微信公众号「计算机视觉研究院」
    - [2023-02-09，计算机视觉研究院亲自体验ChatGPT的感受，太疯狂了！](https://mp.weixin.qq.com/s/82Z3cODnPbwpStXIhnuJyw)
    - [2023-02-16，Image GPT——手把手教你搭建](https://mp.weixin.qq.com/s/gH_K_9Qo67HoNnSOnBevqw)
    - [2023-02-20，7 Papers | 超越GPT 3.5的小模型；对ChatGPT摸底考试](https://mp.weixin.qq.com/s/_HV9atcakv0sWD5X4tloPw)
    - [2023-06-21，RevCol：大模型架构设计新范式，给神经网络架构增加了一个维度！](https://mp.weixin.qq.com/s/vsia8h5LI4zs-lES0u_dcw)
    - [2023-06-21，走向CV的通用人工智能：从GPT和大型语言模型中汲取的经验教训 (上)](https://mp.weixin.qq.com/s/6Sl8ELrA9zulal5iJoQXJA)
    - [2023-07-03，ChatGPT实践应用和大模型技术解析](https://mp.weixin.qq.com/s/4GFc1e06hRjK4crfVPc2JA)
    - [2023-07-03，DeepSpeed ZeRO++：降低4倍网络通信，显著提高大模型及类ChatGPT模型训练效率](https://mp.weixin.qq.com/s/sSIw7y-_vcN_y80b1tP6oQ)
    - [2023-08-16，轻量级MobileSAM：比FastSAM快4倍，处理一张图像仅需10ms（附源代码）](https://mp.weixin.qq.com/s/3VhGKWpKTFY3u8hVJUYp_A)
  - 微信公众号「江大白」
    - [2023-02-15，万字拆解，ChatGPT各项能力的起源追溯](https://mp.weixin.qq.com/s/l0uGPO4vdFQzwCSP-HQQgg)
    - [2023-03-02，ChatGPT团队背景研究报告，大厂不再是顶尖人才第一选择！](https://mp.weixin.qq.com/s/F_9fChIMkuZLoUfhnenwAw)
    - [2023-03-03，行业热点 | ChatGPT数据集深度解密](https://mp.weixin.qq.com/s/mQiZIf-1QolCkX-2jTUa5Q)
    - [2023-03-13，北大团队搞出ChatExcel，说人话自动处理表格，免费且不限次使用！](https://mp.weixin.qq.com/s/H8aG9AewM0npJCpA2A0YGQ)
    - [2023-03-23，脑洞大开，如何利用ChatGPT搞科研？](https://mp.weixin.qq.com/s/HZvUfwpmPQC6OOX2Qyr-JQ)
    - [2023-03-29，GPT-4 的独立创业之路，一个人就是一家公司！](https://mp.weixin.qq.com/s/Qu-OXSoDS5hmdPe6EENM4w)
    - [2023-03-30，开源版ChatGPT项目，30分钟训完，性能堪比GPT3.5！（附源码）](https://mp.weixin.qq.com/s/x-UYyeAQc8NF2TiW8XLJHg)
    - [2023-04-03，学术版专用Chatgpt火热开源，科研工作必备，附源码！](https://mp.weixin.qq.com/s/19jGbV37DhkihhKAxqBk7w)
    - [2023-04-14，阿里版GPT通义千问实测来了！数学、编程、情书全套整活](https://mp.weixin.qq.com/s/a5NRdeR703CVBsG9xYgUlA)
    - [2023-05-12，MedSAM在医学领域，图像分割中的落地应用（附论文及源码）](https://mp.weixin.qq.com/s/JJ0umIzJ5VKJ87A_jnDtOw)
    - [2023-05-16，算法工程师如何优雅地使用ChatGPT?](https://mp.weixin.qq.com/s/FHdwnTPM6kOsMvAPcegrwg)
    - [2023-06-03，深入浅出，Stable Diffusion完整核心基础讲解](https://mp.weixin.qq.com/s/5HnOAmUKDnOtf2xDX2R9Xg)
    - [2023-06-03，分割一切模型(SAM)的全面综述调研](https://mp.weixin.qq.com/s/39imonlyIdSHYW9VnQhOjw)
    - [2023-06-10，万字长文，解析大模型在自动驾驶领域的应用](https://mp.weixin.qq.com/s/QGF8ssfB6Rk350ro-ohIHA)
    - [2023-06-21，AIGC 10亿参数模型进手机！15秒即可出图，飞行模式也能用！](https://mp.weixin.qq.com/s/chy2qMyD5ILTP2R6DpL4Yg)
    - [2023-06-23，硬核详解SAM TensorRT模型，实战转换教程](https://mp.weixin.qq.com/s/Y5Y1b3iLcJWgQ2i3pPFNyg)
    - [2023-06-26，CV通用人工智能：GPT和大语言模型带来的启发和感悟](https://mp.weixin.qq.com/s/Vu7svINOBSXqz9vjMgOjSw)
    - [2023-06-30，MobileSAM来啦，比SAM小60倍，速度和效果双赢（附源码）](https://mp.weixin.qq.com/s/BRv9GDle40QS--Tt-hNPjg)
    - [2023-07-07，中科院多语言大模型：BayLing(百聆)，性能媲美GPT，可在线体验！](https://mp.weixin.qq.com/s/bvn70GNlU3zHJSDHV5BsRA)
    - [2023-07-10，十分钟读懂Diffusion：图解Diffusion扩散模型原理](https://mp.weixin.qq.com/s/54g-3foInJWI1wnB0X4odA)
    - [2023-07-14，AI算法应用，模型部署服务代码实战](https://mp.weixin.qq.com/s/vFRTHcWjerFDlgV9TV6FWQ)
    - [2023-08-07，GPT-5出世，需5万张H100！全球需求43万张， 英伟达GPU陷短缺风暴](https://mp.weixin.qq.com/s/l1Un2V6KreyA1djyc3juFA)
    - [2023-08-15，万字长文，深入浅出Llama搭建及源码解读](https://mp.weixin.qq.com/s/qDLVH9ADKrHySvPtr3carw)
  - 微信公众号「WeThinkln」
    - [2023-02-12，Rocky和ChatGPT“谈笑风生”的日子 |【AI行研&商业价值分析】](https://mp.weixin.qq.com/s/rV6J6UZgsJT-4HI49GBBaw)
    - [2023-02-26，深入浅出解析ChatGPT引领的科技浪潮 |【AI行研&商业价值分析】](https://mp.weixin.qq.com/s/FLLtb_9shzFmH1wpV7oP_Q)
    - [2023-06-22，深入浅出解析LoRA完整核心基础知识 |【算法兵器谱】](https://mp.weixin.qq.com/s/n-17rH0PrwHYZz0g58Cyiw)
  - 微信公众号「夕小瑶科技说」
    - [2023-05-31，一个技巧，让ChatGPT学会复杂编程，编程水平逼近人类程序员！](https://mp.weixin.qq.com/s/QgL5-fTA99InHsoI7hJ8lw)
    - [2023-07-06，刚刚！OpenAI宣布，斥巨资建立「超级对齐」团队！向人类意图看齐](https://mp.weixin.qq.com/s/K7e6mfCA7eWN_armMBH9UA)
    - [2023-07-09，羊驼再度进化，“长颈鹿版”LongLLaMA 来啦，上下文长度冲向 100K ，性能不减](https://mp.weixin.qq.com/s/XzaET7WfrNpOf-zdiSxrig)
    - [2023-07-19，更强的Llama 2开源，可直接商用：一夜之间，大模型格局变了](https://mp.weixin.qq.com/s/PJyFoLP7IBxjbswq-NBEkA)
    - [2023-07-31，强推！大语言模型『百宝书』，一文缕清所有大模型！](https://mp.weixin.qq.com/s/7K5cMlLekUUtKwEtCHwGtg)
    - [2023-08-10，大模型的数据隐私问题有解了，浙江大学提出联邦大语言模型](https://mp.weixin.qq.com/s/5Ejc2JNefZK0lockU70l-Q)
    - [2023-08-17，文心一言杀疯了！大模型社区、插件系统来了，码农神器发布，AI原生时代降临](https://mp.weixin.qq.com/s/M3WKKr7CvCHgZQgKVfR3SA)
    - [2024-02-23，符尧大佬一作发文，仅改训练数据，就让LLaMa-2上下文长度扩展20倍！](https://mp.weixin.qq.com/s/sTxoxhyG6mAm5fI8tKdMPw)
    - [2024-04-01，今日arXiv最热NLP大模型论文：Github万星！北航发布零代码大模型微调平台LlamaFactory](https://mp.weixin.qq.com/s/jJ5hItGNz91TiaDrdfYwUg)
    - [2024-04-10，黑科技 ！AI届的“指环王”，已接入ChatGPT和Gemini！一个戒指可操控手机和智能家居，韩国公司研发](https://mp.weixin.qq.com/s/kS3BufC2_KBzxQ7_ZkPAvQ)
  - 微信公众号「所向披靡的张大刀」
    - [2023-04-07，分割大一统——Segment Anything深度体验](https://mp.weixin.qq.com/s/qtk1Ds3hdNi4NOwrw2tDrg)
  - 微信公众号「算法邦」
    - [2023-03-06，没有这些，别妄谈做ChatGPT了](https://mp.weixin.qq.com/s/BwFUYFbkvAdDRE1Zqt_Qcg)
    - [2023-03-29，GPT-4将如何冲击计算机视觉领域？](https://mp.weixin.qq.com/s/KIFb24nxEvxIlyG23sy8bQ)
    - [2023-04-01，GPT-4的前世、今生和未来！](https://mp.weixin.qq.com/s/QNSbLdj5MdHuatdxW74QPQ)
    - [2023-04-03，ChatGPT成功背后的秘密，开源了！](https://mp.weixin.qq.com/s/V6Qgdf6JzfT7KGWVgNqWsQ)
    - [2023-04-05，如何与ChatGPT4结对编程提升研发效率](https://mp.weixin.qq.com/s/UJgNjIdQ13SuGHy2p7XE0Q)
    - [2023-08-05，强推！伯克利AI博士详解Llama 2的技术细节](https://mp.weixin.qq.com/s/_buXlspjvc_rt50AVSBslQ)
    - [2023-08-20，堪比ChatGPT！Meta华人提出「牧羊人」Shepherd，LLaMA 70亿参数微调，评估模型生成给出建议](https://mp.weixin.qq.com/s/IIQMEAkqYdT-Ye2M5FjopA)
  - 微信公众号「极市平台」
    - [2023-03-28，GPT系列来龙去脉大起底（一）｜第一代 GPT：无标注数据预训练生成式语言模型](https://mp.weixin.qq.com/s/wzZOjBJYtBpVZB-PzZenmQ)
    - [2023-04-06，GPT系列来龙去脉大起底（一）｜GPT-2：GPT 在零样本多任务学习的探索](https://mp.weixin.qq.com/s/YekKHeJD0KcCJ_73Wriuqw)
    - [2023-04-06，压缩下一个 token 通向超过人类的智能](https://mp.weixin.qq.com/s/UCB9-XPxZ0UA-kifakudFQ)
    - [2023-07-08，十分钟读懂Diffusion：图解Diffusion扩散模型](https://mp.weixin.qq.com/s/vZnnefyVgNNiP92GpSGFxQ)
  - 微信公众号「计算机视觉与机器学习」
    - [2023-04-06，不止 GPT4 ，大语言模型的演变之路！](https://mp.weixin.qq.com/s/YhvtxqBszvfcmtLvZgWqhw)
    - [2023-04-04，GPT-4 版“贾维斯”诞生，国外小哥用它 4 分钟创建网站、聊天就能创建 GitHub repo......](https://mp.weixin.qq.com/s/agtQeScBNBvSX1yqLTW4JQ)
    - [2023-04-03，CVPR 2023 | 模块化MoE将成为视觉多任务学习基础模型](https://mp.weixin.qq.com/s/VsGOio9mn-o82bWI1MMUcA)
    - [2023-05-15，Nature发文！ChatGPT加速科研编程](https://mp.weixin.qq.com/s/MoXAnTJIV4JTVppfmBccHA)
  - 微信公众号「CV技术指南」
    - [2023-04-07，3090单卡5小时，每个人都能训练专属ChatGPT，港科大开源LMFlow](https://mp.weixin.qq.com/s/h6zbAVgFpW0ccdEHjLFpdQ)
    - [2023-04-07，上线一天，4k star | Facebook：Segment Anything](https://mp.weixin.qq.com/s/G7xeuZE3vHuujQrDxIrePA)
  - 微信公众号「计算机视觉工坊」
    - [2023-04-07，超震撼！Meta发布「分割一切」AI 模型！](https://mp.weixin.qq.com/s/_IbadabLJnvv1_a-NsAJfg)
    - [2023-04-08，CV开启大模型时代！谷歌发布史上最大ViT：220亿参数，视觉感知力直逼人类](https://mp.weixin.qq.com/s/ur2WTw95pUduxh9EYULR_Q)
  - 微信公众号「新智元」
    - [2023-02-03，60天月活破亿，ChatGPT之父传奇：16岁出柜，20岁和男友一同当上CEO](https://mp.weixin.qq.com/s/W1xfLgZXWL3lfP4_54SQKw)
    - [2023-03-17，微软深夜放炸弹！GPT-4 Office全家桶发布，10亿打工人被革命](https://mp.weixin.qq.com/s/YgiurOE0uZ7lRDx1ehpbhQ)
    - [2023-05-03，AI通灵！类ChatGPT模型解码大脑信息，准确率高达82%](https://mp.weixin.qq.com/s/4KbtJ5cfur7KrWWijjQtIA)
    - [2023-05-20，GAN逆袭归来！清华校友论文引爆AI绘图圈，一秒把大象P转身，Diffusion黯然失色](https://mp.weixin.qq.com/s/DBLMAEbVw6v4xH94-5Zl3w)
    - [2023-06-20，GPT-Engineer一夜爆火！一个提示生成整个代码库，GitHub狂飙19k星](https://mp.weixin.qq.com/s/fjrKWsjgsiCXBar9r9F4XQ)
    - [2023-07-12，Transformer八子全部叛逃谷歌！最后一位共同作者月底离职创业](https://mp.weixin.qq.com/s/ltQsq6Z36nvPSRa4IC8a_A)
    - [2023-07-20，Llama 2宇宙大爆炸！伯克利实测排第8，iPhone本地可跑，一大波应用免费玩，LeCun狂转](https://mp.weixin.qq.com/s/tc2Tz_K30358t07w-IHxfQ)
    - [2023-07-29，ChatGPT羊驼家族全沦陷！CMU博士击破LLM护栏，人类毁灭计划脱口而出](https://mp.weixin.qq.com/s/9UaYiLoIaXixfE8Ka8um5A)
    - [2023-08-18，天才少年稚晖君智元机器人走路进场！AI模型做大脑，目标售价20万以内](https://mp.weixin.qq.com/s/0SE0w0ne3npFjrEdjYhZdg)
    - [2023-08-19，波士顿大学「鸭嘴兽-70B」登顶Hugging Face大模型排行榜！高效数据集+独特LoRA微调是关键](https://mp.weixin.qq.com/s/RED36cGaqrhOOC5SGD9buw)
    - [2023-08-22，GPT-4没有意识！但图灵奖得主Bengio等88页论文暗示「天网」迟早降临](https://mp.weixin.qq.com/s/VfUM_y7DdShHwhbrdkzoqA)
    - [2023-09-10，H100推理飙升8倍！英伟达官宣开源TensorRT-LLM，支持10+模型](https://mp.weixin.qq.com/s/xcNQBG69XkS6mOstzqROAw)
    - [2024-02-22，全球最强开源大模型一夜易主！谷歌Gemma 7B碾压Llama 2 13B，今夜重燃开源之战](https://mp.weixin.qq.com/s/fpKW9UV7_S-FiFhiIet82g)
    - [2024-02-23，Stable Diffusion 3深夜横空出世！模型与Sora同架构，也能「理解」物理世界](https://mp.weixin.qq.com/s/PU_VCbFU29rkfgoIm2as0g)
    - [2024-04-07，Llama提速500%！谷歌美女程序员手搓矩阵乘法内核](https://mp.weixin.qq.com/s/2ROw_Tmmh4NHf8WOiwnJLg)
    - [2024-04-09，1000行C语言搓出GPT-2！AI大神Karpathy新项目刚上线就狂揽2.5k星](https://mp.weixin.qq.com/s/_W2GlbO8nAfpLPtRtQJ-yw)
    - [2024-04-19，全球首个「开源GPT-4」出世！Llama 3震撼发布，Meta AI免登录可用](https://mp.weixin.qq.com/s/jiEfe60I446jrDzZxDh_Vg)
    - [2024-04-25，国产大模型卷翻机器人！这些火遍全网的机器人，都装上了星火「大脑」](https://mp.weixin.qq.com/s/ZU_oOH4-s6Sd6nD_-jmbgw)
  - 微信公众号「智东西」
    - [2023-02-06，ChatGPT版搜索引擎突然上线，科技巨头们坐不住了！](https://mp.weixin.qq.com/s/lncJm6hmK3AQNF2paWI5Dw)
    - [2023-04-07，ChatGPT和Matter两大风口汇合！AWE同期AIoT智能家居峰会月底举行，首批嘉宾公布](https://mp.weixin.qq.com/s/cuI8sSff_zGiLtwukAcLRw)
    - [2023-04-23，BroadLink CEO刘宗孺：ChatGPT助推全屋智能管家式变革](https://mp.weixin.qq.com/s/t4BPrvYT8oF8lGKutjpJtQ)
    - [2023-04-23，复旦MOSS升级版开源上线；马斯克启动TruthGPT；海康训练出百亿参数CV大模型丨AIGC大事周报](https://mp.weixin.qq.com/s/gBDcHw1SFSCWpJIxeC5vHg)
    - [2023-05-16，北京打响大模型地方战第一枪：公布通用人工智能发展21项措施](https://mp.weixin.qq.com/s/HdTkIaLL33ZMhrQ00fVYZQ)
    - [2023-07-25，重磅，ChatGPT老板官宣“世界币”，价格暴涨、用户超两百万，要给全世界每个人发钱](https://mp.weixin.qq.com/s/MVfp_wZIxtLlADIN4hoN_A)
    - [2023-08-15，讯飞星火V2.0突破代码能力，一个指令生成贪吃蛇游戏，10分钟开发“凌空手写”](https://mp.weixin.qq.com/s/544ysBQ0C_j9mD2NAx-cyg)
  - 微信公众号「CSDN」
    - [2023-03-25，ChatGPT 已成为下一代的新操作系统！](https://mp.weixin.qq.com/s/MwrMhVydbhpP6c0AvPp8oQ)
    - [2023-04-06，CV 迎来 GPT-3 时刻，Meta 开源万物可分割 AI 模型和 1100 万张照片，1B+掩码数据集！](https://mp.weixin.qq.com/s/spBwU0UecbxbEl88SA4GJQ)
    - [2023-04-11，最爱 ChatGPT，每天编码 300 行，月薪 8k-17k 占比骤减！揭晓中国开发者真实现状](https://mp.weixin.qq.com/s/P6KjP1Xv85wSWjuxvMzK7Q)
    - [2023-05-10，在 GitHub 上“搞事”，Meta 开源 ImageBind 新模型，超越 GPT-4，对齐文本、音频等 6 种模态！](https://mp.weixin.qq.com/s/wd5vnGEQaVjpLGWYUAo-gA)
    - [2023-05-17，OpenAI CEO 在美国国会首秀：回应对 AI 的一切质疑，主动要求接受监管！](https://mp.weixin.qq.com/s/B6AXGXgwELNrG4FffTfiug)
    - [2023-07-11，ChatGPT 最强代码解释器突破“封印”：30 秒出片、5 分钟制作游戏、可视化分析...样样精通！](https://mp.weixin.qq.com/s/VrxL0Ufxd0meMaY_exttCQ)
    - [2023-07-19，格局打开，Meta 发布免费商业应用的开源 AI 模型 Llama 2，网友：微软又赢麻了！](https://mp.weixin.qq.com/s/DUCZ6LmaaoD6LTiAroM9xQ)
    - [2023-08-16，从失望到精通：AI 大模型实践与实用技巧](https://mp.weixin.qq.com/s/6QwJrmHS7vY1jo4WzyG-2A)
    - [2024-02-22，Google炸场！最强轻量级、开放模型Gemma发布，个人PC就能用，内部员工：强是强，但名字取得让我混乱！](https://mp.weixin.qq.com/s/LMsUnkbepab0KKqK59f7Gg)
  - 微信公众号「刘润」
    - [2023-02-08，ChatGPT：一个人不管有多大的梦想，还是要有盖世武功](https://mp.weixin.qq.com/s/Dd28kONcjwiBYPuDUD8R7g)
    - [2023-02-09，ChatGPT：你来了，那我怎么办？](https://mp.weixin.qq.com/s/3wikMRAJqZtWHaC5dUVgbQ)
    - [2023-02-12，ChatGPT引爆新一轮科技军备赛](https://mp.weixin.qq.com/s/4oofzJywBsG9SF6Hb48WNQ)
    - [2023-02-14，ChatGPT创始人，给我们上的8堂课](https://mp.weixin.qq.com/s/js-fY2nJBAr_pZItTw-PMg)
    - [2023-06-21，ChatGPT：一个人不管有多大的梦想，还是要有盖世武功](https://mp.weixin.qq.com/s/5FG6YIoWUxQ_aB0k5iWTCg)
    - [2023-06-27，今后，好好做私域业务吧...](https://mp.weixin.qq.com/s/9pnvoWpMMs8FV-eR_P_M7w)
  - 微信公众号「AI算法与图像处理」
    - [2023-02-16，推荐一个方便好用的 ChatGPT 客户端！](https://mp.weixin.qq.com/s/Lu0WqBxRcACfucgmTk2OEw)
  - 微信公众号「中国图象图形学报」
    - [2023-02-16，编委动态 | 浅析ChatGPT：历史沿革、应用现状及前景展望](https://mp.weixin.qq.com/s/EgiBEb7D4HkaKtjmsMnRHA)
  - 微信公众号「脑机接口社区」
    - [2023-02-15，ChatGPT发展历程、原理、技术架构详解和产业未来](https://mp.weixin.qq.com/s/LhcqK6W7OTB0Y1LfZIsGfA)
  - 微信公众号「中国科学院自动化研究所」
    - [2023-02-15，嗨ChatGPT，人类对你最好奇的是什么呢？这篇文章一一解答！丨智言智语](https://mp.weixin.qq.com/s/BYCemIdTx2kZ9jotF13u2w)
  - 微信公众号「玩转VS Code」
    - [2023-02-16，目前最火的 ChatGPT 开源项目！](https://mp.weixin.qq.com/s/E2-MrsKfvNxIvuW7h4NT6Q)
  - 微信公众号「人工智能学家」
    - [2023-02-15，人机交互新时代：多维度快速看清ChatGPT（附下载）](https://mp.weixin.qq.com/s/MHqn53ZFjXPt8tC1d9oCOA)
    - [2023-05-19，ChatGPT的工作原理，这篇文章说清楚了](https://mp.weixin.qq.com/s/mt9RH3loOfo3--s1aKVTXg)
  - 微信公众号「新机器视觉」
    - [2023-02-13，ChatGPT 算法原理](https://mp.weixin.qq.com/s/DYRjmJ7ePTqV1RFkBZFCTw)
  - 微信公众号「投行圈子」
    - [2023-02-11，ChatGPT研究框架（80页PPT）](https://mp.weixin.qq.com/s/eGLqpTvFztok3MWE3ISc2A)
  - 微信公众号「机器学习算法那些事」
    - [2023-02-08，多模态版ChatGPT，拿下视觉语言新SOTA， 代码已开源](https://mp.weixin.qq.com/s/lsRSzwsLiTo6anPnKFa-4A)
    - [2024-04-23，有位大佬逐模块解析transformer结构](https://mp.weixin.qq.com/s/MmTrUTsf1zMcn3YvYDTGIA)
  - 微信公众号「机器学习算法工程师」
    - [2023-04-08，CV突然进入GPT4时代！Meta和智源研究院发布「分割一切」AI 模型](https://mp.weixin.qq.com/s/9zTX0awkGPc9kfoX2QpDIg)
    - [2023-05-04，开源版Imagen来了！效果完全碾压Stable Diffusion！](https://mp.weixin.qq.com/s/Ipsw1smfINxcJT2sY00-QQ)
    - [2023-05-17，StarCoder: 最先进的代码大模型](https://mp.weixin.qq.com/s/XrY-pgBQ-DoTH_0olJ7ytw)
  - 微信公众号「人工智能与算法学习」
    - [2023-02-15，ChatGPT数据集之谜](https://mp.weixin.qq.com/s/CFgsiJ7a2mXQNAWkQxScYQ)
    - [2023-03-10，王炸！微软发布Visual ChatGPT：视觉模型加持ChatGPT实现丝滑聊天](https://mp.weixin.qq.com/s/jQd0xujid66CrcBrhhZoLQ)
    - [2023-08-21，大模型榜单再次刷新，比Llama 2更强的大模型来了](https://mp.weixin.qq.com/s/5UYfqA8LES936V9pL8g-UA)
    - [2023-09-05，DoctorGPT 模型：为每个人提供一个私人医生](https://mp.weixin.qq.com/s/JAc2GlBJOA1rPfZHGVwbmQ)
    - [2024-02-21，全网最细致的Sora技术推演](https://mp.weixin.qq.com/s/xl56nMgqNK5uih7uGoOU3w)
  - 微信公众号「量子学派」
    - [2023-02-10，封杀这个公式，ChatGPT智商将为零](https://mp.weixin.qq.com/s/l1Qxe3rGTYuIumHq02exsg)
    - [2023-02-10，ChatGPT，一种更中心化的权力？](https://mp.weixin.qq.com/s/-qmccVnv_rpKVdFP6x4GNg)
  - 微信公众号「42章经」
    - [2023-02-13，我是怎样用一周时间研究 ChatGPT 的？](https://mp.weixin.qq.com/s/obVI3ENpMgaq4AKZs6Hw1w)
  - 微信公众号「人工智能技术与咨询」
    - [ChatGPT四大应用主线及相关细分场景](https://mp.weixin.qq.com/s/f8cmRVs0ys7FNyNU1qbP6g)
  - 微信公众号「应用语言学研习」
    - [2023-02-17，如何利用ChatGPT搞科研？](https://mp.weixin.qq.com/s/sW_utRBS_jJAaWfGo_eT5g)
  - 微信公众号「机器之能」
    - [2023-03-22，比尔·盖茨：AI时代已经开启，GPT是40年来最具革命性技术](https://mp.weixin.qq.com/s/j3D7g_1HeKZbznOqqU2pxw)
    - [2024-04-19，开源大模型Llama 3王者归来！最大底牌4000亿参数，性能直逼GPT-4](https://mp.weixin.qq.com/s/eTN6kGFiJLoN0HKvAyWFug)
  - 微信公众号「机器学习研究组订阅」
    - [2023-03-26，震惊科学界！微软154页研究刷屏：GPT-4能力接近人类，「天网」初现？](https://mp.weixin.qq.com/s/C0qwDb_ASCbmP8sHgH97Jg)
  - 微信公众号「浮之静」
    - [2022-12-14，流量密码：ChatGPT 开源的一些思考](https://mp.weixin.qq.com/s/-lpQycfKVQ1gLKjoMrTvpA)
    - [2023-02-08，ChatGPT 扫盲指南](https://mp.weixin.qq.com/s/4RczQBdAmnYSdlhMBcXcZA)
    - [2023-03-01，一文读懂 OpenAI](https://mp.weixin.qq.com/s/_ovmBsJ7EQr_k4JnSKtuLw)
    - [2023-03-15，AI 里程碑：GPT-4 发布了！](https://mp.weixin.qq.com/s/n8ttVSJmd44sBdpnL3Whxw)
    - [2023-03-27，AI 浪潮下的一些浅思](https://mp.weixin.qq.com/s/1TYrtufxtLcMy0RolNAbhg)
    - [2023-05-21，ChatGPT 探索：英语学习小助手](https://mp.weixin.qq.com/s/QGURRcD3QOM7-4x0CumX4Q)
    - [2023-05-25，ChatGPT 桌面应用 v1.0.0 发布啦！](https://mp.weixin.qq.com/s/jbQCws2G8hNdytIMPHHg0w)
    - [2023-06-22，GPT-4 混合模型：8 个 2200 亿参数的专家模型？](https://mp.weixin.qq.com/s/PEqusMr1p4-T5piWUzbfzA)
    - [2023-07-11，ChatGPT：Code Interpreter == GPT-4.5？](https://mp.weixin.qq.com/s/cexXvkbkxZNF8-ZD9Zplyg)
    - [2023-07-12，ChatGPT：GPT-4 架构揭秘](https://mp.weixin.qq.com/s/B-XQRuns_U9Li5jXW-sOuw)
    - [2023-08-06，LangUI：AI 与 GPT 项目专属开源组件库](https://mp.weixin.qq.com/s/Uszrre1L__91aIYEGl32uA)
  - 微信公众号「学术头条」
    - [2023-02-22，揭秘ChatGPT背后的AI“梦之队”：90后科研“后浪”展示强大创新能力｜智谱研究报告](https://mp.weixin.qq.com/s/sncE01utzu_-r3dLFYU5QA)
    - [2023-07-19，更强的Llama 2开源，可直接商用：一夜之间，大模型格局变了](https://mp.weixin.qq.com/s/TR8DdLLUEZGL4Q2Wan8PpQ)
  - 微信公众号「人工智能研究」
    - [2023-03-11，哈工大NLP研究所ChatGPT调研报告发布！](https://mp.weixin.qq.com/s/u17VEv0VM8MXYyB7jcV-yA)
  - 微信公众号「OpenFPGA」
    - [2023-03-13，在FPGA设计中怎么应用ChatGPT？](https://mp.weixin.qq.com/s/BvCFoAi9tAvSs4QS4BFRdA)
    - [2023-03-27，ChatGPT推荐的开源项目，到底靠不靠谱？](https://mp.weixin.qq.com/s/_ERFebXaLUbF3EQs_ZyPIQ)
  - 微信公众号「AI科技评论」
    - [2023-03-14，何恺明 MIT 最新演讲：未来工作将聚焦 AI for science](https://mp.weixin.qq.com/s/8oiHz34DpfDJmT4IPzU8IA)
    - [2023-08-10，清华提出开源工具学习框架，接入真实世界 16000+API, 效果达 ChatGPT](https://mp.weixin.qq.com/s/pg4oeybuy0tuXK_7K5zq3w)
  - 微信公众号「AI科技大本营」
    - [2023-07-19，微软又赢麻了！联合 Meta 发布免费商业应用的开源 AI 模型 Llama 2](https://mp.weixin.qq.com/s/gBLkqSpHkRBK6nhSUnMTUA)
  - 微信公众号「HelloGitHub」
    - [2023-03-17，GPT-4 来了！这些开源的 GPT 应用又要变强了](https://mp.weixin.qq.com/s/MeexLX_aOyUKHtaiyuwMTA)
  - 微信公众号「脚本之家」
    - [2023-03-23，GPT-4 Copilot X震撼来袭！AI写代码效率10倍提升，码农遭降维打击](https://mp.weixin.qq.com/s/XCBPSCLSDUSiu3CP54PfWg)
  - 微信公众号「FightingCV」
    - [2023-03-23，OpenAI重磅研究：ChatGPT可能影响80%工作岗位，收入越高影响越大](https://mp.weixin.qq.com/s/DUiEqgz-Ytf6c8NU8f7O3w)
    - [2023-07-09，不作诗，只做事：华为盘古3.0，给大模型落地定了个调](https://mp.weixin.qq.com/s/Qwvu6EA1PJx1v5sP0ouN5A)
    - [2023-07-09，VisCPM：迈向多语言多模态大模型时代](https://mp.weixin.qq.com/s/4Dv7o1LHY_K3gbzvVQi9pQ)
  - 微信公众号「科金中心」
    - [2023-03-22，今日关注 | 比尔盖茨：超级人工智能还没来 GPT模型是40余年来最革命性技术进步](https://mp.weixin.qq.com/s/vBkbE04Oz0ssYqjsvIacPg)
  - 微信公众号「findyi」
    - [2023-04-06，ChatGPT！王炸级更新！！！](https://mp.weixin.qq.com/s/F3gSN_GWvvCOR2zGva4Oew)
  - 微信公众号「AI能力站」
    - [2023-04-01，AIGC、ChatGPT和LLM三者之间的联系](https://mp.weixin.qq.com/s/O-A3uU1g8_LkOO1VhxYX4Q)
  - 微信公众号「孙立平社会观察」
    - [2023-04-07，霍金：失控的人工智能很难被阻止住](https://mp.weixin.qq.com/s/Zd4o3p4ysTJ7_kNzGivKPA)
  - 微信公众号「世界经济论坛」
    - [2023-04-01，比尔·盖茨：人工智能变革前夜的展望](https://mp.weixin.qq.com/s/O-AUjuVgfcDk2OrxBOcL_g)
  - 微信公众号「新华数字」
    - [2022-12-06，AIGC：ChatGPT的未来展望](https://mp.weixin.qq.com/s/sZUwvE6kehkTuZ1wuXzn2g)
  - 微信公众号「猫说AI」
    - [2023-04-04，ChatGPT开源平替--ChatGLM](https://mp.weixin.qq.com/s/sCTuMgbGK6N_bThOhJJ9-w)
  - 微信公众号「资本实验室」
    - [2023-02-13，ChatGPT爆火之下，生成式人工智能的「远忧近虑」| 海外周选](https://mp.weixin.qq.com/s/hrIwPA_eBu2sUmfW7mYlsw)
    - [2023-02-15，ChatGPT爆火之际，一文看清全球各方力量的应对与跟进行动](https://mp.weixin.qq.com/s/q-xuf3DUtsqW9U4SL5p18A)
  - 微信公众号「空中机器人前沿」
    - [2023-03-22，在「机器人领域」使用ChatGPT提高生产力](https://mp.weixin.qq.com/s/MB9pcqzLHb_oNNdDYa2oSA)
  - 微信公众号「CVHub」
    - [2023-04-06，《万字长文带你解读AIGC》系列之技术篇](https://mp.weixin.qq.com/s/6jMCd9yn_vBLiLJGBpSB2g)
    - [2023-04-29，哈工大团队开源医学智能问诊大模型 | 华佗: 基于中文医学知识的LLaMa指令微调模型](https://mp.weixin.qq.com/s/YKR3Bt-Ii4M0MLJApWwyDQ)
    - [2023-06-05，X-AnyLabeling: 一款多SOTA模型集成的高精度自动标注工具！](https://mp.weixin.qq.com/s/Fi7i4kw0n_QsA7AgmtP-JQ)
    - [2023-06-07，三万字长文带你全面解读生成式AI](https://mp.weixin.qq.com/s/BDYHCnkihSChKBJHVxqywA)
    - [2023-06-08，微软发布医学多模态大模型LLaVA-Med | 基于LLaVA的医学指令微调](https://mp.weixin.qq.com/s/gzyVtbMArWDnfSzfCkxl9w)
    - [2023-06-13，VisorGPT: 如何基于 GPT 和 AIGC 模型定制一个可控的生成模型](https://mp.weixin.qq.com/s/0XHjkGz7XN5jZZi2mvEKxA)
    - [2023-07-30，大连理工联合阿里达摩院发布HQTrack | 高精度视频多目标跟踪大模型](https://mp.weixin.qq.com/s/Jl2mr7tszulZX19Fx4ZNgw)
    - [2023-08-07，万字长文带你全面解读视觉大模型](https://mp.weixin.qq.com/s/aA_f4ZPWquoYbbPRqiv60g)
    - [2024-04-04，具身智能论文巡礼 - 开篇](https://mp.weixin.qq.com/s/T3oKepEReqSlntYiyeHGBw)
  - 微信公众号「芯榜」
    - [2023-04-16，思特威：人工智能浪潮，将机器视觉冲向新蓝海](https://mp.weixin.qq.com/s/jtJvltmjSeCi47XiVOzzdw)
  - 微信公众号「数智前线」
    - [2023-04-12，阿里通义千问，通向企业](https://mp.weixin.qq.com/s/L3FCVJVbMdKdeP6m8B9Lmg)
    - [2023-04-18，解码商汤大模型体系](https://mp.weixin.qq.com/s/3mkYe-UAy3dJFMBbPvgbrA)
  - 微信公众号「智能进化论」
    - [2023-04-18，AI大模型内卷加剧，商汤凭什么卷进来](https://mp.weixin.qq.com/s/-az_NylC3EyqN4iYx8Sbrw)
  - 微信公众号「深蓝AI」
    - [2023-04-23，最新综述！AIGC到底是什么？都有哪些应用？一文尽览！](https://mp.weixin.qq.com/s/rp9XVUBrh17Wr57SPFgTvg)
  - 微信公众号「人工智能前沿讲习」
    - [2023-04-23，【综述专栏】“ChatGPT的问题、风险与机遇”会议综述](https://mp.weixin.qq.com/s/-Gi4xMUXYiI13DaTVgwUdQ)
    - [2023-08-15，【综述专栏】伦敦大学、MetaAI、StabilityAI联合发布70页综述，盘点大模型的16大挑战](https://mp.weixin.qq.com/s/Q9PGJK4Z7vyuYzjXVK9yCw)
    - [2023-08-18，【【综述专栏】可信赖的大型语言模型](https://mp.weixin.qq.com/s/K3wWV6l7q_acKp2cEezakw)
  - 微信公众号「澎湃新闻」
    - [2023-05-17，莫言给余华写颁奖词，找ChatGPT帮忙](https://mp.weixin.qq.com/s/ym0w_1ftIw5BpPnGSDLsYg)
  - 微信公众号「宅码」
    - [2023-04-18，【知出乎争】GPT的变现和技术介绍](https://mp.weixin.qq.com/s/yWTriSW7CGndHraJXAi3FQ)
  - 微信公众号「Web3天空之城」
    - [2023-05-07，AI教父最新MIT万字访谈: 人类可能只是AI演化过程中的一个过渡阶段](https://mp.weixin.qq.com/s/VxlyLOUP_CIyMvGCBGimCQ)
    - [2023-05-17，Sam Altman 国会质询2.5万字全文：如果这项技术出错，它会出错得很严重](https://mp.weixin.qq.com/s/DqPTN8pADPWGjMSiO3__2w)
  - 微信公众号「AI前线」
    - [2023-05-03，7天花5万美元，我们成功复制了 Stable Diffusion，成本大降88%！训练代码已开源](https://mp.weixin.qq.com/s/KYhjUOhi3dBvGptBiBlW8A)
    - [2023-06-21，微软也搞起了开源小模型！利用OpenAI的ChatGPT和GPT-4 训练，实力碾压当前最强开源模型](https://mp.weixin.qq.com/s/RRdrSeI2ux5QE6MqJ8opSg)
    - [2023-08-11，Python 失宠！Hugging Face 用 Rust 新写了一个 ML框架，现已低调开源](https://mp.weixin.qq.com/s/YMmYnODJObYplDolnhtJZw)
    - [2023-08-21，开源打败闭源？Meta即将推出开源代码生成平台Code Llama，剑指OpenAI Codex](https://mp.weixin.qq.com/s/jKjgvMNy-UYOVMYE0dbo2w)
  - 微信公众号「AI工程化」
    - [2023-08-11，Hugging Face偷偷放大招了，Rust版本的ML框架Candle曝光](https://mp.weixin.qq.com/s/iwrV35oq_j8-SqUIMk-m0A)
  - 微信公众号「CVer」
    - [2023-05-03，代季峰教授：超大规模视觉通用模型最新研究成果分享](https://mp.weixin.qq.com/s/RYCHY0CrFbnM88ORegED1A)
    - [2023-05-20，华人一作DragGAN爆火！拖动你的GAN：交互式图像编辑新高度](https://mp.weixin.qq.com/s/QGyuCPFzg2W2QUyMu4HD2g)
  - 微信公众号「Jack Cui」
    - [2023-05-04，新项目又火了，已开源！gpt4免费了...](https://mp.weixin.qq.com/s/f6Sxc1ZYWguYkiFV3atI3g)
    - [2023-05-16，一个厉害的中医GPT，AI老中医开源了！](https://mp.weixin.qq.com/s/9O1pr7UZVRz9G9D8kMvwRw)
    - [2023-05-19，狂飙，ChatGPT 官方 iOS 应用上线了！](https://mp.weixin.qq.com/s/dt3Rf7j7ALt-GxnAXxnOgQ)
  - 微信公众号「AI数据派」
    - [2023-05-05，UC伯克利发布大语言模型排行榜！Vicuna夺冠，清华ChatGLM进前5](https://mp.weixin.qq.com/s/JS2ISYUOiSQKECYuXB8h5A)
  - 微信公众号「我爱计算机视觉」
    - [2023-05-05，图文理解能力强大！多模态对话生成模型：mPLUG-Owl，已开源！](https://mp.weixin.qq.com/s/tQYV54g6aMJxogmI3MzmiA)
    - [2023-06-13，YouKu-mPLUG 最大中文视频语言数据集，助力增强多模态大型模型性能](https://mp.weixin.qq.com/s/iJoaKCykO09R3jTCylRTVA)
    - [2023-06-28，中科大腾讯发布首篇《多模态大语言模型综述》](https://mp.weixin.qq.com/s/IiPZWEVdAJ4xrlgyWtDwng)
    - [2024-04-10，8.3K Stars!《多模态大语言模型综述》重大升级](https://mp.weixin.qq.com/s/QrP3BSW16maQQmXwt7f7uQ)
  - 微信公众号「计算机视觉联盟」
    - [2023-05-10，北大、西湖大学等开源PandaLM](https://mp.weixin.qq.com/s/mKq56QrTWTd7IiXcmYqSFA)
    - [2023-08-05，综述！LLM的当前挑战和应用](https://mp.weixin.qq.com/s/LhykEJ2SXxMZlRQm2g91JQ)
  - 微信公众号「机器学习与AI生成创作」
    - [2023-05-09，借助通用分割大模型！半自动化标注神器，Label-Studio X SAM（附源码）](https://mp.weixin.qq.com/s/2qPiEkuruIVZk1HcTqHYjg)
  - 微信公众号「差评」
    - [2023-04-17，我有个周入百万的项目：教人用ChatGPT。](https://mp.weixin.qq.com/s/awfe5Hb2_g-EZ-rHJY-SBw)
  - 微信公众号「程序员的那些事」
    - [2023-05-16，Midjourney 5.1 震撼更新！逼真到给跪，中国情侣细节惊艳，3D视频大片马上来](https://mp.weixin.qq.com/s/IViZPmfKlzgc83ozuj-zcg)
    - [2023-08-08，GitHub 1.1 万星，模拟软件开发流程，开源框架 MetaGPT 爆火](https://mp.weixin.qq.com/s/hXY4maq_-4Xlhfj9wCkEQQ)
  - 微信公众号「51CTO技术栈」
    - [2023-05-19，Stability AI开源一系列人工智能应用](https://mp.weixin.qq.com/s/QOT7ycS5MuobPW2XeYWLWw)
    - [2023-05-16，入驻QQ一天就爆满！Midjourney中文版来了！](https://mp.weixin.qq.com/s/2eLc_vIUIdR9wKIUzOxZ0A)
  - 微信公众号「GitHubDaily」
    - [2023-05-18，人手一个 Midjourney，StableStudio 重磅开源！](https://mp.weixin.qq.com/s/SbW3drfTmXyoeuwpDg5o2w)
    - [2023-09-04，开箱即用，完整版 LLaMA2 大模型全流程方案，开源了！](https://mp.weixin.qq.com/s/adoVaa6FTAtSgD1lgpJZTQ)
  - 微信公众号「CreateAMind」
    - [2023-05-20，改进GPT的底层技术](https://mp.weixin.qq.com/s/5zZrol7CLHD-kEMejwHimw)
  - 微信公众号「深度学习与NLP」
    - [2023-05-21，邱锡鹏团队提出具有跨模态能力SpeechGPT，为多模态LLM指明方向](https://mp.weixin.qq.com/s/fEBWELAiEJikC91pwk9l-Q)
  - 微信公众号「APPSO」
    - [2023-06-01，ChatGPT路线图曝光：没有GPT-5、识图功能要等到明年、GPT-3或将开源](https://mp.weixin.qq.com/s/yKst4w3x0II3kGy5VqY2gA)
  - 微信公众号「佐思汽车研究」
    - [2023-05-26，大模型上不了车](https://mp.weixin.qq.com/s/guxGFY5Jg_YdWDxnIyTZsA)
  - 微信公众号「芯东西」
    - [2023-06-14，1530亿颗晶体管！AMD甩出最强AI芯片，单个GPU跑大模型](https://mp.weixin.qq.com/s/b47zVOa_KGEN47_d3Dlibw)
  - 微信公众号「开源技术服务中心」
    - [2023-05-31，河套IT WALK(总第64期)：AI与自动驾驶科技：打造未来生活方式](https://mp.weixin.qq.com/s/wGupibJ9cKrjdSbUv9cQgQ)
  - 微信公众号「OneFlow」
    - [2023-06-09，GPT总设计师：大型语言模型的未来](https://mp.weixin.qq.com/s/DAV4ZQ5HVKw3z-mQnM7cWA)
  - 微信公众号「AINLP」
    - [2023-08-06，Llama深入浅出](https://mp.weixin.qq.com/s/grayNg0IvAmILTF1dCEWTA)
    - [2023-08-06，哈工大开源“活字”对话大模型](https://mp.weixin.qq.com/s/gmKjMjr7VVESPEAWIQW3wQ)
  - 微信公众号「AINLPer」
    - [2023-06-05，近乎完美！最强算术语言模型: Goar-7B，干翻GPT-4，怒越PaLM-540B！24G可训练](https://mp.weixin.qq.com/s/_haINkHNV4bMszm9F41yXA)
    - [2023-06-06，Amazon | 深入研究LLMs与AutoGPT的结合：揭示出GPT-4惊人的人类决策能力！](https://mp.weixin.qq.com/s/Gbz7ZVVdeTq64mj1-__aQA)
    - [2023-06-16，FinGPT：一个「专用于金融领域」的开源大语言模型（LLM）框架，源码公开！](https://mp.weixin.qq.com/s/A9euFin675nxGGciiX6rJQ)
    - [2023-06-26，ChatGLM2-6B 发布：性能大幅提升，8-32k上下文，推理提速42%](https://mp.weixin.qq.com/s/zDf9YbOEc681Otcjh0FJxw)
  - 微信公众号「ArronAI」
    - [2023-06-13，高性能支持LLM的机器学习Tensor库](https://mp.weixin.qq.com/s/hdwWP39BHb68VHtCcUcM7Q)
    - [2023-07-19，Meta发布升级大模型LLaMA 2：开源可商用](https://mp.weixin.qq.com/s/cahpaMKbdKNMJCp1Rot5KA)
    - [2023-07-30，大模型部署框架 FastLLM 实现细节解析](https://mp.weixin.qq.com/s/AFUZC9RAgA7_Mj6KsgYqSw)
    - [2023-07-31，ChatGLM-6B VS 昆仑万维天工对比](https://mp.weixin.qq.com/s/I4RdHFzOhyxzOYkVGMH-og)
  - 微信公众号「DataLearner」
    - [2023-05-19，ChatGLM-6B重磅升级！清华大学开源VisualGLM-6B技术解析：一个可以在本地运行的读懂图片的语言模型！](https://mp.weixin.qq.com/s/nZwiNk_80uTPcS2QrofnrQ)
    - [2023-05-27，Falcon-40B：截止目前最强大的开源大语言模型，超越MetaAI的LLaMA-65B的开源大语言模型](https://mp.weixin.qq.com/s/Vy_xWBuZU0AaaPMCIhKIyw)
    - [2023-06-13，国产开源大模型再添重要玩家：BAAI发布开源可商用大模型Aquila](https://mp.weixin.qq.com/s/n8GwkDt9wXI9nNfFTIRcBQ)
    - [2023-06-25，重磅！第二代ChatGLM-6B发布！清华大学THUDM发布ChatGLM2-6B：更快更准，更低资源更长输入！](https://mp.weixin.qq.com/s/7Y6_jqj0RBq82hEggFHTgg)
    - [2023-07-09，使用LangChain做大模型开发的一些问题：来自Hacker News的激烈讨论~ ](https://mp.weixin.qq.com/s/GKF28C1yzWZDtCXjJQ52hg)
    - [2023-07-14，重磅！清华大学第二代大模型ChatGLM2-6B现在转为免费商用授权协议了~](https://mp.weixin.qq.com/s/FpRAA2b3o6pj8gNpeSWb4g)
    - [2023-07-15，GPT4All发布可以在CPU上生成embeddings向量的模型：低成本、高质量、易上手的embedding模型新选择](https://mp.weixin.qq.com/s/hPQlthpVVlxjHhkSKLU0GA)
    - [2023-07-18，如何让开源大模型支持Code Interpreter：基于LangChain的开源项目Code Interpreter API](https://mp.weixin.qq.com/s/q5D4k4ZFxjRKX7LrKk3SEA)
    - [2023-07-19，重磅！Meta发布LLaMA2，最高700亿参数，在2万亿tokens上训练，各项得分远超第一代LLaMA~完全免费可商用！](https://mp.weixin.qq.com/s/I-zU5n_dXKKMa2x9wyxYgw)
    - [2023-07-22，关于大语言模型的11个应用方向和16个挑战总结：来自来自伦敦大学、MetaAI等机构合作的688篇参考文献与业界实践](https://mp.weixin.qq.com/s/fnyTrTAqFonrt1IxZnHRVw)
    - [2023-07-23，一文总结13个国内外ChatGPT平替产品：是时候可以不那么依赖ChatGPT了~](https://mp.weixin.qq.com/s/QvVkTYDT6k2eado1HEWLbg)
    - [2023-07-27，如何基于Gradio构建生成式AI的应用：吴恩达联合HuggingFace推出最新1小时短课](https://mp.weixin.qq.com/s/N0R2yC_zcmbWlbZZmXKwBQ)
    - [2023-07-29，Open ChatGPT：一个整合了GPT-4和多模态能力的ChatGTP服务商](https://mp.weixin.qq.com/s/23_3sFZhIxP6FDiFsNwr4w)
    - [2023-08-02，Megatron-LLM：支持大规模分布式语言模型(LLM)预训练和微调的库](https://mp.weixin.qq.com/s/WsK1MgMxIRf6RNWKzOUkOA)
    - [2023-08-03，生成式AI领域拓展！MetaAI开源AudioCraft：一个支持AudioGen、MusicGen等模型的音频生成开发框架](https://mp.weixin.qq.com/s/OLLCiMqKHQJxGGR1sPA3qw)
    - [2023-08-07，MetaGPT技术全解析：另一个AutoGPT，一个可以替代小型软件开发团队的LLM框架，产品经理、系统设计、代码实现一条龙](https://mp.weixin.qq.com/s/OteOLYsO6WoAjA1j3HMrbg)
    - [2023-08-09，ChatGLM团队发布AI Agent能力评测工具AgentBench：GPT-4一骑绝尘，开源模型表现非常糟糕！](https://mp.weixin.qq.com/s/wUuAHsiZJmpCPn_3uvT4Aw)
    - [2023-08-10，《流浪地球2》的数字生命计划可能快实现了！HeyGen即将发布下一代AI真人视频生成技术，效果逼真到无法几乎分辨！](https://mp.weixin.qq.com/s/70Fj9HCe3ruiI43WmMZLjQ)
    - [2023-08-16，国产大模型与全球最强大模型大比拼：语义理解、数学推理同台竞技，究竟谁更厉害~](https://mp.weixin.qq.com/s/lVQorSHWUmYjDK2MgVm9bg)
    - [2023-08-20，需要多少GPU显存才能运行预训练大语言模型？大语言模型参数规模与显存大小的关系估算方法~](https://mp.weixin.qq.com/s/-f9AY-nYRKaWKjDKhSW2iw)
    - [2023-08-24，大规模中文开源数据集发布！2TB、几十亿条可商用的中文数据集书生·万卷 1.0开源~中文大模型能力可能要更上一层楼了！](https://mp.weixin.qq.com/s/ImCt2OgIt8W7-off8W7hxQ)
    - [2024-04-06，高产的阿里！Qwen1.5系列再次更新：阿里开源320亿参数Qwen1.5-32B，评测超Mixtral MoE，性价比更高！](https://mp.weixin.qq.com/s/e_djuVBXtfttGmgCpw6UOw)
    - [2024-04-10，重磅！Google开源CodeGemma编程大模型和基于RNN架构的新型大模型RecurrentGemma，同等参数规模表现优秀](https://mp.weixin.qq.com/s/58y65bUKFGYLo42nOXaGWQ)
    - [2024-04-19，开源王者！全球最强的开源大模型Llama3发布！15万亿数据集训练，最高4000亿参数，数学评测超过GPT-4，全球第二！](https://mp.weixin.qq.com/s/m3rEZY-BFumitxBqg17Epw)
  - 微信公众号「算法美食屋」
    - [2023-07-03，60分钟吃掉ChatGLM2-6b微调范例~](https://mp.weixin.qq.com/s/Lf70i8M0KNDs9ZB8H32h4w)
    - [2023-07-08，单样本微调给ChatGLM2注入知识~](https://mp.weixin.qq.com/s/hANR9OVDVEZMMvK8uxtChA)
    - [2023-07-16，用Kaggle免费GPU微调ChatGLM2](https://mp.weixin.qq.com/s/PSWSN5OJfaSU8tLqOaZE3A)
    - [2023-07-23，微调BaiChuan13B来做命名实体识别](https://mp.weixin.qq.com/s/ElEkYqRiEI8gKtO-cgnaXw)
    - [2023-08-21，BaiChuan13B多轮对话微调范例](https://mp.weixin.qq.com/s/4RUP7VaHwn11UCogyjlb7g)
    - [2023-09-03，9个范例带你入门LangChain](https://mp.weixin.qq.com/s/qHUxO6Ml-O1PCK1bc9uD7g)
  - 微信公众号「KBQA沉思录」
    - [2023-06-14，【中文医疗大模型】训练全流程源码剖析](https://mp.weixin.qq.com/s/DTHIxyDb9vG793hAKGLt2g)
  - 微信公众号「技术狂潮AI」
    - [2023-05-31，基于ChatGLM-6B构建本地私有化离线知识库](https://mp.weixin.qq.com/s/2TVP0WcLfLdnDQw88eGIGg)
    - [2023-06-23，ChromaDB：开源向量嵌入数据库，让你的AI应用程序拥有记忆力](https://mp.weixin.qq.com/s/kqd41FeuQcy8ag8jQwEQNg)
    - [2023-08-21，GPT-LLM-Trainer：如何使用自己的数据轻松快速地微调和训练LLM](https://mp.weixin.qq.com/s/9asqLJtvPins9NlZvaFziA)
    - [2023-08-27，LangChain-Chatchat：基于LangChain和ChatGLM2-6B构建本地离线私有化知识库](https://mp.weixin.qq.com/s/dfJ2qajJrmu1kaAqyijLaw)
  - 微信公众号「NLP日志录」
    - [2023-06-16，WorkGPT：一个智能体框架，类似于AutoGPT或LangChain](https://mp.weixin.qq.com/s/OdRrAQcEMfuuT8xLFPijZQ)
    - [2023-06-19，Awesome-Chinese-LLM：整理开源的中文大语言模型](https://mp.weixin.qq.com/s/bn97j_OKWPakwMDYQYEgyw)
    - [2023-06-25，LLaMA Server：将LLaMA C++和Chatbot UI结合的LLaMA服务](https://mp.weixin.qq.com/s/-kNS6WX4OVCWS_mEHBL_rQ)
    - [2023-06-26，什么是HuggingFace](https://mp.weixin.qq.com/s/EscXWBLM09bgfgfUT66C9Q)
    - [2023-07-05，ChatGenTitle：使用百万arXiv论文信息在LLaMA模型上进行微调的论文题目生成模型](https://mp.weixin.qq.com/s/p3nxReh3-syDPSu6tK4PbA)
    - [2023-07-14，eigenGPT：GPT2的最小化C++实现](https://mp.weixin.qq.com/s/ivVQxXUI-RP0rsYkSKg3zQ)
    - [2023-07-17，开源版的OpenAI ChatGPT Code interpreter实现](https://mp.weixin.qq.com/s/7iDXnRm3j4-xkJLDxfVS_A)
    - [2023-07-28，Chidori是一个LangChain的替代品](https://mp.weixin.qq.com/s/2p00yh65pb4dcDUTfRwJjQ)
    - [2023-08-12，小米发布了他们的大模型MiLM-6B](https://mp.weixin.qq.com/s/kLpgRzy3j6fAqhM50cC2xg)
    - [2023-08-14，VirtualWife - 一个虚拟主播项目](https://mp.weixin.qq.com/s/QgVfKx2CkUwDUIRTqFELqA)
    - [2023-08-14，MeChat：中文心理健康支持对话大模型与数据集](https://mp.weixin.qq.com/s/yKxXi6SiIJpBhLozqe_XYQ)
    - [2023-08-16，原Langchain-ChatGLM项目正式发布v0.2.0版本](https://mp.weixin.qq.com/s/fBPEE34_EBf_2-RM4ZqAzg)
    - [2023-08-16，Llama2模型的优化版本：Llama-2-Onnx](https://mp.weixin.qq.com/s/Z2nBkaIgtLIa8OEeFJP4jg)
    - [2023-08-16，妙鸭相机开源版工具FaceChain](https://mp.weixin.qq.com/s/qF7WVqHpMN1zODTe_W8J7A)
    - [2023-08-18，仲景：首个实现从预训练到 RLHF 全流程训练的中文医疗大模型](https://mp.weixin.qq.com/s/Rhir7Il0NnsetzpX03Cjjw)
    - [2023-08-18，书生·万卷多模态语料库](https://mp.weixin.qq.com/s/spl-N87mySAkRpBoMIYPuA)
  - 微信公众号「NLP工程化」
    - [2023-08-22，基于MovieChat视频理解的问答，能够在24GB显卡上处理10K帧视频](https://mp.weixin.qq.com/s/gBEmygej9mauJ-DMzVefjQ)
    - [2023-08-22，llama2.c for Dummies：llama2.c手把手代码解析](https://mp.weixin.qq.com/s/AiFY_uu48KFX0hv3eDdAwQ)
    - [2024-04-16，本地 LLM 推理项目大列表](https://mp.weixin.qq.com/s/3O6nAO8GN4eYQDefqJCfQQ)
    - [2024-04-25，llama2.cpp：C++版本的Llama 2推理库](https://mp.weixin.qq.com/s/mr0aKhxV9V-vKeaJXOMijQ)
  - 微信公众号「NewBeeNLP」
    - [2023-02-07，ChatGPT Prompt工程：设计、实践与思考](https://mp.weixin.qq.com/s/a8hjzZ_Rzl6pOU1PRAARJQ)
    - [2023-07-19，谁才是真正的 OpenAI？更大更强的Llama 2来啦，可直接商用](https://mp.weixin.qq.com/s/2kN6hI17VpKEMgvK8iEqDg)
    - [2023-02-07，ChatGPT Prompt工程：设计、实践与思考](https://mp.weixin.qq.com/s/a8hjzZ_Rzl6pOU1PRAARJQ)
    - [2023-08-07，大模型时代必看！Open AI创始人演讲《State Of GPT》](https://mp.weixin.qq.com/s/gQ4LnMebEHvtBVt52oxT-w)
    - [2023-04-11，OpenAI创始大神手搓千行C代码训练GPT，附PyTorch迁移教程](https://mp.weixin.qq.com/s/OBNqoZ6Iq9BVUWVrobYe7A)
    - [2024-04-13，中山大学：“梗王”大模型，靠讲笑话登上CVPR](https://mp.weixin.qq.com/s/AeWCbKByO-fYFThSxOb43A)
  - 微信公众号「AI寒武纪」
    - [2023-06-19，重磅：未来10年生成式人工智能将这样影响所有人](https://mp.weixin.qq.com/s/qsLOke8-jckhF1XYxswFtQ)
    - [2023-08-31，国内首批8个大模型正式获批上线](https://mp.weixin.qq.com/s/ElUjTKpDFG4vYmOjSZfM3g)
    - [2024-04-10，【太疯狂了】用 1000 行纯 C 代码实现 GPT-2 训练：Andrej Karpathy重塑LLM训练格局](https://mp.weixin.qq.com/s/hNKWVqepbega6YPf48b8ag)
    - [2024-04-12，【重磅】谷歌重塑Transformer：无限记忆力，无限长输入，LLM基础研究重大突破](https://mp.weixin.qq.com/s/bV2b9uJ4GFQPhhggHT3VIA)
    - [2024-04-14，【全球黑客加持】Karpathy 1000行纯C训练大模型速度已追平PyTorch](https://mp.weixin.qq.com/s/VvwDhMmq80yN-Wcb8s3aiQ)
  - 微信公众号「毫末智行」
    - [2023-06-13，自动驾驶大模型亮相2023北京智源大会！顾维灏：DriveGPT将重塑汽车智能化技术路线](https://mp.weixin.qq.com/s/ybtjyY7gjgywl6Jvjd5RMg)
  - 微信公众号「智源研究院」
    - [2023-06-11，悟道·天鹰 Aquila + 天秤 FlagEval，打造大模型能力与评测标准双标杆](https://mp.weixin.qq.com/s/8oP9nongpkkfHuE1RsKx8A)
    - [2023-08-15，FlagEval 8月榜单：新增通义千问、Llama2等多个模型评测，新增基座模型代码生成能力评测](https://mp.weixin.qq.com/s/RYccZXQNs9hHHNRJI9tLgg)
  - 微信公众号「CLUE中文语言理解测评基准」
    - [2023-06-19，最新大模型排名！中文大模型评测基准SuperCLUE发布6月榜单](https://mp.weixin.qq.com/s/lTqAOO8iqKUW3B_4VMswtw)
    - [2023-07-20，Meta开源免费商用大模型Llama2-13B测评揭晓 | SuperCLUE](https://mp.weixin.qq.com/s/ZowePHkDouP8AiZshR-MXw)
  - 微信公众号「AI范儿」
    - [2023-06-09，Midjourney指令的终极列表：完整指南](https://mp.weixin.qq.com/s/wyAe6hDDusbSC6M2naAHVA)
    - [2023-07-19，细观察 - Llama-2开源新闻刷屏背后...... 商用？没戏，“中文”被排除在外！](https://mp.weixin.qq.com/s/imVXxEJ4TJL3kRP2Aze2nA)
  - 微信公众号「机器学习实验室」
    - [2023-06-26，Midjourney 5.2震撼发布！](https://mp.weixin.qq.com/s/l8a6T2ha4q13go3dRbt8pA)
    - [2023-07-06，「分割一切」视频版SAM来了！](https://mp.weixin.qq.com/s/FdbOe_kvFwDJxF2KMzUO5g)
    - [2023-07-09，ChatGPT神器Code Interpreter来了！奉上一份保姆级教程](https://mp.weixin.qq.com/s/-PhTEwe8xZ3pXRck7imYsA)
    - [2023-07-20，Meta 开源 Llama 2！大模型竞争格局变了](https://mp.weixin.qq.com/s/EesOpLmGDyvKSkiu2OlcgQ)
  - 微信公众号「无数据不智能」
    - [2023-05-31，WebGLM：10B 堪比 webGPT 175B](https://mp.weixin.qq.com/s/3bXpWUq6twqBmumU1xH0yg)
    - [2023-06-14，一份大模型应用到各领域的综述，包括法律、金融、教育、软件工程、生物等等](https://mp.weixin.qq.com/s/dui1xcCIIVyBv-sLslHeTg)
    - [2023-06-16，H2OGPT：开源代码仓库套件,开源GPT替代品,包括可商用的代码、数据、模型、微调工具](https://mp.weixin.qq.com/s/QIPMIqG8C8rNJqSKTjFWxg)
    - [2023-06-17，macaw-llm：开源图像、音频、视频和文本的多模态语言建模模型](https://mp.weixin.qq.com/s/O3ryffaCghfU3_tUUu2TIA)
    - [2023-07-05，GPT-Migrate：让你的项目轻松更换语言或框架](https://mp.weixin.qq.com/s/Cl5jvzoKe6kU7zeTi4plqA)
    - [2023-07-09，让每个人都可以轻松、快速、廉价地使用vLLM进行服务](https://mp.weixin.qq.com/s/N1ursW7evovFsYKEc_x6NA)
    - [2023-07-09，InternLM：强大的开源模型和弹性工作流程建设工具](https://mp.weixin.qq.com/s/OQLy7ZM81Cde0-Qba4sHMg)
    - [2023-07-19，deepspeed发布0.10.0，加入ZeRO++：降低4倍网络通信，显著提高大模型及类ChatGPT模型训练效率](https://mp.weixin.qq.com/s/GWauayszfYWDV2pZr9Wf5g)
    - [2023-08-17，memochat: 将llms优化为使用备忘录以实现一致的长程对话](https://mp.weixin.qq.com/s/dkaXAxHTNLIAoFEwwL_ifg)
    - [2023-08-17，diaggpt: 基于大模型的多轮对话话题管理](https://mp.weixin.qq.com/s/cMYEp8J4SzU7yjGTF2TG9Q)
  - 微信公众号「AI浪潮时代」
    - [2023-06-18，150个ChatGPT角色扮演指令，全网的角色扮演指令都在这里！让你的ChatGPT成为任何领域的专家（1/15）](https://mp.weixin.qq.com/s/T8A_FpFwOHHwsyvNggf7yA)
    - [2023-06-20，150个ChatGPT角色扮演指令，全网的角色扮演指令都在这里！让你的ChatGPT成为任何领域的专家（2/15）](https://mp.weixin.qq.com/s/IaolSkSOFakF6eBJVEsFyA)
    - [2023-06-21，150个ChatGPT角色扮演指令，全网的角色扮演指令都在这里！让你的ChatGPT成为任何领域的专家（3/15）](https://mp.weixin.qq.com/s/h45GnzshxyI0p-xAW1hdNA)
    - [2023-07-07，重大消息！GPT-4.0API，即将全面开发使用](https://mp.weixin.qq.com/s/sJT8Kj5GPxfLoaB4hCsueg)
  - 微信公众号「深度学习自然语言处理」
    - [2023-06-26，ChatGLM2-6B：性能大幅提升，8-32k上下文，推理提速42%，在中文榜单位列榜首](https://mp.weixin.qq.com/s/7Dn_R-9q_uGZBEEQcIZJGg)
    - [2023-07-21，iPhone、Mac上都能跑，刷屏的Llama 2究竟性能如何？](https://mp.weixin.qq.com/s/B8LnEVjRt6dwaECRQIlHfw)
    - [2023-08-15，字节 | 大模型BuboGPT：引入视觉定位，实现细粒度多模态，已开源](https://mp.weixin.qq.com/s/1yM83EO9qh_iM_9CkbjuCw)
  - 微信公众号「集智书童」
    - [2023-06-28，MobileSAM来啦 | 比SAM小60倍，比FastSAM快4倍，速度和效果双赢](https://mp.weixin.qq.com/s/gTsdqVNgKpfnU-4S7DJhnA)
    - [2023-07-03，医疗SAM也来啦 | AutoSAM告诉你如何在医疗领域更快更好开发大模型](https://mp.weixin.qq.com/s/vd7bxoxB_BiffcSu-oHPbg)
    - [2023-07-04，聊聊大火的AIGC和扩散模型](https://mp.weixin.qq.com/s/y2rakG6A-vWRp3i0ka9DPA)
    - [2023-07-04，中科院版「分割一切」模型来了，比Meta原版提速50倍 | GitHub 4.2K+星](https://mp.weixin.qq.com/s/u_IcsEldPR2TCtjJVIvZ6g)
    - [2023-07-10，SAM增强技术 | SAMAug提出Point Prompt增强，让SAM模型天天向上](https://mp.weixin.qq.com/s/KPP07jWt8DYUslkRCMGuKw)
  - 微信公众号「分布式实验室」
    - [2023-07-11，万字长文详解GPT](https://mp.weixin.qq.com/s/sBKaW5W_uyXxzUVx3nMYsg)
    - [2023-07-12，王小川的百川智能发布Baichuan-13B AI大模型](https://mp.weixin.qq.com/s/tudo6INXBGfUcDaGwtpctQ)
    - [2023-07-19，Meta开源LLama 2，可商用的大语言模型](https://mp.weixin.qq.com/s/3Rmx05-X5EeFi0O6Q2_ccw)
    - [2023-07-20，LangChain初学者入门指南](https://mp.weixin.qq.com/s/F4QokLPrimFS1LRjXDbwQQ)
  - 微信公众号「浩瀚的苍穹」
    - [2023-06-26，利用 GPT-4 & LangChain 本地部署企业知识库(技术篇)](https://mp.weixin.qq.com/s/-UNRLV9ttgI79A5iFmO7zQ)
  - 微信公众号「AI育未来」
    - [2023-07-13，解读8月15日实施的《生成式人工智能服务管理暂行办法》，AI的春天来了](https://mp.weixin.qq.com/s/mScsxyYH56oFEoMC0XWopw)
  - 微信公众号「SolidUI」
    - [2023-07-06，SolidUI AI生成可视化，开创性开源项目，版本0.1.0 功能讲解](https://mp.weixin.qq.com/s/X0wxx9ZN982iOY6JzFBmAA)
  - 微信公众号「RUC AI Box」
    - [2023-07-05，大模型综述升级啦](https://mp.weixin.qq.com/s/9YMUSSrGLSBKMFY3JYlaoQ)
    - [2023-08-07，YuLan-Chat-2：基于LLaMA-2的全新中英文对话大模型](https://mp.weixin.qq.com/s/dKiclXeYRI83p4uy3ruSSQ)
  - 微信公众号「电子发烧友网」
    - [2023-07-08，探索大模型落地应用成为当前主旋律！众多垂直领域大模型陆续发布！](https://mp.weixin.qq.com/s/QvRt6Sm9Qti4GPE4aucpYg)
  - 微信公众号「CSDN程序人生」
    - [2023-07-11，华为盘古大模型3.0发布！](https://mp.weixin.qq.com/s/G9OEi27CeZJq7KVNF1U2sA)
  - 微信公众号「GitHubStore」
    - [2023-06-29, ChatGLM.cpp：ChatGLM-6B的C++实现版，可在macBook上运行 ，ChatGLM.cpp：ChatGLM-6B的C++实现版，可在macBook上运行](https://mp.weixin.qq.com/s/QuaK09Z5Na04SH-fncfbiA)
    - [2023-07-11，LiteChain：构建LLMs应用的轻量级LangChain](https://mp.weixin.qq.com/s/kp7oBS8kwIHB3HJo4vWtdQ)
    - [2023-07-12，gpt4free：提供免费的gpt API](https://mp.weixin.qq.com/s/d8mWZFa2QANlcuFQHBaLpg)
    - [2023-07-17，RealChar：实时AI数字人](https://mp.weixin.qq.com/s/v1UcB5Y77JWz_KGwZt8rJw)
    - [2023-07-20，开源多模态模型LLaVA重大更新，支持LLaMA2!](https://mp.weixin.qq.com/s/8u9GPluromcbqalKaYWQKw)
    - [2023-07-24，MLC LLM：让每个人都能在每个人的设备上开发、优化和部署人工智能模型](https://mp.weixin.qq.com/s/DNn89Gmqt7EvrYAVW39A3Q)
    - [2023-07-28，AutoChain : LangChain 的替代品](https://mp.weixin.qq.com/s/v4c4JzXiVEJfwi9CQbJ2Tg)
    - [2023-07-29，Xorbits Inference：大模型推理， 轻而易举](https://mp.weixin.qq.com/s/dDmUwoQAknvq27rCJePtxQ)
    - [2023-07-29，Chidori: LangChain的替代品](https://mp.weixin.qq.com/s/graiS0SluRWrAQb6N7bkGQ)
    - [2023-07-30，magentic：将LLM无缝集成到Python函数](https://mp.weixin.qq.com/s/-5ZQvix-gfPgwkC3Qn8YFw)
    - [2023-07-30，llama2-webui：在本地使用Gradio用户界面在GPU或CPU上运行Llama 2](https://mp.weixin.qq.com/s/e8PupfNNHyNm9pEOFEoV5w)
    - [2023-08-04，重磅！Facebook 开源 AudioCraft！](https://mp.weixin.qq.com/s/gEwfu7JbHqjmsXIwumnVSQ)
    - [2023-08-05，哈工大科大讯飞联合推出中文LLaMA-2 & Alpaca-2大语言模型](https://mp.weixin.qq.com/s/sJ_imBdHCD4NibVy58EO2w)
    - [2023-08-06，ToolLLM: 利用大型语言模型掌握 16000 多个真实世界的 API](https://mp.weixin.qq.com/s/dQc58kMqtiiYM2JfpS5jRg)
    - [2023-08-09，Whisper Burn: Rust实现的OpenAI's Whisper语音转录模型](https://mp.weixin.qq.com/s/-QMaS3BmtsmSaFLW629N8w)
    - [2023-08-09，Cria - 像使用OpenAI一样使用LLAMA-2](https://mp.weixin.qq.com/s/bFzQzD_gYtIbN04Dy9foUA)
    - [2023-08-07，阿里开源通义千问模型](https://mp.weixin.qq.com/s/SHNg2ti5a8Doop6nbPuRRA)
    - [2023-08-10，能当老板的多智体框架MetaGPT](https://mp.weixin.qq.com/s/PtixAzNoxmJ_WN9WPJGuGg)
    - [2023-08-10，Chie：类似ChatGPT的跨平台桌面应用](https://mp.weixin.qq.com/s/Lh4NuKd2ENTNuseB6U8WbQ)
    - [2023-08-13，Windows桌面版Whisper客户端](https://mp.weixin.qq.com/s/U0CIIibKx5uzZXl3Waz0IA)
    - [2023-08-14，Doctor GPT：通过了美国医学执照考试的大型语言模型](https://mp.weixin.qq.com/s/zsXMg1H9T-bBi_X7Exeh0g)
    - [2023-08-15，Fooocus : 集Stable Diffusion 和 Midjourney 优点于一身的开源AI绘图软件](https://mp.weixin.qq.com/s/adyXek6xcz5aOPAGqZBrvg)
    - [2023-08-16，OpenChat 大规模更新！](https://mp.weixin.qq.com/s/Xq8PLZ8CeSMZHFzD89by8A)
    - [2023-08-16，FaceChain：三张照片打造个人数字替身！](https://mp.weixin.qq.com/s/y4FdOifwgSWjRmtRJI2mgw)
    - [2023-08-17，GPT-vup: Live2D数字人直播](https://mp.weixin.qq.com/s/A1NAsYQaxTuUUKZ_q2ahkQ)
    - [2023-08-19，FastGPT：基于 LLM 大语言模型的知识库问答系统](https://mp.weixin.qq.com/s/fRxcWN9UaKBuOzRNT8G--Q)
    - [2023-08-20，SillyTavern:可以本地部署的虚拟角色聊天软件](https://mp.weixin.qq.com/s/MyZamu0hMosnpPSFh_IpQg)
    - [2023-08-24，浙大阿里等联合研发法律大模型：智海-录问](https://mp.weixin.qq.com/s/nhr2DMJxS_O6Ull4CXtoPw)
    - [2023-08-29，Meta AI真的是清流！发布了一款专门用于编程的模型：Code Llama](https://mp.weixin.qq.com/s/9MkM3t_aI9XJw9Ziinkbgg)
    - [2024-04-11，llm.c：实现了大语言模型(LLM)训练的简单、纯 C/CUDA 版本，无需 PyTorch 或 cPython](https://mp.weixin.qq.com/s/7cHYDBHqs8ClkijI-Fya9A)
  - 微信公众号「山行AI」
    - [2023-06-17，基于LangChain的优秀项目资源库](https://mp.weixin.qq.com/s/G9aqBFzd5j8wVPTH160pZA)
    - [2023-06-19，GPT4All——可本地布署的AI助理](https://mp.weixin.qq.com/s/KJRyAbUAxmNrcPcFJ3f-cw)
    - [2023-06-20，优秀的多模态大模型(LLM)资源库](https://mp.weixin.qq.com/s/n9ICXF1d2ZO2Vw3RgF-RyQ)
    - [2023-06-22，open-llms 开源可商用的优秀大模型资源库](https://mp.weixin.qq.com/s/3W2a06OV0fLTptqjs4f-AQ)
    - [2023-06-27，LocalAI——一款可在消费级硬件上本地运行 LLMs的AI应用](https://mp.weixin.qq.com/s/J-3Apw2aJJrwrrkKKfcjuQ)
    - [2023-07-17，Chatgpt-Retrieval-Plugin—GPT AI插件 真正联网的人工智能](https://mp.weixin.qq.com/s/_U-g1dw09tWbdH5TS4LIVw)
    - [2023-07-25，LangChain +Streamlit+ Llama ：将对话式人工智能引入您的本地设备](https://mp.weixin.qq.com/s/hBQRapWbtqsUH5y7vqlggw)
  - 微信公众号「凤凰网科技」
    - [2023-06-20，AI前哨｜孙正义要对AI出手了：我天天都在和ChatGPT聊天](https://mp.weixin.qq.com/s/8BwhEKZLnphzUFlVK_Rc8A)
  - 微信公众号「证券时报」
    - [2023-06-22，软银孙正义：结束休眠，All in AI](https://mp.weixin.qq.com/s/3SrGGhwLeL-plHpKh_UCkw)
  - 微信公众号「智王AI研究院」
    - [2023-06-03，langChain杀手2：MiniChain迷你链-全球首发](https://mp.weixin.qq.com/s/kkXR2G1CipYutu8M590nTw)
    - [2023-06-27，GPT爆款：vicuna-33B](https://mp.weixin.qq.com/s/Bo06Rzmd1_NhGsPNkH9bYw)
    - [2023-07-20，全球首发：llama2架构图](https://mp.weixin.qq.com/s/gGt9rXYpqAYY1J4zAq-POA)
  - 微信公众号「关于NLP那些你不知道的事」
    - [2023-06-27，【LLMs 入门实战】 ChatGLM2-6B 模型学习与实战](https://mp.weixin.qq.com/s/11jCCeOpg1YbABIRLlnyvg)
    - [2023-07-21，重磅！Meta发布LLaMA2，最高700亿参数，在2万亿tokens上训练，各项得分远超第一代LLaMA~完全免费可商用！](https://mp.weixin.qq.com/s/IEhvq4Dw2JewF-QFzftlvA)
    - [2023-08-05，大模型思维链（Chain-of-Thought）技术原理](https://mp.weixin.qq.com/s/IlRhdwBJAtynhrnPSEdoRQ)
    - [2023-08-09，LLaMA2多GPU训练入门](https://mp.weixin.qq.com/s/At8HfnbKlZm-edojmeIRxQ)
    - [2023-08-13，LangChain+ChatGLM如何调优？](https://mp.weixin.qq.com/s/vinAWk3g8kwBYLmGDLXV6g)
    - [2024-01-26，基于TensorRT-LLM的大模型部署(速通笔记)](https://mp.weixin.qq.com/s/2d6ihFFDTDfppYbjtBPHMw)
    - [2024-04-19，Llama-3问世，开源模型弯道超车闭源模型的历史时刻就在眼前了？ ](https://mp.weixin.qq.com/s/IvubUL147CPhlsBy1KG8gQ)
  - 微信公众号「前端立志传」
    - [2023-07-02，用Midjourney+剪映,我一天量产上百个精致短视频！](https://mp.weixin.qq.com/s/LBzHC2-x_ppnkElOOWFVBw)
  - 微信公众号「AI的潜意识」
    - [2023-07-10，LLaMA Plus版来了，谷歌推出LongLLaMA，不仅让你的大模型更集中注意力，还能处理超长上线文](https://mp.weixin.qq.com/s/K8ExTUUXDruZGwr-PA4oFQ)
  - 微信公众号「HsuDan」
    - [2023-07-07，OpenChat：性能高达105.7%，第一个超越ChatGPT的开源模型？](https://mp.weixin.qq.com/s/XUZOnOck6TUDBZnMqVj1_Q)
  - 微信公众号「智能车情报」
    - [2023-07-10，最新综述一览！自动驾驶中基于Transformer的模型和硬件加速分析](https://mp.weixin.qq.com/s/CLKkPeHjCESkE5qNvn7XBg)
  - 微信公众号「智能车参考」
    - [2023-08-18，芜湖起飞！两个安徽老乡握手，1700亿参数大模型上车，“超过ChatGPT！”](https://mp.weixin.qq.com/s/J6IHMf7THKJ9QTxsjG87lg)
  - 微信公众号「InfoQ」
    - [2023-07-11，OpenAI 宣布 GPT-4 API 全面开放使用！](https://mp.weixin.qq.com/s/caRvuREB_bxPa5GU4rkVMA)
    - [2024-04-09，“真男人就应该用 C 编程”！用 1000 行 C 代码手搓了一个大模型，Mac 即可运行，特斯拉前AI总监爆火科普 LLM](https://mp.weixin.qq.com/s/qb0dhdFnXZS4LeW2mvG6fg)
  - 微信公众号「自然语言处理及深度学习」
    - [2023-05-17，ChatGLM-6B模型结构组件源码阅读](https://mp.weixin.qq.com/s/r7KEJmrpJZmY7KBP4veS6A)
  - 微信公众号「雷峰网」
    - [2023-07-28，五道口大模型简史](https://mp.weixin.qq.com/s/fm37ofUwLQyItKkkLMjG5Q)
  - 微信公众号「自动驾驶之心」
    - [2023-07-04，最新综述！AIGC到底是什么？都有哪些应用？一文尽览！](https://mp.weixin.qq.com/s/DseSOGMdsmZGfF_ep-wpSg)
    - [2023-08-14，超越UniAD！FusionAD：预测与规划任务的多模态融合方案](https://mp.weixin.qq.com/s/-IC9ZWRPUWB83Lj43YtQSw)
    - [2024-04-08，一文看懂llama2（原理&模型&训练）](https://mp.weixin.qq.com/s/XP4xYbepZqTEOKWT_I-5ww)
  - 微信公众号「酷酷的群」
    - [2023-07-12，InstructGPT：语言模型的人类反馈指令对齐](https://mp.weixin.qq.com/s/qMpGxhpixut5-7YHcq1OOw)
  - 微信公众号「汀丶人工智能」
    - [2023-07-16，人工智能大语言模型微调技术：SFT 监督微调、LoRA 微调方法、P-tuning v2 微调方法、Freeze 监督微调方法](https://mp.weixin.qq.com/s/N0Z1Kq0mrVrK-RED_gvJmw)
  - 微信公众号「吃果冻不吐果冻皮」
    - [2023-07-12，百川智能大模型baichuan-13B技术剖析](https://mp.weixin.qq.com/s/L3V3a4h3ZJtTM0SXacrZsg)
    - [2024-04-19，迄今为止最强大的开源 LLM，15 万亿 Token 预训练的 LLaMA3 强势来袭](https://mp.weixin.qq.com/s/PmQL51LYPIzoTF5MBNrppg)
  - 微信公众号「OpenMMLab」
    - [2023-07-19，大模型社区再掀波澜，Meta重磅开源LLAMA-2，性能升级可商用](https://mp.weixin.qq.com/s/Eqh-ED4BgiR4BBQQbwXAmA)
  - 微信公众号「高通中国」
    - [2023-07-19，高通携手Meta利用Llama 2赋能终端侧AI应用](https://mp.weixin.qq.com/s/LwWoDUMUN6Isdee2vzpUwg)
  - 微信公众号「pythonLLM智能」
    - [2023-07-19，更强的Llama 2开源，可直接商用](https://mp.weixin.qq.com/s/GcDo9jRv8xPhtuS30HNSNg)
  - 微信公众号「包包算法笔记」
    - [2023-07-19，大模型开源社区的原子弹Llama2](https://mp.weixin.qq.com/s/RvAyXJ9KWqJ73XO7ZL1McA)
    - [2023-08-17，大模型面试八股含答案](https://mp.weixin.qq.com/s/qTXXEUeEbpR8EpIPoSAx5g)
    - [2023-08-21，从零训练大模型教程](https://mp.weixin.qq.com/s/qQDV2L7EBQLivkoONgXR9A)
    - [2023-08-26，大模型微调技术​报告汇总](https://mp.weixin.qq.com/s/4yAlLjvd-V1WI4fe_s9kgw)
    - [2023-08-28，判断场景是否适合大模型](https://mp.weixin.qq.com/s/OOea-WC3dFdCC7iNKQcBMw)
    - [2023-08-31，大模型来自面试的一些体会和分享](https://mp.weixin.qq.com/s/S7YlHn0ss0ApP0AC4waL4Q)
    - [2024-04-19，大模型重磅！Llama3发布！](https://mp.weixin.qq.com/s/FqkX3-iuxQdPHiRwI8CTNA)
  - 微信公众号「SimpleAI」
    - [2023-07-21，基于 LoRA 的 RLHF: 记一次不太成功但有趣的百川大模型调教经历](https://mp.weixin.qq.com/s/4dt3XiLnZN7Q17VHz3lsng)
  - 微信公众号「NLP工作站」
    - [2023-07-20，Llama2技术细节&开源影响](https://mp.weixin.qq.com/s/rHJkJw9TFGaAR8bWDM5wmg)
    - [2024-02-22，关于Google开源Gemma的一些想法](https://mp.weixin.qq.com/s/H2ie4vuhLqr4UKtgvZZtEQ)
    - [2024-03-29，Qwen1.5-MoE模型：2.7B的激活参数量达到7B模型的性能](https://mp.weixin.qq.com/s/FTd9L6HzpV-5AoT20V8YyQ)
    - [2024-04-06，Qwen1.5开源32B模型-将开源进行到底](https://mp.weixin.qq.com/s/WOiyQYSs5XZzSsn6hdb_Ww)
  - 微信公众号「对白的算法屋」
    - [2023-07-27，北交大TransGPT，开源了！](https://mp.weixin.qq.com/s/jSwvUIbNI_VQTBWGmwd3wg)
    - [2023-08-14，科大讯飞星火大模型2.0 终于体验上了！](https://mp.weixin.qq.com/s/fp3mnMLlh5oL5q7G0zsnpQ)
  - 微信公众号「Llama中文社区」
    - [2023-07-26，欢迎加入Llama中文社区！](https://mp.weixin.qq.com/s/mYdQ8L-J9hD8g3kesjDYmw)
    - [2023-08-01，首发！真正意义上的Llama2中文版大模型](https://mp.weixin.qq.com/s/lExUU7z_MvgJ7tzQPF8tUQ)
    - [2023-08-13，零门槛没GPU也能训练自己的大语言模型，Llama中文社区推出共享训练平台！](https://mp.weixin.qq.com/s/uJc-67VyF9u3a72nMFjdvQ)
    - [2023-08-31，首批大模型牌照发放，我们还能做些什么？](https://mp.weixin.qq.com/s/srKxGlbySQw8NKgK4kHupA)
    - [2024-04-19，和Llama中文社区一起玩转Llama3](https://mp.weixin.qq.com/s/b749y1NZKCY14a4gUmRTMw)
  - 微信公众号「极客公园」
    - [2023-07-25，一文读懂 OpenAI 创始人的「世界币」](https://mp.weixin.qq.com/s/7E2O2-iXt-4DCOUgldvfUQ)
  - 微信公众号「智车科技」
    - [2023-07-16，数据闭环，通向高阶自动驾驶的必经之路](https://mp.weixin.qq.com/s/TQQ5qIWtonM1pZ83jZOK7A)
  - 微信公众号「AILab笔记」
    - [2023-06-08，【文献】视觉transformer研究进展——史上最全综述](https://mp.weixin.qq.com/s/zCbFEl8pvPIfjnfIgv8Hqw)
  - 微信公众号「CVer」
    - [2023-08-02，ICCV 2023｜目标检测新突破！AlignDet：支持各类检测器完全自监督预训练的框架](https://mp.weixin.qq.com/s/t7jlTyUP6UxplpythX0dOw)
  - 微信公众号「EmacsTalk」
    - [2023-08-13，大模型入门指南](https://mp.weixin.qq.com/s/9nJ7g2mo7nOv4iGXT_CPNg)
  - 微信公众号「深度学习初学者」
    - [2023-08-18，决策树、随机森林、bagging、boosting、Adaboost、GBDT、XGBoost总结](https://mp.weixin.qq.com/s/OP_RM1Vl_PcIChCuuCaEXA)
  - 微信公众号「机器懂语言」
    - [2023-08-26，Stable Diffusion 文生图技术原理](https://mp.weixin.qq.com/s/bNJZNEt7ftWCk5J0NwNz0A)
  - 微信公众号「壹零社」
    - [2023-02-10，下一个ChatGPT？去中心化社交软件迎来现象级产品](https://mp.weixin.qq.com/s/rHnNMNNJLL-QFx3Uj97ekg)
  - 微信公众号「长城汽车」
    - [2023-08-18，DriveGPT与ChatGPT分不清楚？一起来认识这位全能选手](https://mp.weixin.qq.com/s/sE3JeBoLcZhEdJMT_oy_xg)
  - 微信公众号「稀土掘金技术社区」
    - [2024-02-23，谷歌最强开源大模型亮相！Gemini技术下放，笔记本就能跑，可商用](https://mp.weixin.qq.com/s/46ilHz7lGPdUnaxnwxPNRA)
  - 微信公众号「码科智能」
    - [2024-02-09，小鹏开源AI视频生成项目！在任何场景中的无缝插入任何对象，Corner Case将不复存在](https://mp.weixin.qq.com/s/uF44KNOIVX5k6Qyu6ccsxQ)
    - [2024-02-21，DriveVLM：自动驾驶和大型视觉语言模型的融合（理想汽车）](https://mp.weixin.qq.com/s/58rm-zVnVTzM52Hn2EjIYQ)
    - [2024-02-23，欢迎 Gemma: Google 推出可商用的大语言模型，主打开源和轻量！](https://mp.weixin.qq.com/s/VEJxO8UpVdNzqkxyKQRXaA)
    - [2024-03-04，Open Sora Plan! 北大-兔展AIGC联合实验室共同发起，希望通过开源社区的力量复现Sora](https://mp.weixin.qq.com/s/FcJN-95C4Ox_uYpNTCwn9A)
    - [2024-04-10，又一大模型技术开源！有道自研 RAG 引擎 QAnything 正式开放下载，支持任意格式的文件问答](https://mp.weixin.qq.com/s/1kgW5cUds3slium3g1aWow)
  - 微信公众号「AI闲谈」
    - [2024-02-20，追本溯源：OpenAI Sora 技术报告解读](https://mp.weixin.qq.com/s/FYIC3F5po7_v0VP89pEORQ)
  - 微信公众号「Second State」
    - [2024-02-22，本地运行 Google 最新开源的 Gemma 系列模型](https://mp.weixin.qq.com/s/RrSZTli9rcehOb3FHj9NuA)
  - 微信公众号「AI大模型实验室」
    - [2024-02-22，谷歌发布最强大模型Gemma，性能碾压Llama 2](https://mp.weixin.qq.com/s/8S7ExKurnJrj3LWUAGRPPQ)
    - [2024-04-11，Meta确认5月发布Llama 3，参数量达1400亿](https://mp.weixin.qq.com/s/KaVV0iiU7A3h8Y2Z7PIjkQ)
    - [2024-04-13，小模型的优势越来越明显了](https://mp.weixin.qq.com/s/tM3q-bp6Kq93f9vBbkPE1A)
    - [2024-04-15，杨立昆：目标驱动AI才是未来](https://mp.weixin.qq.com/s/eaxMQbLf_akGGEMkaNwLyg)
  - 微信公众号「董董灿是个攻城狮」
    - [2024-02-21，OpenAI 开放 Sora 内测资格申请通道，附手把手教学](https://mp.weixin.qq.com/s/18Nm_Uy2p7Y8LzKruHIdww)
  - 微信公众号「自动驾驶Daily」
    - [2024-02-23，清华&理想 | DRIVEVLM：自动驾驶和大型视觉语言模型的融合（复杂条件下超越所有SOTA）](https://mp.weixin.qq.com/s/wFl6PSss3haVmLk0m-tlZg)
  - 微信公众号「MicroComputer」
    - [2024-02-22，TensorRT LLM加速Gemma！NVIDIA与谷歌牵手，RTX助推AI聊天](https://mp.weixin.qq.com/s/UmLziuo5kVrVF2AVqd8gPg)
  - 微信公众号「Xsuperzone」
    - [2024-02-23，NVIDIA TensorRT-LLM 为 Google Gemma 加速推理](https://mp.weixin.qq.com/s/W4hbfsrCqWjSLVFHeGvobQ)
  - 微信公众号「Datawhale」
    - [2023-04-22，《ChatGPT开发应用指南》，Datawhale开源了！](https://mp.weixin.qq.com/s/UiW0z4Eb4cSw6YRgAZ7GMQ)
    - [2024-04-07，一文带你了解基于大模型的Agent](https://mp.weixin.qq.com/s/tkdNkUIdmWoy_Ib37wiebQ)
    - [2024-04-11，行业巨变！LLama3要来了](https://mp.weixin.qq.com/s/WhR1CIJxF8c_kO3i6Lx98A)
  - 微信公众号「蜂耘网」
    - [2024-03-04，北大发起Open-Sora开源计划，研究“国产版sora”](https://mp.weixin.qq.com/s/N5zoOafYLYZfxOzulqjNjg)
  - 微信公众号「AIoffer」
    - [2023-08-24，商汤研究院基础视觉组(大模型专题)正式员工（校招、社招）[目前还有多个HC，含相应资深岗位需求]&实习生长期招聘](https://mp.weixin.qq.com/s/fFqeCh-kLbfcCqO97Jl6yQ)
  - 微信公众号「数智笔记」
    - [2024-04-04，2024检索增强生成RAG最新综述](https://mp.weixin.qq.com/s/F-shRy1m7wQIS87ujOS7Dw)
  - 微信公众号「AI大模型应用实践」
    - [2024-04-10，一文彻底搞懂Self-RAG【上】：自省式RAG的原理与应用](https://mp.weixin.qq.com/s/3e8GG6iO7DVat5TSUFbCUQ)
  - 微信公众号「优必选科技」
    - [2024-04-10，优必选亮相首届中国人形机器人产业大会暨具身智能峰会](https://mp.weixin.qq.com/s/_nuwVkwOa56IcojNSW-1TA)
  - 微信公众号「AIGC开放社区」
    - [2024-04-10，Llama 3下月正式发布，继续开源！](https://mp.weixin.qq.com/s/_iWt5oEcJgRyj0AMpIMRrQ)
    - [2024-04-10，谷歌重磅发布Gemini 1.5 Pro：能自动写影评，理解视频！](https://mp.weixin.qq.com/s/E-0c8cHZcvga8eNqdu1msA)
  - 微信公众号「Meet DSA」
    - [2024-03-29，大语言模型硬件加速器综述](https://mp.weixin.qq.com/s/rtq8e_zVUWLc-vkT4V0qzQ)
  - 微信公众号「RUC AI Engine」
    - [2024-03-18，ICLR 2024 因果推断相关论文总结](https://mp.weixin.qq.com/s/zE4gCtd3uM0OD6d4aS9BNQ)
    - [2024-03-30，AI-Engine实验室招生| We Want You!](https://mp.weixin.qq.com/s/0BFY6nHouLgSGd5cOizIIg)
    - [2024-04-07，ICLR 2024 大语言模型多智能体研究总结](https://mp.weixin.qq.com/s/ROTFmXMarvKmbop4wT8gDw)
  - 微信公众号「开放知识图谱」
    - [2024-04-07，开源开放 | OpenRAG Base：RAG的开源开放知识库](https://mp.weixin.qq.com/s/MZ4jSH1torrEpYGTLTkiEw)
  - 微信公众号「AI不止算法」
    - [2024-04-09，全网首篇从tensorRT-LLM MoE CUDA kernel角度理解Mixtral-8x7b的推理加速及展望](https://mp.weixin.qq.com/s/3PsVUba-kTLIHK_s0RA2ow)
  - 微信公众号「大猿搬砖简记」
    - [2024-03-11，图解Mixtral 8 * 7b推理优化原理与源码实现](https://mp.weixin.qq.com/s/jjZQ4A-rvk_e-woKLlNTVQ)
    - [2024-03-29，图解大模型计算加速系列之：vLLM核心技术PagedAttention原理](https://mp.weixin.qq.com/s/-5EniAmFf1v9RdxI5-CwiQ)
    - [2024-04-06，图解大模型计算加速系列：vLLM源码解析1，整体架构](https://mp.weixin.qq.com/s/r_t6_zMvPT7za82MZX4oRA)
    - [2024-04-12，图解大模型计算加速系列：vLLM源码解析2，调度器策略(Scheduler)](https://mp.weixin.qq.com/s/UCdqQUM_9a36uXkO36wpSg)
  - 微信公众号「芝士AI吃鱼」
    - [2024-04-11，突破传统RAG限制！Adaptive-RAG实现高效复杂查询处理](https://mp.weixin.qq.com/s/PszyHnvTfQ6ZZZN89ZCxwg)
    - [2024-04-21，RAG与LLM本身知识存在冲突时，大模型如何抉择？](https://mp.weixin.qq.com/s/0nkvkyLEarxR4iu6rNd6Qg)
  - 微信公众号「oldpan博客」
    - [2024-01-03，大模型笔记！以LLAMA为例，快速入门LLM的推理过程](https://mp.weixin.qq.com/s/xPjuBitTw0c_kYy2zg2plw)
    - [2024-03-19，NVIDIA大语言模型落地的全流程解析](https://mp.weixin.qq.com/s/-sNnuDvkucUB_9K9RBfDEw)
    - [2024-03-20，TensorRT-LLM初探（二）简析了结构，用的更明白](https://mp.weixin.qq.com/s/Jk-AK84sllBbkDDpvkv62w)
    - [2024-03-21，高性能 LLM 推理框架的设计与实现](https://mp.weixin.qq.com/s/zys9KvQWbbdRHkOyhzZqUw)
    - [2024-04-21，搞懂 NVIDIA GPU 性能指标 很容易弄混的一个概念： Utilization vs Saturation](https://mp.weixin.qq.com/s/6PcF2RwGdm1G0JllGSS3jw)
    - [2024-04-22，快速提升性能，如何更好地使用GPU（上）](https://mp.weixin.qq.com/s/dUj058iBzYm-J2vlS5DfNA)
  - 微信公众号「人工智能大讲堂」
    - [2024-04-16，Facebook开源大模型可视分析工具：Transparency Tool ，将Transformer扒的一干二净](https://mp.weixin.qq.com/s/TSOkh5LEnE0sraE6yGRaCw)
  - 微信公众号「手写AI」
    - [2024-04-18，人形机器人哪家好？万字总结人形机器人发展近况！](https://mp.weixin.qq.com/s/hubkOpV521iDmEwkL1rWFg)
  - 微信公众号「Founder Park」
    - [2024-04-19，Llama 3 发布！目前最强开源大模型，全面登陆 Meta 系产品，即将推出 4000 亿模型](https://mp.weixin.qq.com/s/Ik29LVChNrq8aou8RXVg3Q)
  - 微信公众号「智能涌现」
    - [2024-04-19，Meta震撼发布Llama 3，一夜重回开源大模型铁王座](https://mp.weixin.qq.com/s/QJC76vH9ZrynQalkh0rXhg)
  - 微信公众号「苏哲管理咨询」
    - [2024-02-25，英伟达（NVIDA）崛起不平凡之路--老黄全球AI芯片新帝国简史](https://mp.weixin.qq.com/s/4c8FtVeJmNlXL6akj5lj8A)
    - [2024-03-31，杨立昆教授在哈佛大学数学系演讲稿-关于人工智能世界新模型](https://mp.weixin.qq.com/s/BUCKq4SWEMqwsy3gi_GULw)
    - [2024-04-02，杨立昆教授哈佛大学数学系演讲稿全文-目标驱动的人工智能世界新模型](https://mp.weixin.qq.com/s/itFaooocbcSKVkAP-kERyQ)
  - 微信公众号「美团技术团队」
    - [2024-04-11，美团外卖基于GPU的向量检索系统实践](https://mp.weixin.qq.com/s/pPl-anyQnFNFkmBlVsrBpA)
  - 微信公众号「大模型生态圈」
    - [2024-03-18，大模型推理百倍加速之KV cache篇](https://mp.weixin.qq.com/s/Rio4MYuWBOk7GDzoATp3qA)
    - [2024-03-18，LLM百倍推理加速之量化篇](https://mp.weixin.qq.com/s/jbpVBZLZ0AkrP7bacY5mKw)
    - [2024-03-21，研发大模型的血液--万字长文详谈数据工程](https://mp.weixin.qq.com/s/_vbqReTwOkN_wZi1tqtDpA)
    - [2024-03-22，LLM推理：GPU资源和推理框架选择](https://mp.weixin.qq.com/s/qUaLOXZmk1xyGHGKX4ZtpQ)
    - [2024-03-27，LLM 推理加速方式汇总](https://mp.weixin.qq.com/s/IlaQw6Ut25NNoTZkxs63Vg)
    - [2024-03-31，通往 LLM 算法工程师之路](https://mp.weixin.qq.com/s/1LzZ3HeXAYxrhi3cmAUL0A)
    - [2024-04-26，LLM推理量化：FP8 VS INT8](https://mp.weixin.qq.com/s/e7QZC1qNkETXNXZpcD9cRg)
  - 微信公众号「前沿技术汇」
    - [2024-03-23，卷积神经网络（Convolutional Neural Network）的重要概念](https://mp.weixin.qq.com/s/VMPBhe2VmGoGE-1p-_OLQQ)
  - 微信公众号「CPP开发者」
    - [2024-04-22，用 1000 行 C 代码手搓了一个大模型，Mac 即可运行，特斯拉前AI总监爆火科普 LLM](https://mp.weixin.qq.com/s/qitXPAmHSQFGfBxNLMMnpg)
  - 微信公众号「八一菜刀」
    - [2024-04-02，创业：大模型RAG系统三个月的开发心得和思考](https://mp.weixin.qq.com/s/Np-UUBtAGzZSE-hi5jfHrQ)
  - 微信公众号「AIGC先锋科技」
    - [2024-04-13，复旦&北大&上海交大开源 Chinese-Tiny-LLM/ | 以中文为中心的大语言模型 ！](https://mp.weixin.qq.com/s/buTWv6eKrYvwN69mEwWIag)
    - [2024-04-25，​中科院联合多所高校提出 AdvLoRA | 通过数据增强，攻击检测等对抗模型攻击，提高模型安全性和鲁棒性！](https://mp.weixin.qq.com/s/37t5kwgPQzORR3Sxmxy14w)
  - 微信公众号「DeepLearning笔记」
    - [2024-04-13，如何微调Meta Llama-3 8B](https://mp.weixin.qq.com/s/mwaCtibKkFjQzPhDRKtCOw)
    - 微信公众号「DeepPrompting」
        - [2024-01-09，LLM推理库TensorRT-LLM深入分析](https://mp.weixin.qq.com/s/hI6maWtVGHnTi0uGPj6tmA)

  - [知乎「Lil2J」](https://www.zhihu.com/people/ai-er-sha-la-wei-81)
    - [2024-03-02，从0开始预训练1.4b中文大模型实践](https://zhuanlan.zhihu.com/p/684946331)
  - [知乎「老苏聊AI」](https://www.zhihu.com/people/su-pin-yu)
    - [2023-12-16，中文大模型预训练数据集介绍](https://zhuanlan.zhihu.com/p/672560962)
  - [知乎「猛猿」](https://www.zhihu.com/people/lemonround)
    - [2023-02-25，ChatGPT技术解析系列之：GPT1、GPT2与GPT3](https://zhuanlan.zhihu.com/p/609367098)
  - [华尔街见闻](https://wallstreetcn.com/)
    - [2023-07-12，5年20亿美元！毕马威与微软签了大单，会计师事务所要All In AI了](https://wallstreetcn.com/articles/3693053)
  - [Jay Alammar](https://jalammar.github.io/)
    - [2018-06-27，The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)
  - 「[The official LangChain blog](https://blog.langchain.dev/)」
    - [2023-07-18，Announcing LangSmith, a unified platform for debugging, testing, evaluating, and monitoring your LLM applications](https://blog.langchain.dev/announcing-langsmith/)






## Videos

  - bilibili「OpenMMLab」
    - [2024-01-03，书生·浦语大模型全链路开源体系](https://www.bilibili.com/video/BV1Rc411b7ns/)
  - bilibili「ChatGLM」
    - [2023-07-19，【官方教程】ChatGLM2-6B 部署与微调](https://www.bilibili.com/video/BV1D94y1i7Qp/)
  - bilibili「二次元的Datawhale」
    - [2023-04-25，学会如何使用大模型，让创意有能力落地成应用：HuggingLLM，Hugging未来](https://www.bilibili.com/video/BV1ek4y1J7Rd/)



## Jobs and Interview

  - 微信公众号「CVHub」
    - [2024-04-12，自变量机器人（X Square）- 具身智能企业招聘 | 机器人大模型、多模态、SLAM、机器人开发、仿真、ROS](https://mp.weixin.qq.com/s/H8r-KEiLso7JZTKO-PrjHA)
  - 微信公众号「美团技术团队」
    - [2024-03-21，美团自动配送车2024春季招聘 | 社招专场](https://mp.weixin.qq.com/s/2e0g-7fD8Fbp65LbjGdVnA)
  - 微信公众号「AINLP」
    - [2024-04-03，蚂蚁集团智能引擎团队招聘大模型相关算法工程师](https://mp.weixin.qq.com/s/Vre7ANtyAhTuQTxtRhUn9Q)
    - [2024-04-19，【社招】NewsBreak北京招聘：多模态内容理解算法工程师（​北京）](https://mp.weixin.qq.com/s/OOn5Y2_BBJyq4wuvHmU--A)
  - 微信公众号「大模型生态圈」
    - [2024-04-21，推理部署工程师面试题库](https://mp.weixin.qq.com/s/q46vKFPlQhcN7LyZNTRhXA)
  - 微信公众号「AIGC小白入门记」
    - [2024-04-20，面试小米汽车，不想去，拒了offer。。。](https://mp.weixin.qq.com/s/8UIlJwz3AJTTZNvwxLamtg)
    - [2024-04-21，算法工程师面试常考手撕题（更新）](https://mp.weixin.qq.com/s/UlmNOIwohQJjl_UTpcw_uw)
    - [2024-04-21，算法工程师面试题笔记](https://mp.weixin.qq.com/s/IKaLrqAeWyYes9mKMKZh0g)


## Star History

<img alt="Star History Chart" src="https://api.star-history.com/svg?repos=codingonion/awesome-llm-and-aigc&type=Date" />