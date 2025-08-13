[ACPWalkthrough](https://github.com/nicknochnack/ACPWalkthrough/blob/main/6.%20ACPCallingAgent.py)

- Install Ollama on your local machine from the official website. And then pull the gpt-oss model:
```
ollama pull gpt-oss:20b
```
Install the dependencies using pip:
```
pip install -r requirements.txt
```
And also create an account on Tavily and get your API key. Set it as an environment variable:
```
export TAVILY_API_KEY=your_api_key_here
```

Run the Streamlit app:
```
streamlit run gpt_oss_agent_with_mcp.py
```

```py
import asyncio
import os

import streamlit as st
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

tavily_api_key = os.getenv("TAVILY_API_KEY")
model = ChatOllama(model="gpt-oss:20b")

async def answer_question_async(query):
    async with streamablehttp_client(f"https://mcp.tavily.com/mcp/?tavilyApiKey={tavily_api_key}") as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(model, tools)
            response = await agent.ainvoke({
                "messages": [
                    {"role": "user", "content": query}
                ]
            })

            for message in response["messages"]:
                print(message.pretty_print())
                print()

            return response["messages"][-1].content

def answer_question(query):
    return asyncio.run(answer_question_async(query))

st.title("Local ChatGPT")
query = st.text_input("Enter your query:")

if query:
    answer = answer_question(query)
    st.markdown(answer)

```
