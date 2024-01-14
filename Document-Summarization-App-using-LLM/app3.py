import streamlit as st
import faiss
import numpy as np
import base64
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, pipeline


# Initialize Faiss index and storage
dimension = 768  # Change this dimension to match your language model's output dimension
num_clusters = 1000 # Adjust the number of clusters based on your requirements
num_sub_quantizers = 64 # Adjust the number of sub-quantizers for IndexIVFPQ
index = faiss.IndexIVFPQ(faiss.IndexFlatL2(dimension), num_clusters, num_sub_quantizers, faiss.METRIC_L2)
doc_ids = []  # List to store document IDs for retrieval
doc_vectors = []  # List to store document vectors

# Load tokenizer and model
checkpoint = "MBZUAI/LaMini-Flan-T5-248M"
tokenizer = T5Tokenizer.from_pretrained(checkpoint)
base_model = T5ForConditionalGeneration.from_pretrained(checkpoint, device_map='auto', torch_dtype=torch.float32)

# Function to vectorize text using your language model
def vectorize_text(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=512)
    with torch.no_grad():
        outputs = base_model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy().astype('float32')

# Function to display the PDF of a given file
def displayPDF(file):
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f''
    st.markdown(pdf_display, unsafe_allow_html=True)

# Document summarization pipeline using the language model
def llm_pipeline(input_text):
    pipe_sum = pipeline(
        'summarization',
        model=base_model,
        tokenizer=tokenizer,
        max_length=500,
        min_length=50
    )
    result = pipe_sum(input_text)
    result = result[0]['summary_text']
    return result

# Main Streamlit application
st.set_page_config(layout="wide")

def main():
        st.title("Document Summarization App")
        uploaded_file = st.file_uploader("Upload your PDF file", type=['pdf'])

        if uploaded_file is not None:
            if st.button("Summarize"):
                col1, col2 = st.columns(2)
                filepath = "data/" + uploaded_file.name
                
                with open(filepath, "wb") as temp_file:
                    temp_file.write(uploaded_file.read())
                with col1:
                   st.info("Uploaded File")
                   displayPDF(filepath)

                with col2:
                    with open(filepath, "rb") as f:
                        input_text = f.read().decode('utf-8','ignore')  # Read the content of the file
                    summary = llm_pipeline(input_text)
                    st.info("Summarization Complete")
                    st.success(summary)

if __name__ == "__main__":
        main()
