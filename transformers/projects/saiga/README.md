# Saiga scripts

Download model:
```
python3 -c 'from huggingface_hub import snapshot_download; snapshot_download(repo_id="meta-llama/Meta-Llama-3-8B-Instruct", local_dir="models/llama-3-8b", ignore_patterns=["LICENSE", "README.md", "*.bin"])'
```

Fetch SFT dataset:
```
python3 -m scripts.compose_sft_dataset configs/datasets/sft_d1.json sft_d1_train.jsonl sft_d1_val.jsonl
```

Train SFT model with Unsloth:
```
python3 -m src.train_unsloth configs/models/saiga_llama3_8b_sft_m10.json sft_d1_train.jsonl sft_d1_val.jsonl models/saiga_llama3_8b_sft_m10_d1
```

Alternatively, train SFT model with vanilla:
```
python3 -m src.train_transformers configs/models/saiga_llama3_8b_sft_m10.json sft_d1_train.jsonl sft_d1_val.jsonl models/saiga_llama3_8b_sft_m10_d1
```

Fetch preferences dataset:
```
python3 -m scripts.compose_pref_dataset configs/datasets/pref_d2.json pref_d2_train.jsonl pref_d2_val.jsonl
```

Train KTO model with TRL:
```
python3 -m src.train_kto configs/models/saiga_llama3_8b_kto_m2.json pref_d2_train.jsonl pref_d2_val.jsonl models/saiga_llama3_8b_sft_m10_d1_kto_m2_d2
```
