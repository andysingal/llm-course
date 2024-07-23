- https://mer.vin/2024/03/ai-research-rag-using-chromadb-ollama/
- https://github.com/tyrell/llm-ollama-llamaindex-bootstrap/tree/main
- [Ollama-FastAPI-LlamaIndex](https://github.com/iSiddharth20/Ollama-FastAPI-LlamaIndex/tree/main)

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
