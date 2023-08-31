# Response Data

We collected the response data of AlpaGasus2-QLoRA for evaluating and comparing the responses with Alpaca2.
Please run the 'generate.py' following the instructions below to collect the response data.

**Alpaca2**
```
python generate.py \
    --base_model 'meta-llama/Llama-2-13b-hf' \
    --lora_weight 'alpaca2' \
    --auth_token 'your authorization token' \
    --file_path 'AlpaGasus2-QLoRA/test_data/' \
    --save_path './results/' \
```

**AlpaGasus2**
```
python generate.py \
    --base_model 'meta-llama/Llama-2-13b-hf' \
    --lora_weight 'alpagasus2' \
    --auth_token 'your authorization token' \
    --file_path 'AlpaGasus2-QLoRA/test_data/' \
    --save_path './results/' \
```
