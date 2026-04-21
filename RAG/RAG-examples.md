[RAG-neon](https://neon.tech/blog/building-a-rag-application-with-llama-3-1-and-pgvector)

[Basic-Rag](https://github.com/gurezende/Basic-Rag)



[DeskRAG](https://levelup.gitconnected.com/deskrag-create-an-offline-ai-assistant-in-one-afternoon-b2ae6242b762)


[Agent.md](https://github.com/openai/agents.md)

Think of AGENTS.md as a README for agents: a dedicated, predictable place to provide context and instructions to help AI coding agents work on your project.

```
import os
import numpy as np
import faiss
import gradio as gr

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# PDF Loader
def load_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + " "
    return text


#Chunking
def chunk_text(text, chunk_size=800, overlap=200):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


# Embedding Model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def create_vector_store(chunks):
    embeddings = embedding_model.encode(chunks)
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    return index


# Retrieval
def retrieve(query, chunks, index, k=3):
    query_embedding = embedding_model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)
    return [chunks[i] for i in indices[0]]


# Groq Client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

#prompt
def ask_llm(context, question):
    prompt = f"""
You are a strict academic assistant.
Answer ONLY using the provided context.
If the answer is not explicitly stated in the context,
respond exactly with:
This PDF does not contain this information.
Do not use outside knowledge.
Context:
{context}
Question:
{question}
Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant", #model type
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()



# Gradio App
with gr.Blocks() as demo:

    gr.Markdown("## 📄 Welcome to DOCY AI ")
    gr.Markdown("### Upload your PDF and ask questions about it.")

    pdf_file = gr.File(file_types=[".pdf"], label="Upload PDF")

    status = gr.Markdown("")  # PDF index status message

    question = gr.Textbox(label="Ask a question", lines=3)
    answer = gr.Textbox(label="Answer", lines=8)

    run_btn = gr.Button("▶️ Run")
    stop_btn = gr.Button("⛔ Stop Thinking")
    clear_btn = gr.Button("🆕 New Question")

    state = gr.State()

    # ---------------- PDF Processing ----------------
    def process_pdf(file):
        text = load_pdf(file.name)
        chunks = chunk_text(text)
        index = create_vector_store(chunks)
        return (chunks, index), "✅ PDF indexed successfully! You can now ask questions."

    pdf_file.upload(
        process_pdf,
        inputs=pdf_file,
        outputs=[state, status]
    )

    # ---------------- Question Logic ----------------
    def ask_question(question, state):
        if state is None:
            return "Please upload a PDF first."

        chunks, index = state
        retrieved_chunks = retrieve(question, chunks, index)

        if retrieved_chunks is None:
            return "This PDF does not contain this information."

        context = "\n\n".join(retrieved_chunks)
        return ask_llm(context, question)

    run_event = run_btn.click(
        ask_question,
        inputs=[question, state],
        outputs=answer
    )

    # ---------------- Stop Button ----------------
    stop_btn.click(
        None,
        None,
        None,
        cancels=[run_event]
    )

    # ---------------- Clear Button ----------------
    def clear_all():
        return "", ""

    clear_btn.click(
        clear_all,
        outputs=[question, answer]
    )

demo.launch()

```
