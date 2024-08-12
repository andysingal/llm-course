AirLLM was released, which allows even relatively large LLM models to run on a small amount of GPU memory by calculating each layer on the GPU.

```py
from airllm import AutoModel

model = AutoModel.from_pretrained(
    "unsloth/Meta-Llama-3.1-405B-Instruct-bnb-4bit")

input_text = ['日本の首都は？',]

input_tokens = model.tokenizer(input_text,
      return_tensors="pt", 
      return_attention_mask=False, 
      truncation=True, 
      max_length=128, 
      padding=False)

generation_output = model.generate(
      input_tokens['input_ids'].cuda(), 
      max_new_tokens=10,
      return_dict_in_generate=True)

output = model.tokenizer.decode(generation_output.sequences[0])

print(output)
```
