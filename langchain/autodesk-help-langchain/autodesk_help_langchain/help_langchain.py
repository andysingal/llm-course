import bs4
import requests
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def find_autodesk_help_answer(question: str) -> str:
    llm = ChatOpenAI(model="gpt-3.5-turbo")

    # Process the question to get keywords for the search
    keywords_template = """What would be a good keyword search on the autodesk help website for the question: {question}
    Give me the words separated only by spaces and do not include Autodesk on the list.
    """
    keywords_prompt = ChatPromptTemplate.from_template(keywords_template)

    keywords_chain = (
        {"question": RunnablePassthrough()} | keywords_prompt | llm | StrOutputParser()
    )
    keywords = keywords_chain.invoke(question)
    print(f"Question: {question}\nKeywords: {keywords}")

    # Search the Autodesk Help API for the question and get the guids of the resulting topics
    api_base_url = "https://beehive.autodesk.com/community/service/rest/cloudhelp/resource/cloudhelpchannel/search/"
    params = dict(
        origin="upi",
        p="RVT",
        v="2025",
        l="ENU",
        maxresults=3,
        knowledgeSource="Product Documentation",
        q=keywords,
        source="all",
    )

    resp = requests.get(url=api_base_url, params=params)
    data = resp.json()
    urls = [item.get("url") for item in data.get("entries").get("item")]
    if not urls:
        return "No results found on the Autodesk Help Website."

    # Load the corresponding documents from the Autodesk Help website
    loader = WebBaseLoader(
        web_paths=urls,
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(),
        ),
    )
    docs = loader.load()

    # Split the documents into chunks and embed them
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

    # Define the RAG prompt template
    rag_template = """Use the following pieces of context to answer the question at the end. The question can be in any language and in that case you have to translate the question to english before using the context text. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Use three sentences maximum and keep the answer as concise as possible. If the question was originaly in portuguese, please answer it in portuguese.
    Always say "thanks for asking!" at the end of the answer.

    {context}

    Question: {question}

    Helpful Answer:
        """
    rag_prompt = PromptTemplate.from_template(rag_template)

    # Define a function to format the context documents
    def format_docs(docs_to_format):
        return "\n\n".join(doc.page_content for doc in docs_to_format)

    # Define the langchain pipeline
    retriever = vectorstore.as_retriever()

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    # Run the pipeline
    result = rag_chain.invoke(question)

    # Clean up
    vectorstore.delete_collection()

    return result


if __name__ == "__main__":
    load_dotenv()

    question = input("Question? ")  # How do I change view range?
    print(find_autodesk_help_answer(question))
