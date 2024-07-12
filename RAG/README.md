
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



New Resources
[RAG using LLMSmith and FastAPI](https://dev.to/dheerajgopi/rag-using-llmsmith-and-fastapi-1e6i) 
[Exploring RAG Applications Across Languages: Conversing with the Mishnah](https://towardsdatascience.com/exploring-rag-applications-across-languages-conversing-with-the-mishnah-16615c30f780) 


  
