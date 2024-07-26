# GraphRAG + AutoGen + Ollama + Chainlit UI = Local Multi-Agent RAG Superbot  

![Graphical Abstract](https://github.com/karthik-codex/autogen_graphRAG/blob/main/images/1721017707759.jpg?raw=true)

This application integrates GraphRAG with AutoGen agents, powered by local LLMs from Ollama, for free and offline embedding and inference. Key highlights include:
 - **Agentic-RAG:** - Integrating GraphRAG's knowledge search method with an AutoGen agent via function calling.
 - **Offline LLM Support:** - Configuring GraphRAG (local & global search) to support local models from Ollama for inference
 and embedding.
 - **Non-OpenAI Function Calling:** - Extending AutoGen to support function calling with non-OpenAI LLMs from Ollama via Lite-LLM proxy
server.
 - **Interactive UI:** - Deploying Chainlit UI to handle continuous conversations, multi-threading, and user input settings.

![Main Interfacce](https://github.com/karthik-codex/autogen_graphRAG/blob/main/images/UI1.webp?raw=true)
![Widget Settings](https://github.com/karthik-codex/autogen_graphRAG/blob/main/images/U2.webp?raw=true)

## Useful Links 🔗

- **Full Guide:** Microsoft's GraphRAG + AutoGen + Ollama + Chainlit = Fully Local & Free Multi-Agent RAG Superbot [Medium.com](https://medium.com/@karthik.codex/microsofts-graphrag-autogen-ollama-chainlit-fully-local-free-multi-agent-rag-superbot-61ad3759f06f) 📚

## 📦 Installation and Setup Linux

Follow these steps to set up and run AutoGen GraphRAG Local with Ollama and Chainlit UI:

1. **Install LLMs:**

    Visit [Ollama's website](https://ollama.com/) for installation files.

    ```bash
    ollama pull mistral
    ollama pull nomic-embed-text
    ollama pull llama3
    ollama serve
    ```

2. **Create conda environment and install packages:**
    ```bash
   conda create -n RAG_agents python=3.12
   conda activate RAG_agents
   git clone https://github.com/karthik-codex/autogen_graphRAG.git
   cd autogen_graphRAG
   pip install -r requirements.txt
    ```    
3. **Initiate GraphRAG root folder:**
    ```bash
    mkdir -p ./input
    python -m graphrag.index --init  --root .
    mv ./utils/settings.yaml ./
    ```      
4. **Replace 'embedding.py' and 'openai_embeddings_llm.py' in the GraphRAG package folder using files from Utils folder:**
    ```bash
    sudo find / -name openai_embeddings_llm.py
    sudo find / -name embedding.py
    ```      
5. **Create embeddings and knowledge graph:**
    ```bash
    python -m graphrag.index --root .
    ```         
6. **Start Lite-LLM proxy server:**
    ```bash
    litellm --model ollama_chat/llama3
    ```    
7. **Run app:**
    ```bash
    chainlit run appUI.py
    ```                

## 📦 Installation and Setup Windows

Follow these steps to set up and run AutoGen GraphRAG Local with Ollama and Chainlit UI on Windows:

1. **Install LLMs:**

    Visit [Ollama's website](https://ollama.com/) for installation files.

    ```pwsh
    ollama pull mistral
    ollama pull nomic-embed-text
    ollama pull llama3
    ollama serve
    ```

2. **Create conda environment and install packages:**
    ```pwsh
    git clone https://github.com/karthik-codex/autogen_graphRAG.git
    cd autogen_graphRAG
    python -m venv venv
    ./venv/Scripts/activate
    pip install -r requirements.txt
    ```    
3. **Initiate GraphRAG root folder:**
    ```pwsh
    mkdir input
    python -m graphrag.index --init  --root .
    cp ./utils/settings.yaml ./
    ```      
4. **Replace 'embedding.py' and 'openai_embeddings_llm.py' in the GraphRAG package folder using files from Utils folder:**
    ```pwsh
    cp ./utils/openai_embeddings_llm.py .\venv\Lib\site-packages\graphrag\llm\openai\openai_embeddings_llm.py
    cp ./utils/embedding.py .\venv\Lib\site-packages\graphrag\query\llm\oai\embedding.py 
    ```      
5. **Create embeddings and knowledge graph:**
    ```pwsh
    python -m graphrag.index --root .
    ```         
6. **Start Lite-LLM proxy server:**
    ```pwsh
    litellm --model ollama_chat/llama3
    ```    
7. **Run app:**
    ```pwsh
    chainlit run appUI.py
    ```                
