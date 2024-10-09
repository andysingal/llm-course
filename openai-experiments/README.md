[My finetuned models beat OpenAI’s GPT-4](https://mlops.systems/posts/2024-07-01-full-finetuned-model-evaluation.html)

[openai-interpreter](https://colab.research.google.com/drive/1WKmRXZgsErej2xUriKzxrEAXdxMSgWbb?usp=sharing)

[Query SQL with Natural Language Using Azure OpenAI (NL2SQL)](https://cookbook.openai.com/examples/how_to_call_functions_with_chat_models)

[Langchain and OpenAI Vector Embedding Q/A System](https://dev.to/admantium/advanced-langchain-memory-tools-agents-4gki)


[Introducing vision to the fine-tuning API](https://openai.com/index/introducing-vision-to-the-fine-tuning-api/)

```py
import requests
import json

def chat(content):
  url = "https://api.openai.com/v1/chat/completions"
  headers = {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]
  }
  data = {
      "model": "gpt-3.5-turbo",
      "messages": [
          {"role": "user", "content": content}
      ],
      "temperature": 0,
  }

  response = requests.post(url=url, headers=headers, json=data)
  print(json.dumps(response.json(), indent=2))

  chat("Hi! I'm Kubota!")
```
