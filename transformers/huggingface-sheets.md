[huggingface-on-sheets](https://huggingface.co/spaces/JournalistsonHF/huggingface-on-sheets) 

[Understanding the DistilBart Model and ROUGE Metric](https://machinelearningmastery.com/understanding-the-distilbart-model-and-rouge-metric/)

[hftools](https://github.com/ziozzang/hftools)

```
go install github.com/ziozzang/hftools/cmd/hftools@latest
export HF_TOKEN=hf_xxx
hftools d --filter '*_q4_?.gguf|*.json' owner/model
```

- Resume on by default — multipart Range downloads pick up at the exact byte offset, and --retries -1 rides out multi-hour Hub outages instead of failing.

- Hash verification that actually matters for air-gap. When you're copying multi-GB models onto an offline box, "did this file survive the transfer intact?" isn't paranoia — it's basically mandatory. Every file is checked against Git blob SHA-1 / LFS SHA-256, with standard .sha256/.sha1sum you can re-verify anywhere, no network needed.

- Convert between flat downloads and the HF cache layout, both directions. Pull a model in a clean flat dir, then export it into ~/.cache/huggingface so transformers/diffusers load it offline — or import an existing cache back out. Sounds minor until you actually need it across an air gap, then it's a lifesaver.

- Bonus: peek reads a safetensors/GGUF header via one Range request (tensors, dtypes, params, ~few MB); scan flags unsafe pickle imports before you load a random checkpoint


### Huggingface DLC

 Hugging Face Embedding DLC is a new purpose-built Inference Container to easily deploy Embedding Models in a secure and managed environment.

 The DLC is powered by Text Embedding Inference (TEI) a blazing fast and memory efficient solution for deploying and serving Embedding Models. TEI enables high-performance extraction for the most popular models, including FlagEmbedding, Ember, GTE and E5. TEI implements many features such as:

- No model graph compilation step
- Small docker images and fast boot times
- Token based dynamic batching
- Optimized transformers code for inference using Flash Attention, Candle and cuBLASLt
- Safetensors weight loading
- Production ready (distributed tracing with Open Telemetry, Prometheus metrics)

TEI supports the following model architectures

- BERT/CamemBERT, e.g. BAAI/bge-large-en-v1.5 or Snowflake/snowflake-arctic-embed-m
- RoBERTa, sentence-transformers/all-roberta-large-v1
- XLM-RoBERTa, e.g. sentence-transformers/paraphrase-xlm-r-multilingual-v1
- NomicBert, e.g. jinaai/jina-embeddings-v2-base-en
- JinaBert, e.g. nomic-ai/nomic-embed-text-v1.5

Resources:

 -[How to deploy Embedding Models to Amazon SageMaker using new Hugging Face Embedding DLC](https://huggingface.co/docs/sagemaker/en/examples/sagemaker-sdk-deploy-embedding-models)

 
