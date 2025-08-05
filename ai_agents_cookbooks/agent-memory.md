```py
import re

import streamlit as st
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent


def clean_text(text: str):
    cleaned_text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return cleaned_text.strip()

st.title("Agent with Memory")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

if "memory" not in st.session_state:
    memory = MemorySaver()
    st.session_state.memory = memory

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

model = ChatOllama(model="deepseek-r1:8b")
chat_agent = create_react_agent(
    model=model,
    tools=[],
    name="chat_agent",
    checkpointer=st.session_state.memory
)

question = st.chat_input()

if question:
    st.session_state["messages"].append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    result = chat_agent.invoke(
        {
            "messages":  [
                {
                    "role": "user",
                    "content": question
                }
            ]
        },
        config={"configurable": {"thread_id": "1"}}
    )

    response = clean_text(result["messages"][-1].content)

    st.session_state["messages"].append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
```
