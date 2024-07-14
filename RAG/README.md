
<img width="1214" alt="Screenshot 2023-12-16 at 6 40 36 PM" src="https://github.com/andysingal/modern_nlp_2/assets/20493493/45c66a20-1bf2-4faf-a5f7-359fc7da9847">



References :
1. Haystack with LLM: https://github.com/anakin87
2. https://www.atyun.com/58579.html 

```
from typing import List, Optional, Union
import time
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from retriever import (
    create_parent_retriever,
    load_embedding_model,
    load_pdf,
    load_reranker_model,
    retrieve_context,
)


def main(
    file: str = "example_data/2401.08406.pdf",
    llm_name="mistral",
):
    docs = load_pdf(files=file)

    embedding_model = load_embedding_model()
    retriever = create_parent_retriever(docs, embedding_model)
    reranker_model = load_reranker_model()

    llm = ChatOllama(model=llm_name)
    prompt_template = ChatPromptTemplate.from_template(
        (
            "Please answer the following question based on the provided `context` that follows the question.\n"
            "If you do not know the answer then just say 'I do not know'\n"
            "question: {question}\n"
            "context: ```{context}```\n"
        )
    )
    chain = prompt_template | llm | StrOutputParser()

    while True:
        query = input("Ask question: ")
        context = retrieve_context(
            query, retriever=retriever, reranker_model=reranker_model
        )[0]
        # print("context:\n", context, "\n", "=" * 50, "\n")
        print("LLM Response: ", end="")
        for e in chain.stream({"context": context[0].page_content, "question": query}):
            print(e, end="")
        print()
        time.sleep(0.1)


if __name__ == "__main__":
    from jsonargparse import CLI

    CLI(main)
```
[Source](https://lightning.ai/lightning-ai/studios/document-chat-assistant-using-rag)


```py
import gradio as gr
from huggingface_hub import InferenceClient
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from rank_bm25 import BM25Okapi
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import fitz  # PyMuPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

client = InferenceClient("HuggingFaceH4/zephyr-7b-beta")

class MyApp:
    def __init__(self) -> None:
        self.documents = []
        self.embeddings = None
        self.index = None
        self.bm25 = None
        self.rerank_model = AutoModelForSequenceClassification.from_pretrained("cross-encoder/ms-marco-MiniLM-L-6-v2")
        self.rerank_tokenizer = AutoTokenizer.from_pretrained("cross-encoder/ms-marco-MiniLM-L-6-v2")
        self.tfidf_vectorizer = TfidfVectorizer()

    def load_pdf(self, file_path: str) -> None:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        chunks = self.split_into_chunks(text, chunk_size=300, overlap=100)
        for i, chunk in enumerate(chunks):
            self.documents.append({
                "chunk_id": i,
                "content": chunk,
                "metadata": {
                    "source": file_path,
                    "chunk": i
                }
            })
        print("PDF content processed successfully!")

    def split_into_chunks(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        sentences = text.split('.')
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence = sentence.strip() + '.'
            sentence_length = len(sentence.split())
            
            if current_length + sentence_length <= chunk_size:
                current_chunk.append(sentence)
                current_length += sentence_length
            else:
                chunks.append(' '.join(current_chunk))
                current_chunk = current_chunk[-overlap:] + [sentence]
                current_length = sum(len(s.split()) for s in current_chunk)
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks

    def build_vector_db(self) -> None:
        model = SentenceTransformer('all-mpnet-base-v2')
        self.embeddings = model.encode([doc["content"] for doc in self.documents])
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(np.array(self.embeddings))
        
        tokenized_docs = [doc["content"].split() for doc in self.documents]
        self.bm25 = BM25Okapi(tokenized_docs)
        
        self.tfidf_vectorizer.fit([doc["content"] for doc in self.documents])
        
        print("Vector database, BM25 index, and TF-IDF vectorizer built successfully!")

    def search_documents(self, query: str, k: int = 10) -> List[str]:
        model = SentenceTransformer('all-mpnet-base-v2')
        query_embedding = model.encode([query])
        
        D, I = self.index.search(np.array(query_embedding), k)
        semantic_results = [self.documents[i]["content"] for i in I[0]]
        
        tokenized_query = query.split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        top_bm25 = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)[:k]
        lexical_results = [self.documents[i]["content"] for i in top_bm25]
        
        tfidf_query = self.tfidf_vectorizer.transform([query])
        tfidf_docs = self.tfidf_vectorizer.transform([doc["content"] for doc in self.documents])
        tfidf_similarities = cosine_similarity(tfidf_query, tfidf_docs)[0]
        top_tfidf = sorted(range(len(tfidf_similarities)), key=lambda i: tfidf_similarities[i], reverse=True)[:k]
        tfidf_results = [self.documents[i]["content"] for i in top_tfidf]
        
        combined_results = list(set(semantic_results + lexical_results + tfidf_results))
        return combined_results[:k] if combined_results else ["No relevant documents found."]

    def rerank_results(self, query: str, results: List[str], top_k: int = 5) -> List[str]:
        pairs = [[query, doc] for doc in results]
        inputs = self.rerank_tokenizer(pairs, padding=True, truncation=True, return_tensors="pt", max_length=512)
        with torch.no_grad():
            scores = self.rerank_model(**inputs).logits.squeeze(-1)
        ranked_results = [x for _, x in sorted(zip(scores, results), key=lambda pair: pair[0], reverse=True)]
        return ranked_results[:top_k]

    def compress_prompt(self, context: str, max_tokens: int = 2000) -> str:
        tokens = self.rerank_tokenizer.tokenize(context)
        if len(tokens) > max_tokens:
            sentences = context.split('.')
            compressed_sentences = []
            current_length = 0
            for sentence in sentences:
                sentence_tokens = self.rerank_tokenizer.tokenize(sentence)
                if current_length + len(sentence_tokens) <= max_tokens:
                    compressed_sentences.append(sentence)
                    current_length += len(sentence_tokens)
                else:
                    break
            context = '.'.join(compressed_sentences)
        return context

app = MyApp()
app.load_pdf("YOURPDFFILE.pdf")  
app.build_vector_db()

def respond(
    message: str,
    history: List[Tuple[str, str]],
    system_message: str = "You are a knowledgeable Cybersecurity Threat Intelligence Advisor. Provide accurate and up-to-date information on cyber threats, vulnerabilities, and mitigation strategies. Use the provided knowledge base to offer relevant advice on cybersecurity issues. Always prioritize current best practices and verified threat intelligence in your responses.",
    max_tokens: int = 500,
    temperature: float = 0.3,
    top_p: float = 0.9,
):
    try:
        messages = [{"role": "system", "content": system_message}]

        for val in history:
            if val[0]:
                messages.append({"role": "user", "content": val[0]})
            if val[1]:
                messages.append({"role": "assistant", "content": val[1]})

        retrieved_docs = app.search_documents(message, k=10)
        print(f"Retrieved docs: {retrieved_docs}")
        
        reranked_docs = app.rerank_results(message, retrieved_docs, top_k=5)
        print(f"Reranked docs: {reranked_docs}")
        
        context = "\n\n".join(reranked_docs)
        
        compressed_context = app.compress_prompt(context, max_tokens=2000)
        print(f"Compressed context: {compressed_context}")
        
        messages.append({"role": "user", "content": message})
        messages.append({"role": "system", "content": "Use the following information to answer the user's question: " + compressed_context})

        response = ""
        for message in client.chat_completion(
            messages,
            max_tokens=max_tokens,
            stream=True,
            temperature=temperature,
            top_p=top_p,
        ):
            token = message.choices[0].delta.content
            response += token
            yield response
    except Exception as e:
        yield f"An error occurred: {str(e)}"

demo = gr.Blocks()

with demo:
    gr.Markdown("🛡️ **Cybersecurity Threat Intelligence Advisor**")
    gr.Markdown(
        "‼️Disclaimer: This chatbot is based on a cybersecurity knowledge base that is publicly available. "
        "We are not responsible for any actions taken based on the advice provided. Use this information at your own risk.‼️"
    )
    
    chatbot = gr.ChatInterface(
        respond,
        examples=[
            ["What are the most common types of cyber attacks?"],
            ["How can I protect my organization from ransomware?"],
            ["What is phishing and how can it be prevented?"],
            ["Can you explain the concept of zero trust security?"],
            ["What are some best practices for incident response?"]
        ],
        title='Cybersecurity Threat Intelligence Advisor 🛡️'
    )

if __name__ == "__main__":
    demo.launch()
```

<img width="877" alt="Screenshot 2024-02-20 at 10 22 14 AM" src="https://github.com/andysingal/llm-course/assets/20493493/4f722453-a82f-4bea-ab52-78c416740284">


Resources:
- [How to Build a Chatbot Using the OpenAI API & Pinecone](https://www.datacamp.com/tutorial/how-to-build-chatbots-using-openai-api-and-pinecone)
- [Retrieval Augmented Generation (RAG): Demystified](https://cheatsheet.md/ja/prompt-engineering/rag-llm)
- [RAG techniques: Cleaning user questions with an LLM](https://techcommunity.microsoft.com/t5/educator-developer-blog/rag-techniques-cleaning-user-questions-with-an-llm/ba-p/4075340)
- [How to build RAG Applications that Reduce Hallucinations](https://community.aws/content/2ddbSgLL6Ey1et3Cq2k2m6C2SvW/how-to-build-rag-applications-that-reduce-hallucinations)
- https://github.com/anthropics/anthropic-cookbook/blob/main/third_party/LlamaIndex/Multi_Document_Agents.ipynb
- [Advanced RAG with TATR](https://walkingtree.tech/advanced-rag-multi-modal-techniques-for-accurate-data-extraction/)
- [txtai-RAG](https://dev.to/neuml/advanced-rag-with-guided-generation-38ca)
- [Building LLM Applications: Advanced RAG](https://medium.com/@vipra_singh/building-llm-applications-advanced-rag-part-10-ec0fe735aeb1)

Notebooks
- [Milvus-notebooks](https://github.com/milvus-io/bootcamp/blob/master/bootcamp/RAG/multi_doc_qa_llamaindex.ipynb)
- [RAG-W/-Phi-3-mini](https://www.kaggle.com/code/ahmedeldokmak/rag-w-phi-3-mini)
- [LLM Fine-Tuning Workshop: Improve Question-Answering Skills](https://dev.to/admantium/llm-fine-tuning-workshop-improve-question-answering-skills-1h18)
- [RAG on structured data with PostgreSQL](https://techcommunity.microsoft.com/t5/microsoft-developer-community/rag-on-structured-data-with-postgresql/ba-p/4164456)
- [https://www.analyticsvidhya.com/blog/2024/06/llm-observability-and-evaluations/](https://www.analyticsvidhya.com/blog/2024/06/llm-observability-and-evaluations/)
- [RAG in 85 lines of code](https://docs.zenml.io/user-guide/llmops-guide/rag-with-zenml/rag-85-loc)
- [Unlocking RAG’s Potential: Mastering Advanced Techniques](https://procogia.com/unlocking-rags-potential-mastering-advanced-techniques-part-1/)
- [Fine-Tune Embeddings from HuggingFace for RAG](https://huggingface.co/blog/lucifertrj/finetune-embeddings) - Beyond LLM
- [Vector Search & RAG Landscape: A review with txtai](https://medium.com/neuml/vector-search-rag-landscape-a-review-with-txtai-a7f37ad0e187)
- [LLM + RAG Projects on Finance Domain](https://github.com/simranjeet97/LLM-RAG_Finance_UseCases/blob/main/LLM_%2B_RAG_for_Finance.ipynb)
- [Databricks-RAG](https://learn.microsoft.com/en-us/azure/databricks/_extras/notebooks/source/machine-learning/structured-data-for-rag.html)
- [Transformers-RAG](https://huggingface.co/spaces/Tusharvw/ragllm/blob/main/app.py)



New Resources
[RAG using LLMSmith and FastAPI](https://dev.to/dheerajgopi/rag-using-llmsmith-and-fastapi-1e6i) 
[Exploring RAG Applications Across Languages: Conversing with the Mishnah](https://towardsdatascience.com/exploring-rag-applications-across-languages-conversing-with-the-mishnah-16615c30f780) 


  
