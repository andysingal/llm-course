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
