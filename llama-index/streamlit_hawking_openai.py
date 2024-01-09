
'''
Overview:

    In this GenAI Streamlit app we leverage OpenAI*, LlamaIndex, and a text
    file containing a history of Stephen Hawking to ask questions about one of
    the world's greatest astrophysicists.

    *Note: An OpenAI API key must reside in .env, but API usage is regulated 

    Date: 1/05/2024

'''

from dotenv import load_dotenv
from llama_index.llms import OpenAI
from llama_index import VectorStoreIndex, SimpleDirectoryReader
import os
import streamlit as st
import datetime
import json

load_dotenv()
open_api_key = os.getenv("OPENAI_API_KEY")

# Streamlit app layout
st.title("Stephen Hawking Q&A :telescope:")
intro = '''**Examples:**  
           :pill: :orange[What illness did Stephen Hawking develop?]  
           :baby: :green[What was Stephen Hawking's early life like?]  
           :boom: :blue[What kind of work helped Stephen Hawking prove the idea of the 'Big Bang'?]
        '''
st.markdown(intro)
user_input = st.text_input("Ask a question about Stephen Hawking:")

# LlamaIndex integrated RAG 
# text file resides in /hawking_data/
documents = SimpleDirectoryReader("hawking_data").load_data() 
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

# Load or initialize API usage data
def load_usage_data():
    try:
        with open("usage_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"date": str(datetime.date.today()), "usage": 0}

# Save usage data
def save_usage_data(usage_data):
    with open("usage_data.json", "w") as file:
        json.dump(usage_data, file)

# Check and update API usage
def check_and_update_usage():
    usage_data = load_usage_data()
    usage_limit = 100

    # If it's a new day, reset the usage counter
    if usage_data["date"] != str(datetime.date.today()):
        usage_data["date"] = str(datetime.date.today())
        usage_data["usage"] = 0

    # Check if usage exceeds the limit
    if usage_data["usage"] >= usage_limit:
        st.write("API limit exceeded. Try again tomorrow.")
        return False

    # Increment usage counter
    usage_data["usage"] += 1
    save_usage_data(usage_data)
    return True

# Check usage and provide output
if check_and_update_usage():
    # Check for input and produce output
    if user_input:
        response = query_engine.query(user_input)
        response_string = str(response)
        # Display the output
        st.write(response_string)
