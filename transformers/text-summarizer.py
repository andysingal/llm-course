import streamlit as st
from transformers import pipeline
import tensorflow as tf

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def main():
    st.title("Text Summarizer App")

    
    input_text = st.text_area("Enter the text you want to summarize:")

    # Sidebar 
    min_length = st.sidebar.slider("Minimum Summary Length", 10, 200, 50)
    max_length = st.sidebar.slider("Maximum Summary Length", 50, 500, 100)

    if st.button("Generate Summary"):
        if input_text:
            # Generate summary
            summary = summarizer(input_text, max_length=max_length, min_length=min_length, do_sample=False)
            st.subheader("Generated Summary:")
            st.write(summary[0]["summary_text"])
        else:
            st.warning("Please enter some text to summarize.")

if __name__ == "__main__":
    main()
