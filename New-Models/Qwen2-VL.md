```py
!pip install git+https://github.com/huggingface/transformers

from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor

# モデルとプロセッサの準備
model = Qwen2VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2-VL-2B-Instruct", 
    torch_dtype="auto", 
    device_map="auto"
)
processor = AutoProcessor.from_pretrained(
    "Qwen/Qwen2-VL-2B-Instruct"
)
```

```py
from PIL import Image
import requests

# 画像の準備
image = Image.open("sample.jpg")

# メッセージの準備
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
            },
            {"type": "text", "text": "メッセージボードには何と書いてある？"},
        ],
    }
]

# 入力の準備
text_prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
inputs = processor(
    text=[text_prompt], 
    images=[image], 
    padding=True, 
    return_tensors="pt"
)
inputs = inputs.to("cuda")

# 推論の実行
output_ids = model.generate(**inputs, max_new_tokens=128)
generated_ids = [
    output_ids[len(input_ids) :]
    for input_ids, output_ids in zip(inputs.input_ids, output_ids)
]
output_text = processor.batch_decode(
    generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True
)
print(output_text)
```
