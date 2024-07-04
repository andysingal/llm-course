# Huggingface Accelerate to train on multiple GPUs 
## [What is Huggingface accelerate](https://jarvislabs.ai/blogs/accelerate) 
Huggingface accelerate allows us to use plain PyTorch on

- Single and Multiple GPU
- Used different precision techniques like fp16, bf16
- Use optimization libraries like DeepSpeed and FullyShardedDataParallel

[accelerate-classifier](https://github.com/svishnu88/multi-gpu-hugging-face/blob/main/accelerate_classifier.py) 

When you run accelerate config, you’ll be prompted with a series of options to configure your training environment.

Sharding strategy
FSDP offers a number of sharding strategies to select from:

1. FULL_SHARD - shards model parameters, gradients and optimizer states across workers; select 1 for this option
2. SHARD_GRAD_OP- shard gradients and optimizer states across workers; select 2 for this option
3. NO_SHARD - don’t shard anything (this is equivalent to DDP); select 3 for this option
4. HYBRID_SHARD - shard model parameters, gradients and optimizer states within each worker where each worker also has a full copy; select 4 for this option
5. HYBRID_SHARD_ZERO2 - shard gradients and optimizer states within each worker where each worker also has a full copy; select 5 for this option

C. CPU offload
You could also offload parameters and gradients when they are not in use to the CPU to save even more GPU memory and help you fit large models where even FSDP may not be sufficient. This is enabled by setting fsdp_offload_params: true when running accelerate config.

D. Wrapping policy
FSDP is applied by wrapping each layer in the network. The wrapping is usually applied in a nested way where the full weights are discarded after each forward pass to save memory for use in the next layer. The auto wrapping policy is the simplest way to implement this and you don’t need to change any code. You should select fsdp_auto_wrap_policy: TRANSFORMER_BASED_WRAP to wrap a Transformer layer and fsdp_transformer_layer_cls_to_wrap to specify which layer to wrap (for example BertLayer).




Resources:
-[pytorch-accelerated](https://pytorch-accelerated.readthedocs.io/en/latest/quickstart.html) 
- [accelerate-train-on-tpu](https://colab.research.google.com/github/yellowback/notebooks/blob/main/accelerate_train_on_tpu.ipynb)
- [Accelerate + LoRA fine-tuning](https://hackmd.io/@3tffdwdTRT-Eev0i-1ljZA/SJgQ4dUP2)
- [Hugging Face Accelerate Super Charged With Weights & Biases](https://wandb.ai/gladiator/HF%20Accelerate%20+%20W&B/reports/Hugging-Face-Accelerate-Super-Charged-With-Weights-Biases--VmlldzoyNzk3MDUx)


