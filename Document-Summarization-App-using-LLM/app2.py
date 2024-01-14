import streamlit as st
import faiss
import torch
import numpy as np
import base64
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from transformers import T5Tokenizer, T5ForConditionalGeneration, pipeline

# Initialize Faiss index and storagestreamlit 
dimension = 768 # Change this dimension to match your language model's output dimension
index = faiss.IndexFlatL2(dimension) # You can choose a different index type if needed
doc_vectors = [] # List to store document vectors

# Load tokenizer and model
checkpoint = "MBZUAI/LaMini-Flan-T5-248M"
tokenizer = T5Tokenizer.from_pretrained(checkpoint)
base_model = T5ForConditionalGeneration.from_pretrained(checkpoint, device_map='auto', torch_dtype=torch.float32)

# Modify the following function to vectorize text using your language model
def vectorize_text(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=512)
    with torch.no_grad():
        outputs = base_model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy().astype('float32')

# Modify the file_preprocessing function to store vectors in the vector database
def file_preprocessing_and_vectorization(file):
    loader = PyPDFLoader(file)
    pages = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    texts = text_splitter.split_documents(pages)

    for text in texts:
        vector = vectorize_text(text.page_content)
        doc_vectors.append(vector)
        index.add(np.array([vector], dtype='float32')) # Add vector to the index

    return texts

# Streamlit code
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
                pdf_view = displayPDF(filepath)
            with col2:
                texts = file_preprocessing_and_vectorization(filepath)
                input_text = texts[0].page_content
                summary = llm_pipeline(input_text)
                st.info("Summarization Complete")
                st.success(summary)


if __name__ == "__main__":
    main()