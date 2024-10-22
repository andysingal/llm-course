```py
%pip install -qU huggingface_hub openai pydantic==1.10.8
```

```py
from huggingface_hub import login, create_inference_endpoint
from openai import OpenAI

# See https://huggingface.co/docs/inference-endpoints/pricing for details on instances

endpoint = create_inference_endpoint(
    name="llama3-8b-julien-demo",
    repository="meta-llama/Meta-Llama-3-8B-Instruct",
    framework="pytorch",
    task="text-generation",
    accelerator="neuron",
    vendor="aws",
    region="us-east-1",
    type="protected",
    instance_type="inf2",
    instance_size="x1",
    # https://huggingface.co/aws-neuron/optimum-neuron-cache/blob/main/inference-cache-config/llama3.json
    custom_image={
        "health_route": "/health",
        "env": {
            "MAX_INPUT_LENGTH": "1024",
            "MAX_TOTAL_TOKENS": "4096",
            "HF_NUM_CORES": "2",
            "HF_SEQUENCE_LENGTH": "4096",
            "HF_BATCH_SIZE": "1",
            "MAX_BATCH_SIZE": "1",
            "HF_AUTO_CAST_TYPE": "fp16",
            "MODEL_ID": "/repository",
        },
        "url": "registry.internal.huggingface.tech/hf-endpoints/neuronx-tgi:prod",
    },
)
```

 endpoint.wait()

```py
HF_TOKEN = "YOUR_HF_TOKEN" # read-only token

client = OpenAI(
    base_url=f"{endpoint.url}/v1/",
    api_key=HF_TOKEN,
)
chat_completion = client.chat.completions.create(
    model="tgi",
    messages=[
        {"role": "system", "content": "You are a helpful technical assistant giving detailed and factual answers."},
        {"role": "user", "content": "Why are transformers better models than LSTM?"}
    ],
    stream=True,
    max_tokens=1024,
)

# iterate and print stream
for message in chat_completion:
    print(message.choices[0].delta.content, end="")
```
endpoint.delete()

```py
import requests

API_URL = "https://api-inference.huggingface.co/models/jonathandinu/face-parsing"
headers = {"Authorization": "Bearer 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"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

output = query("/content/IMG_20221108_073555.jpg")
```



Resource:
- https://gitlab.com/juliensimon/huggingface-demos/-/blob/main/inference-endpoints/llama3-8b-openai-inf2.ipynb
- [face-parsing](https://www.analyticsvidhya.com/blog/2024/10/understanding-face-parsing/)
