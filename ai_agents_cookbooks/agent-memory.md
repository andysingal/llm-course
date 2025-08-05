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

Pre-requisites
Install Ollama on your local machine from the official website. And then pull the Deepseek model:
```
ollama pull deepseek-r1:8b
```
Install the dependencies using pip:
```
pip install -r requirements.txt
```
Run
Run the Streamlit app:
```
streamlit run agent_with_memory.py
```
Bonus tip
If you want to change the short-term memory with the long-term memory, you can change the MemorySaver with InMemoryStore:
```
from langgraph.store.memory import InMemoryStore

store = InMemoryStore()

# Example usage - Learn more about it by checking the LangGraph documentation
# store.put()
# store.get()
```
