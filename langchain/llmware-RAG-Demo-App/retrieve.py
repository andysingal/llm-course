from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings

embeddings = SentenceTransformerEmbeddings(model_name="llmware/industry-bert-insurance-v0.1")

prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])

load_vector_store = Chroma(persist_directory="stores/insurance_cosine", embedding_function=embeddings)

#retriever = load_vector_store.as_retriever(search_kwargs={"k":3})

query = "What is Group life insurance?"

docs = load_vector_store.similarity_search_with_score(query=query, k=3)
for i in docs:
    doc, score = i
    print({"score": score, "content": doc.page_content, "metadata": doc.metadata})

