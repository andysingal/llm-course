# Document-Summarization
Document Summarization App using large language model (LLM) and Langchain framework. Used a pre-trained T5 model and its tokenizer from Hugging Face Transformers library. 
Created a summarization pipeline to generate summary using model.

1. Import Statements:
   - It begins by importing necessary libraries like Streamlit, Langchain, Transformers, and other Python libraries.

2. Model and Tokenizer Loading:
   - The code loads a pre-trained T5 model (a Transformer-based model) and its associated tokenizer from the Hugging Face Transformers library.
     This model is used for text summarization.

3. File Loader and Preprocessing:
   - The `file_preprocessing` function loads a PDF file using the Langchain library and splits it into smaller text chunks. These text chunks are later used for
     summarization.

4. LLM Pipeline:
   - The `llm_pipeline` function sets up a summarization pipeline using the pre-trained T5 model and tokenizer. It takes the preprocessed text as input and generates
     a summary using the model.

5. Streamlit Setup:
   - The Streamlit app is set up with a title and an option to upload a PDF file.

6. Main Function:
   - The `main` function is the entry point of the app.
   - It provides a file upload button and a "Summarize" button.
   - When a PDF file is uploaded and the "Summarize" button is clicked, it displays the uploaded PDF on the left side and the generated summary on the right side
     of the Streamlit app.

7. HTML Display of PDF:
   - The `displayPDF` function converts the uploaded PDF file into base64 format and embeds it in an HTML iframe, allowing the PDF to be displayed in the app.

8. Streamlit Configuration:
   - The app's layout is configured to be "wide" using `st.set_page_config`.

9. Running the App:
   - The app is launched when the script is run as the main module (`if __name__ == "__main__": main()`).

The main functionality of this app is to upload a PDF document, process it, and then display both the PDF and a summarized version of the document.
It utilizes a pre-trained language model for text summarization and Streamlit for creating a user-friendly interface. Users can upload PDFs and quickly obtain 
summarized content from them.
