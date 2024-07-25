[Mamba-Transformers](https://note.com/hatti8/n/na9782b7fa437)

[LLM-Conversation Summary](https://zhuanlan.zhihu.com/p/682539805)

[Dataset-lib-Tricks](https://www.ai-shift.co.jp/techblog/4271)

[Deepspeed-Zero-Training]()

```
{
    "zero_optimization": {
      "stage": 3,
      "offload_param": {
        "device": "cpu"
      },
      "offload_optimizer": {
        "device": "cpu"
      }
    },
    "gradient_accumulation_steps": 1,
    "train_micro_batch_size_per_gpu": 1,
    "gradient_clipping": 1.0,
    "fp16": {
      "enabled": true
    }
  }
```

FlashAttention has been proposed, which optimizes IO and use online softmax  to reduce both data movement from the GPU memory  and GPU cache.  

[How to Run Your Own Local LLM](https://hackernoon.com/how-to-run-your-own-local-llm-updated-for-2024) 

[autotrain-advanced](https://github.com/huggingface/autotrain-advanced)

Notebook:
[CommonLit RoBERTa](https://www.kaggle.com/code/tealgreen0503/commonlit-roberta-huggingface-trainer)
