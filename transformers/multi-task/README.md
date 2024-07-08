[Multi-GPU Finetuning Secrets](https://medium.com/@kyeg/unlock-multi-gpu-finetuning-secrets-huggingface-models-pytorch-fsdp-explained-a58bab8f510e)

[Fine-tune Llama 3 with PyTorch FSDP and Q-Lora on Amazon SageMaker](https://www.philschmid.de/sagemaker-train-deploy-llama3)


## Tutorial

[Methods and tools for efficient training on a single GPU](https://huggingface.co/docs/transformers/en/perf_train_gpu_one) 

[[However, if the preferred batch size fits into memory, there’s no reason to apply memory-optimizing techniques because they can slow down the training. Just because one can use a large batch size, does not necessarily mean they should. As part of hyperparameter tuning, you should determine which batch size yields the best results and then optimize resources accordingly.]]


## Definitions

1. <strong>Half-precision</strong>: half precision (sometimes called FP16 or float16) is a binary floating-point computer number format that occupies 16 bits (two bytes in modern computers) in computer memory. It is intended for storage of floating-point values in applications where higher precision is not essential, in particular image processing and neural networks. By reducing the precision of certain variables to lower numerical formats like 16-bit floating point (fp16 or float16), we can speed up the computations. Because in this approach some computations are performed in half-precision, while some are still in full precision, the approach is called mixed precision training.

2. <strong>Mixed precision training</strong>: The main advantage of mixed precision training comes from saving the activations in half precision (fp16). Although the gradients are also computed in half precision they are converted back to full precision for the optimization step so no memory is saved here. While mixed precision training results in faster computations, it can also lead to more GPU memory being utilized, especially for small batch sizes.

3. <strong>Flash Attention 2</strong> You can speedup the training throughput by using Flash Attention 2 integration in transformers

- The most common optimizer used to train transformer models is Adam or AdamW (Adam with weight decay). Adam achieves good convergence by storing the rolling average of the previous gradients
- Trainer integrates a variety of optimizers that can be used out of box: adamw_hf, adamw_torch, adamw_torch_fused, adamw_apex_fused, adamw_anyprecision, adafactor, or adamw_bnb_8bit. More optimizers can be plugged in via a third-party implementation.
- <strong>Adafactor</strong>: Adafactor doesn’t store rolling averages for each element in weight matrices. Instead, it keeps aggregated information (sums of rolling averages row- and column-wise), significantly reducing its footprint. However, compared to Adam, Adafactor may have slower convergence in certain cases.
```training_args = TrainingArguments(per_device_train_batch_size=4, optim="adafactor", **default_args)```
Combined with other approaches (gradient accumulation, gradient checkpointing, and mixed precision training) you can notice up to 3x improvement while maintaining the throughput

- <strong>multi_tensor</strong>pytorch-nightly introduced torch.optim._multi_tensor which should significantly speed up the optimizers for situations with lots of small feature tensors


4. <strong> DeepSpeed ZeRO </strong>
DeepSpeed is an open-source deep learning optimization library that is integrated with 🤗 Transformers and 🤗 Accelerate. It provides a wide range of features and optimizations designed to improve the efficiency and scalability of large-scale deep learning training.

- If your model fits onto a single GPU and you have enough space to fit a small batch size, you don’t need to use DeepSpeed as it’ll only slow things down. However, if the model doesn’t fit onto a single GPU or you can’t fit a small batch, you can leverage DeepSpeed ZeRO + CPU Offload, or NVMe Offload for much larger models. In this case, you need to separately install the library, then follow one of the guides to create a configuration file and launch DeepSpeed:

- For an in-depth guide on DeepSpeed integration with Trainer, review the corresponding documentation, specifically the section for a single GPU. Some adjustments are required to use DeepSpeed in a notebook; please take a look at the corresponding guide.

[DeepSpeed Zero With the HuggingFace Trainer](https://wandb.ai/byyoung3/ml-news/reports/A-Guide-to-DeepSpeed-Zero-With-the-HuggingFace-Trainer--Vmlldzo2ODkwMDc4)

[DEEPSPEED](https://lightning.ai/docs/pytorch/stable/advanced/model_parallel/deepspeed.html)

[Fine-tune Falcon 180B with DeepSpeed ZeRO, LoRA & Flash Attention](https://www.philschmid.de/deepspeed-lora-flash-attention) 

5. Distributed Data Parallel: DistributedDataParallel (DDP) implements data parallelism at the module level which can run across multiple machines. Applications using DDP should spawn multiple processes and create a single DDP instance per process. DDP uses collective communications in the torch.distributed package to synchronize gradients and buffers. More specifically, DDP registers an autograd hook for each parameter given by model.parameters() and the hook will fire when the corresponding gradient is computed in the backward pass. Then DDP uses that signal to trigger gradient synchronization across processes. Please refer to DDP design note for more details.

[1-reference](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html)

[2-reference](https://yangkky.github.io/2019/07/08/distributed-pytorch-tutorial.html)

[Gradient Accumulation and Checkpointing](https://aman.ai/primers/ai/grad-accum-checkpoint/#:~:text=Gradient%20accumulation%20is%20a%20technique,after%20each%20batch%20of%20data.)





