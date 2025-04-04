# Deepspeed
DeepSpeed is a PyTorch optimization library that makes distributed training memory-efficient and fast. At it’s core is the Zero Redundancy Optimizer (ZeRO) which enables training large models at scale. ZeRO works in several stages:

- ZeRO-1, optimizer state partioning across GPUs
- ZeRO-2, gradient partitioning across GPUs
- ZeRO-3, parameteter partitioning across GPUs

### Example
```py
# ----------------------------------
# Previous tensor parallelism method
# ----------------------------------
import os
import torch
import transformers
import deepspeed
from transformers.models.t5.modeling_t5 import T5Block
local_rank = int(os.getenv("LOCAL_RANK", "0"))
world_size = int(os.getenv("WORLD_SIZE", "1"))
# create the model pipeline
pipe = transformers.pipeline(task="text2text-generation", model="google/t5-v1_1-small", device=local_rank)
# Initialize the DeepSpeed-Inference engine
pipe.model = deepspeed.init_inference(
    pipe.model,
    mp_size=world_size,
    dtype=torch.float,
    injection_policy={T5Block: ('SelfAttention.o', 'EncDecAttention.o', 'DenseReluDense.wo')}
)
output = pipe('Input String')
```
[source](https://www.deepspeed.ai/tutorials/automatic-tensor-parallelism/)

### Examples:
- [nano-aha-moment](https://github.com/McGill-NLP/nano-aha-moment/blob/main/nano_r1.ipynb)


Resources:
- [Deepspeed-Pytorch](https://lightning.ai/docs/pytorch/1.9.4/_modules/pytorch_lightning/strategies/deepspeed.html)
- [DeepSpeed bbe0afbb-b](https://www.kaggle.com/code/kerneler/starter-deepspeed-bbe0afbb-b/data)
- [DeepSpeed Mixture-of-Quantization (MoQ)](https://www.deepspeed.ai/tutorials/MoQ-tutorial/)
- [DeepSpeed-Llama 2 7B-Chat](https://qiita.com/taka_yayoi/items/432182027f86fd104dcc)
- [Using multiple models with DeepSpeed](https://huggingface.co/docs/accelerate/en/usage_guides/deepspeed_multiple_model)

