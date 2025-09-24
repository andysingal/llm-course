[LangGraph_1o1_Agentic_Customer_Support](https://github.com/Farzad-R/Advanced-QA-and-RAG-Series/tree/main/LangGraph_1o1_Agentic_Customer_Support)

[Plan-Execute-LangGraph](https://wikidocs.net/270688)

[Boost Customer Support](https://dev.to/kaymen99/boost-customer-support-ai-agents-langgraph-and-rag-for-email-automation-21hj)

[NewsAgent](https://www.kaggle.com/code/suvroo/newsagent)

[langgraph-rarallel-execution](https://github.com/SauravP97/agentic-workflows/tree/main/parallel-execution)

[video-1](https://www.youtube.com/watch?v=mMzAbhnOgXQ)

[langgraph-supervisorで作成したSupervisor型マルチエージェントをA2A Protocolを用いて再実装](https://zenn.dev/5enxia/articles/44df8d244b323a)

```py
export OPENAI_API_KEY="your_openai_api_key"
export GOOGLE_GENAI_API_KEY="your_google_genai_api_key"

uv add langchain langchain-google-genai langchain-openai langgraph langgraph-supervisor a2a-sdk[http-server]

# langgraph-only/__main__.py
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain.chat_models import init_chat_model

model = init_chat_model(model='gpt-4.1-nano')
memory = MemorySaver()

@tool
def get_exchange_rate():
    """Get the exchange rate between USD and JPY."""
    return "1 USD = 147 JPY"

currency_agent = create_react_agent(
    model=model,
    tools=[get_exchange_rate],
    checkpointer=memory,
    name="currency_agent",
    prompt=(
        'You answer questions about currency exchange rates. '
        'Use the tool to get the exchange rate between USD and JPY.'
    )
)

@tool
def get_weather(location: str) -> str:
    """Get the current weather."""
    return f"{location} is Sunny"

weather_agent = create_react_agent(
    model=model,
    tools=[get_weather],
    checkpointer=memory,
    name="weather_agent",
    prompt=(
        "You answer questions about the weather in a given location."
        "Use the tool to get the current weather."
    )
)

workflow = create_supervisor(
    model=model,
    agents=[
        currency_agent,
        weather_agent,
    ],
    checkpointer=memory,
    prompt=(
        "You are a supervisor managing two agents:"
        "Assign work to one agent at a time, do not call agents in parallel."
        "Do not do any work yourself."
    )
)

app = workflow.compile()
content = "How many yen is 1 USD?"  # Translated from "1ドルは何円ですか？"
# content = "What's the weather in Tokyo?"  # Translated from "東京の天気は？"

result = app.invoke({"messages": [HumanMessage(content=content)]})
for message in result["messages"]:
    print(message)

```
uv run langgraph-only



## Article

[LangGraph + SciPy: Building an AI That Reads Documentation and Makes Decisions](https://towardsdatascience.com/langgraph-scipy-building-an-ai-that-reads-documentation-and-makes-decisions/)
