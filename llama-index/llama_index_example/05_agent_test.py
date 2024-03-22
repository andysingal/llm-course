# -- coding:utf-8 --
import json
from typing import Sequence, List

from llama_index.core.llms import ChatMessage
from llama_index.core.tools import BaseTool, FunctionTool

import nest_asyncio
from llama_index.llms.ollama import Ollama

nest_asyncio.apply()

def multiply(a: int, b: int) -> int:
    """Multiple two integers and returns the result integer"""
    return a * b


multiply_tool = FunctionTool.from_defaults(fn=multiply)

def add(a: int, b: int) -> int:
    """Add two integers and returns the result integer"""
    return a + b


add_tool = FunctionTool.from_defaults(fn=add)

class YourOpenAIAgent:
    def __init__(
        self,
        tools: Sequence[BaseTool] = [],
        chat_history: List[ChatMessage] = [],
    ) -> None:
        self._llm = Ollama(model="qwen:7b-chat")
        self._llm.base_url = "http://1.92.64.112:11434"
        self._tools = {tool.metadata.name: tool for tool in tools}
        self._chat_history = chat_history

    def reset(self) -> None:
        self._chat_history = []

    def chat(self, message: str) -> str:
        chat_history = self._chat_history
        chat_history.append(ChatMessage(role="user", content=message))
        tools = [
            tool.metadata.to_openai_tool() for _, tool in self._tools.items()
        ]

        ai_message = self._llm.chat(chat_history, tools=tools).message
        additional_kwargs = ai_message.additional_kwargs
        chat_history.append(ai_message)

        tool_calls = ai_message.additional_kwargs.get("tool_calls", None)
        # parallel function calling is now supported
        if tool_calls is not None:
            for tool_call in tool_calls:
                function_message = self._call_function(tool_call)
                chat_history.append(function_message)
                ai_message = self._llm.chat(chat_history).message
                chat_history.append(ai_message)

        return ai_message.content

    def _call_function(self, tool_call: dict) -> ChatMessage:
        id_ = tool_call["id"]
        function_call = tool_call["function"]
        tool = self._tools[function_call["name"]]
        output = tool(**json.loads(function_call["arguments"]))
        return ChatMessage(
            name=function_call["name"],
            content=str(output),
            role="tool",
            additional_kwargs={
                "tool_call_id": id_,
                "name": function_call["name"],
            },
        )

agent = YourOpenAIAgent(tools=[multiply_tool, add_tool])

print(agent.chat("What is 2123 * 215123"))