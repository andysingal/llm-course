# Deepspeed
DeepSpeed is a PyTorch optimization library that makes distributed training memory-efficient and fast. At it’s core is the Zero Redundancy Optimizer (ZeRO) which enables training large models at scale. ZeRO works in several stages:

- ZeRO-1, optimizer state partioning across GPUs
- ZeRO-2, gradient partitioning across GPUs
- ZeRO-3, parameteter partitioning across GPUs

Resources:
- [Deepspeed-Pytorch](https://lightning.ai/docs/pytorch/1.9.4/_modules/pytorch_lightning/strategies/deepspeed.html)
- [DeepSpeed bbe0afbb-b](https://www.kaggle.com/code/kerneler/starter-deepspeed-bbe0afbb-b/data)
- [DeepSpeed Mixture-of-Quantization (MoQ)](https://www.deepspeed.ai/tutorials/MoQ-tutorial/)

