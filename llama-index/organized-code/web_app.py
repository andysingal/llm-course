"""
    This web app is created using streamlit
    Created to demonstrate the working of Llama2-7B-hf-chat model
    for RAG (Retreival Augmented Generation) purposes 
"""
import streamlit as st
import random
import time
import os
from rag_model import Llama2_7B_Chat, reset_model


@st.cache_resource
def load_llm():
    return Llama2_7B_Chat()


def save_chat_to_history(chat_data: dict) -> None:
    """Saves the chat data to streamlit session state"""

    st.session_state.messages.append(chat_data)


def get_llm_reply(model: Llama2_7B_Chat, mode: str = "default", user_prompt: str = None) -> None:
    """get response from the LLM"""

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        if mode == "reply":
            llm_response, _ = model.ask_llm(
                user_prompt, st.session_state.query_engine)   # reply and source nodes
        elif mode == "greet":
            llm_response = random.choice(
                [
                    "Hello there! How can I assist you today?",
                    "Hi, user! Is there anything I can help you with?",
                    "Do you need help?",
                ]
            )
        else:
            llm_response = "No files uploaded! Please upload a file :)"

    full_response = ""

    try:
        llm_response = str(llm_response).split('\n')

        for response in llm_response:
            for chunk in response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            full_response += "  \n"
                
        message_placeholder.markdown(full_response)

    except AttributeError as e:
        message_placeholder.markdown("No answer! Error!")

    # Add assistant response to chat history
    save_chat_to_history({"role": "assistant", "content": full_response})


def show_history() -> None:
    """Display chat messages from streamlit chat history"""

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def clear_chat() -> None:
    st.session_state.messages.clear()


def upload_data(_model: Llama2_7B_Chat) -> None:
    """Upload the data given by the user to a directory"""

    st.session_state.files_uploaded = True

    upload_time = str(int(time.time()))
    folder_name = "Data_" + upload_time
    bar = st.progress(0, text="Uploading files...")

    if not os.path.exists(folder_name):
        os.system(f"mkdir {folder_name}")

        # Write the file to Data directory
        for file in uploaded_files:
            with open(os.path.join(folder_name, file.name), 'wb') as bytes_file:
                bytes_file.write(file.getbuffer())

        # initialize model, create vector_index and start query_engine
        bar.progress(25, text="Creating indices...")
        _model.create_index(folder_name)

        bar.progress(50, text="Staring engine...")
        st.session_state.query_engine = _model.start_query_engine()

        bar.progress(75, text="Staring engine...")
        st.session_state.messages.clear()

        bar.progress(100, "Files uploaded!!")
        time.sleep(0.03)
        bar.empty()


# Main code
if __name__ == "__main__":
    # Site title
    st.title(":blue[Llama2-TalkBot]")

    status = st.text("Initializing Llama2-7B model....")
    model = load_llm()
    status.text("Done!!")
    time.sleep(0.05)
    status.empty()

    # Sidebar to upload files
    with st.sidebar:
        uploaded_files = st.file_uploader(
            ":green[Upload files]", type='pdf', accept_multiple_files=True)

        col1, col2 = st.columns(2, gap="small")
        submit_files = col1.button('Submit', use_container_width=True)
        clear_chat_btn = col2.button(
            'Clear Chat', on_click=clear_chat, use_container_width=True)

        if uploaded_files and submit_files:
            upload_data(model)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        get_llm_reply(model, mode="greet")

    # Accept user input
    if prompt := st.chat_input("Enter query"):
        show_history()
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add user message to chat history
        save_chat_to_history({"role": "user", "content": prompt})

        if "files_uploaded" in st.session_state:
            get_llm_reply(model, mode="reply", user_prompt=prompt)
        else:
            get_llm_reply(model)
