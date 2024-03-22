[MinIO](https://github.com/minio/blog-assets/blob/main/hf_datasets_minio_integration/utils.py)

MinIO offers high-performance, S3 compatible object storage. Native to Kubernetes, MinIO is the only object storage suite available on every public cloud, every Kubernetes distribution, the private cloud and the edge. MinIO is software-defined and is 100% open source under GNU AGPL v3.

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
