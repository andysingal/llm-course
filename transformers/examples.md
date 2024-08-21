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

```py
import torch
from PIL import Image
from transformers import AutoModel, AutoTokenizer

model = AutoModel.from_pretrained('openbmb/MiniCPM-V-2_6-int4', trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained('openbmb/MiniCPM-V-2_6-int4', trust_remote_code=True)
model.eval()

image = Image.open('xx.jpg').convert('RGB')
question = 'What is in the image?'
msgs = [{'role': 'user', 'content': [image, question]}]

res = model.chat(
    image=None,
    msgs=msgs,
    tokenizer=tokenizer
)
print(res)

## if you want to use streaming, please make sure sampling=True and stream=True
## the model.chat will return a generator
res = model.chat(
    image=None,
    msgs=msgs,
    tokenizer=tokenizer,
    sampling=True,
    temperature=0.7,
    stream=True
)

generated_text = ""
for new_text in res:
    generated_text += new_text
    print(new_text, flush=True, end='')
```

```py
import re
import torch
from transformers import pipeline

pipe = pipeline("text-generation", model="AI-MO/NuminaMath-7B-TIR", torch_dtype=torch.bfloat16, device_map="auto")

messages = [
    {"role": "user", "content": "For how many values of the constant $k$ will the polynomial $x^{2}+kx+36$ have two distinct integer roots?"},
]
prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

gen_config = {
    "max_new_tokens": 1024,
    "do_sample": False,
    "stop_strings": ["```output"], # Generate until Python code block is complete
    "tokenizer": pipe.tokenizer,
}

outputs = pipe(prompt, **gen_config)
text = outputs[0]["generated_text"]
print(text)

# WARNING: This code will execute the python code in the string. We show this for eductional purposes only.
# Please refer to our full pipeline for a safer way to execute code.
python_code = re.findall(r"```python(.*?)```", text, re.DOTALL)[0]
exec(python_code)
```
### HuggingFace Transformers library (multi-turn dialogue)
```py
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig
tokenizer = AutoTokenizer.from_pretrained("FarReelAILab/Machine_Mindset_en_ENTJ", use_fast=False, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("FarReelAILab/Machine_Mindset_en_ENTJ", device_map="auto", torch_dtype=torch.float16, trust_remote_code=True)
model.generation_config = GenerationConfig.from_pretrained("FarReelAILab/Machine_Mindset_en_ENTJ")
messages = []
print("####Enter 'exit' to exit.")
print("####Enter 'clear' to clear the chat history.")
while True:
    user=str(input("User:"))
    if user.strip()=="exit":
        break
    elif user.strip()=="clear":
        messages=[]
        continue
    messages.append({"role": "user", "content": user})
    response = model.chat(tokenizer, messages)
    print("Assistant:", response)
    messages.append({"role": "assistant", "content": str(response)})
```

Resources:
- https://github.com/huggingface/transformers/releases/tag/v4.41.0
- https://huggingface.co/PandaVT/MBTIGPT_en_ENTJ
