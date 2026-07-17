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


