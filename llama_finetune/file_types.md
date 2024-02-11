🚀 What is GGML or GGUF in the world of Large Language Models ? 🚀

GGUF / GGML are file formats for quantized models

GGUF is a new format introduced by the llama.cpp team on August 21st 2023. It is a replacement for GGML.

Basically, GGUF (i.e. "GPT-Generated Unified Format"), previously GGML, is a quantization method that allows users to use the CPU to run an LLM but also offload some of its layers to the GPU for a speed up.

📌 GGML is a C++ Tensor library designed for machine learning, facilitating the running of LLMs either on a CPU alone or in tandem with a GPU.

💡 GGUF (new)

💡 GGML (old)

Llama.cpp has dropped support for the GGML format and now only supports GGUF

------------

* GGUF contains all the metadata it needs in the model file (no need for other files like tokenizer_config.json) except the prompt template

* llama.cpp has a script to convert *.safetensors model files into *.gguf

* Transformers & Llama.cpp support both CPU, GPU and MPU inference

Being compiled in C++, with GGUF the inference is multithreaded.

↪️ GGML format recently changed to GGUF which is designed to be extensible, so that new features shouldn’t break compatibility with existing models. It also centralizes all the metadata in one file, such as special tokens, RoPE scaling parameters, etc. In short, it answers a few historical pain points and should be future-proof.

----------------

📌 GGUF (GGML) vs GPTQ

▶️ GPTQ is not the same quantization format as GGUF/GGML. They are different approaches with different codebases but have borrowed ideas from each other.

▶️ GPTQ is a post-training quantziation method to compress LLMs, like GPT. GPTQ compresses GPT models by reducing the number of bits needed to store each weight in the model, from 32 bits down to just 3-4 bits.

▶️ GPTQ analyzes each layer of the model separately and approximating the weights in a way that preserves the overall accuracy.

▶️ Quantizes the weights of the model layer-by-layer to 4 bits instead of 16 bits, this reduces the needed memory by 4x.

▶️ Achieves same latency as fp16 model, but 4x less memory usage, sometimes faster due to custom kernels, e.g. Exllama

----------------------------

▶️ There's also the bits and bytes library, which quantizes on the fly (to 8-bit or 4-bit) and is related to QLoRA. This is also knows as  dynamic quantization

▶️ And there's some other formats like AWQ: Activation-aware Weight Quantization - which is a quantization method similar to GPTQ. There are several differences between AWQ and GPTQ as methods but the most important one is that AWQ assumes that not all weights are equally important for an LLM’s performance. For AWQ, best to use the vLLM package

<img width="474" alt="Screenshot 2024-02-11 at 10 59 08 AM" src="https://github.com/andysingal/llm-course/assets/20493493/e671357e-0c39-4e86-a79b-dbb8fa26c03b">

Resources:
- [Democratizing LLMs: 4-bit Quantization for Optimal LLM Inference](https://towardsdatascience.com/democratizing-llms-4-bit-quantization-for-optimal-llm-inference-be30cf4e0e34)
