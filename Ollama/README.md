- https://mer.vin/2024/03/ai-research-rag-using-chromadb-ollama/
- https://github.com/tyrell/llm-ollama-llamaindex-bootstrap/tree/main
- [Ollama-FastAPI-LlamaIndex](https://github.com/iSiddharth20/Ollama-FastAPI-LlamaIndex/tree/main)
- [Building a Local Full-Stack Application with Llama 3.1 and Aider: A Step-by-Step Guide](https://www.dataedgehub.com/2024/07/building-local-full-stack-application.html)
- [Running a RAG Chatbot with Ollama on Fly.io](https://upstash.com/blog/ollama-rag)
- [Reduce hallucinations with Bespoke-Minicheck](https://ollama.com/blog/reduce-hallucinations-with-bespoke-minicheck)
- [Bringing K/V Context Quantisation to Ollama](https://smcleod.net/2024/12/bringing-k/v-context-quantisation-to-ollama/)


<img width="929" alt="Screenshot 2024-10-26 at 6 27 31 AM" src="https://github.com/user-attachments/assets/85b58208-3c14-4ed8-bb63-3e42c1ccdae9">

```py
conda create -n agentic python=3.11 -y && conda activate agentic

pip install langchain-experimental

from langchain_experimental.llms.ollama_functions import OllamaFunctions

model = OllamaFunctions(model="llama3:8b", format="json")

model = model.bind_tools(
    tools=[
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, " "e.g. San Francisco, CA",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                    },
                },
                "required": ["location"],
            },
        }
    ],
    function_call={"name": "get_current_weather"},
)

from langchain_core.messages import HumanMessage

model.invoke("what is the weather in Boston?")
```
<img width="730" alt="Screenshot 2024-12-14 at 5 59 57 PM" src="https://github.com/user-attachments/assets/110e7ac5-9c76-4514-b57c-b6db9fc7cf54" />


Resources:
- [Ollama-docker](https://highreso.jp/edgehub/machinelearning/ollamapython.html)
- [kotaemon-Ollama](https://github.com/Cinnamon/kotaemon)
- [ollama-python-playground](https://github.com/pamelafox/ollama-python-playground)
