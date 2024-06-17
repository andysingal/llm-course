from datetime import datetime
from typing import Any, Dict

from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI

from support_agent.state import AssistantGraphState
from support_agent.tools.safe_tools import safe_tools

# model_with_tools = ChatMistralAI(model="mistral-large-latest").bind_tools(safe_tools)
model_with_tools = ChatOpenAI().bind_tools(safe_tools)
primary_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful customer support assistant. " "\nCurrent time: {time}.",
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now(), tool_names=[tool.name for tool in safe_tools])


def assistant_with_tools(state: AssistantGraphState) -> Dict[str, Any]:
    chain = primary_assistant_prompt | model_with_tools
    res = chain.invoke(input=state)
    return {"messages": [res]}
