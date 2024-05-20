```py
import torch
from transformers import pipeline

pipe = pipeline("text-generation", model="Unbabel/TowerInstruct-v0.1", torch_dtype=torch.bfloat16, device_map="auto")
# We use the tokenizer’s chat template to format each message - see https://huggingface.co/docs/transformers/main/en/chat_templating
messages = [
    {"role": "user", "content": "Translate the following text from Portuguese into English.\nPortuguese: Um grupo de investigadores lançou um novo modelo para tarefas relacionadas com tradução.\nEnglish:"},
]
prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
outputs = pipe(prompt, max_new_tokens=256, do_sample=False)
print(outputs[0]["generated_text"])
```


```py
from transformers import AutoModelForCausalLM, BitsAndBytesConfig, AutoTokenizer

model_id = "facebook/opt-125m"

model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=BitsAndBytesConfig(load_in_4bit=True))
tokenizer = AutoTokenizer.from_pretrained(model_id)

model.dequantize()

text = tokenizer("Hello my name is", return_tensors="pt").to(0)

out = model.generate(**text)
print(tokenizer.decode(out[0]))
```


Resources:
- https://github.com/huggingface/transformers/releases/tag/v4.41.0 
