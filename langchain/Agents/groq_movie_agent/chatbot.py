import streamlit as st
from agent import Chatbot
from langchain_community.chat_message_histories import ChatMessageHistory

st.title("Movie Information Agent")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "memory" not in st.session_state:
    st.session_state.memory = ChatMessageHistory(session_id="test-session")

##Initialize the Agents:
movie_agent = Chatbot(model='llama3-8b-8192', temperature=0.3, memory=st.session_state.memory)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Type your question here."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    ## Get response
    response = movie_agent.run(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
