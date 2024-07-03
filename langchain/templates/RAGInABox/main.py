import subprocess

import os
from config import LANGCHAIN_API_KEY, TAVILY_API_KEY
from langchain_community.embeddings import GPT4AllEmbeddings

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from langchain_community.tools.tavily_search import TavilySearchResults

from typing_extensions import TypedDict
from typing import List
from langchain_core.documents import Document

from langgraph.graph import END, StateGraph


### Install dependencies
# Run this function the first time this script is run on your machine
def install_dependencies():
    packages = [
        "langchain-nomic",
        "langchain_community",
        "tiktoken",
        "langchainhub",
        "chromadb",
        "langchain",
        "langgraph",
        "tavily-python",
        "gpt4all",
        "langchain-text-splitters"
    ]

    for package in packages:
        subprocess.run(['pip', 'install', '-U', package])

# This code to initialize the vectorstore embeddings model is from the GPT4AllEmbeddings technical documentation from LangChain
def initialize_embeddings(debug=False):
    # Parameters to initialize embeddings model
    model_name = "all-MiniLM-L6-v2.gguf2.f16.gguf"
    gpt4all_kwargs = {'allow_download': 'True'}
    # Initialize embeddings model
    gpt4all_embd = GPT4AllEmbeddings(
        model_name=model_name,
        gpt4all_kwargs=gpt4all_kwargs
    )
    # Testing
    if debug == True:
        print("Debugging initialize_mbeddings")
        query_result = gpt4all_embd.embed_query("This is test doc")
        print(query_result)
    
    return gpt4all_embd


# Build vectorstore
def build_vectorstore(documents_dir = "documents", chunk_size =250, chunk_overlap=0, collection_name = "rag-chroma"):

    # Documents in this direcory will be embedded
    documents = os.listdir(documents_dir)

    # Load docs
    docs = []
    for doc in documents:
        # Only open .txt
        if doc.endswith(".txt"):
            file_path = os.path.join(documents_dir, doc)
            docs.append(TextLoader(file_path).load())

    # Flattens docs to prepare for embedding
    docs_list = [item for sublist in docs for item in sublist]

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    doc_splits = text_splitter.split_documents(docs_list)

    gpt4all_embd = initialize_embeddings()

    # Add to vectorDB
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="rag-chroma",
        embedding=gpt4all_embd,
    )
    retriever = vectorstore.as_retriever()

    return retriever

def create_retrieval_grader(local_llm, retriever, debug=False):
    ### Retrieval Grader

    # LLM
    llm = ChatOllama(model=local_llm, format="json", temperature=0)

    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an expert grader assessing usefulness
        of a retrieved document to a user query. If the document contains keywords that are useful for the query, 
        grade it as relevant. It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question. \n
        Provide the binary score as a JSON with a single key 'score' and no premable or explanation.
        <|eot_id|><|start_header_id|>user<|end_header_id|>
        Here is the retrieved document: \n\n {document} \n\n
        Here is the user query: {question} \n <|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """,
        input_variables=["question", "document"],
    )

    retrieval_grader = prompt | llm | JsonOutputParser()

    # Test
    if debug == True:
        question = "Find an interesting entry"
        docs = retriever.invoke(question)  
        doc_txt = docs[0].page_content
        print("Document: ", doc_txt)
        print("Grade: ", retrieval_grader.invoke({"question": question, "document": doc_txt}))

    return retrieval_grader

def create_rag_chain(local_llm, retriever, debug=False):
    ### Generate

    # Prompt
    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an expert assistant for query-answering tasks. 
        Use the following pieces of retrieved context to answer the query. If you don't know, just say that you don't know. 
        <|eot_id|><|start_header_id|>user<|end_header_id|>
        Question: {question} 
        Context: {context} 
        Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
        input_variables=["question", "context"],
    )

    llm = ChatOllama(model=local_llm, temperature=0)


    # Post-processing
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Chain
    rag_chain = prompt | llm | StrOutputParser()

    # Test
    if debug == True:
        question = "Tell me a fact"
        docs = retriever.invoke(question)
        # Extract page_content from each document
        doc_content = [doc.page_content for doc in docs]
        print(doc_content)
        print(question)
        generation = rag_chain.invoke({"context": doc_content, "question": question})
        print(generation)

    return rag_chain

def create_hallucination_grader(local_llm, retriever, debug=False):
    ### Hallucination Grader
    # LLM
    llm = ChatOllama(model=local_llm, format="json", temperature=0)

    # Prompt
    prompt = PromptTemplate(
        template=""" <|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an expert grader assessing whether 
        a result is grounded in a set of documents. Give a binary 'yes' or 'no' score to indicate 
        whether the generation is grounded in a set of documents. Provide the binary score as a JSON with a 
        single key 'score' and no preamble or explanation. <|eot_id|><|start_header_id|>user<|end_header_id|>
        Here are the documents:
        \n ------- \n
        {documents} 
        \n ------- \n
        Here is the question: {question} \n
        Here is the answer: {generation}  <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
        input_variables=["generation", "documents"],
    )

    hallucination_grader = prompt | llm | JsonOutputParser()

    # Test
    if debug == True:
        question = "Does this document say 'This is a test'"
        generation = "No, this document does not"
        doc_content = "This is a test"
        score = hallucination_grader.invoke({"documents": doc_content, "question": question, "generation": generation})
        # Extract page_content from each document
        print(doc_content)
        print(question)
        print(generation)
        print(f"Grader response: {score}")
    
    return hallucination_grader

def create_answer_grader(local_llm, debug=False):
    ### Answer Grader

    # LLM
    llm = ChatOllama(model=local_llm, format="json", temperature=0)

    # Prompt
    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an expert grader assessing whether an 
        answer is relevant to a query. Give a binary score 'yes' or 'no' to indicate whether the answer is
        relevant to the query. Provide the binary score as a JSON with a single key 'score' and no preamble or explanation.
        <|eot_id|><|start_header_id|>user<|end_header_id|> Here is the answer:
        \n ------- \n
        {generation} 
        \n ------- \n
        Here is the query: {question} <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
        input_variables=["generation", "question"],
    )

    answer_grader = prompt | llm | JsonOutputParser()

    # Test
    if debug == True:
        question = "This is a test"
        generation = "This document says This is a Test"
        score = answer_grader.invoke({"question": question, "generation": generation})
        print("question :", question)
        print("generation: ", generation)
        print(f"Grader response: {score}")

    return answer_grader

def create_question_router(local_llm, retriever, debug=False):
    ### Router

    from langchain_community.chat_models import ChatOllama
    from langchain_core.output_parsers import JsonOutputParser
    from langchain_core.prompts import PromptTemplate

    # LLM
    llm = ChatOllama(model=local_llm, format="json", temperature=0)

    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an expert at routing a 
        user question to a vectorstore or web search. Use web search if the query contains the following string "Search the web"
        Otherwise, use the vectorstore. Give a binary choice 'web_search' or 'vectorstore' based on the question. 
        Return the a JSON with a single key 'datasource' and no premable or explanation.
        Question to route: {question} <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
        input_variables=["question"],
    )

    question_router = prompt | llm | JsonOutputParser()

    # Test
    if debug == True:
        # question = "Who created the internet"
        question = "Who created the internet? Search the web."
        docs = retriever.invoke(question)
        doc_txt = docs[1].page_content
        print("question :", question)
        print(question_router.invoke({"question": question}))
    
    return question_router

def create_web_search_tool(k=3):
    web_search_tool = TavilySearchResults(k=k)
    return web_search_tool

from typing import Any

### State
class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        web_search: whether to add search
        documents: list of documents
    """

    question: str
    generation: str
    web_search: str
    documents: List[str]


### Nodes


def retrieve(state):
    """
    Retrieve documents from vectorstore

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    print("---RETRIEVE---")
    question = state["question"]
    # Get retriever 
    retriever = build_vectorstore()

    # Retrieval
    documents = retriever.invoke(question)
    if debug == True:
        print("documents :", documents)
    return {"documents": documents, "question": question}


def generate(state):
    """
    Generate answer using RAG on retrieved documents

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]

    # RAG generation
    generation = rag_chain.invoke({"context": documents, "question": question})
    return {"documents": documents, "question": question, "generation": generation}


def grade_documents(state):
    """
    Determines whether the retrieved documents are relevant to the question
    If any document is not relevant, we will set a flag to run web search

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Filtered out irrelevant documents and updated web_search state
    """

    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    documents = state["documents"]

    # Score each doc
    filtered_docs = []
    for d in documents:
        score = retrieval_grader.invoke(
            {"question": question, "document": d.page_content}
        )
        grade = score["score"]
        # Document relevant
        if grade.lower() == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d)
        # Document not relevant
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
            # We do not include the document in filtered_docs
            # We set a flag to indicate that we want to run web search
    
    # Only fallback to web search if all of the docs are graded as not relevant
    web_search = "Yes" if not filtered_docs else "No"
    return {"documents": filtered_docs, "question": question, "web_search": web_search}


def web_search(state):
    """
    Web search based based on the question

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Appended web results to documents
    """

    print("---WEB SEARCH---")
    question = state["question"]
    documents = state["documents"]

    # Web search
    docs = web_search_tool.invoke({"query": question})
    web_results = "\n".join([d["content"] for d in docs])
    web_results = Document(page_content=web_results)
    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]
    return {"documents": documents, "question": question}


### Conditional edge


def route_question(state):
    """
    Route question to web search or RAG.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """

    print("---ROUTE QUESTION---")
    question = state["question"]
    print(question)
    source = question_router.invoke({"question": question})
    print(source)
    print(source["datasource"])
    if source["datasource"] == "web_search":
        print("---ROUTE QUESTION TO WEB SEARCH---")
        return "websearch"
    elif source["datasource"] == "vectorstore":
        print("---ROUTE QUESTION TO RAG---")
        return "vectorstore"
    
    # # Uncomment for offline use

    # print("---OFFLINE, ROUTE QUESTION TO RAG---")
    # return "vectorstore"


def decide_to_generate(state):
    """
    Determines whether to generate an answer, or add web search

    Args:
        state (dict): The current graph state

    Returns:
        str: Binary decision for next node to call
    """

    print("---ASSESS GRADED DOCUMENTS---")
    question = state["question"]
    web_search = state["web_search"]
    filtered_documents = state["documents"]

    if web_search == "Yes":
        # All documents have been filtered as not relevant
        # TODO: Take user input yes or no before running web search
        # We will re-generate a new query
        print(
            "---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, INCLUDE WEB SEARCH---"
        )
        return "websearch"
    else:
        # We have relevant documents, so generate answer
        print("---DECISION: GENERATE---")
        return "generate"


### Conditional edge


def grade_generation_v_documents_and_question(state):
    """
    Determines whether the generation is grounded in the document and answers question.

    Args:
        state (dict): The current graph state

    Returns:
        str: Decision for next node to call
    """

    print("---CHECK HALLUCINATIONS---")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    hallucination_grader = create_hallucination_grader(local_llm, retriever, debug)

    score = hallucination_grader.invoke(
        {"documents": documents, "question": question, "generation": generation}
    )

    print("The score is: ", score)
    grade = score["score"]
    print("The grade is: ", grade)

    # Check hallucination
    if grade == "yes":
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        # Check question-answering
        print("---GRADE GENERATION vs QUESTION---")
        answer_grader = create_answer_grader(local_llm, debug)
        score = answer_grader.invoke({"question": question, "generation": generation})
        grade = score["score"]
        if grade == "yes":
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"
    else:
        print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        return "not supported"


def print_result(state):
    print("---RETURN RESULT---")
    docs = state["documents"]
    query = state["question"]
    result = state["generation"]
    
    # Print results
    print("\n")
    print("Question: ", query)
    print("Answer: ", result)
    print("Referenced Documents :")
    # print all docs with metadata
    for doc in docs:
        print("Document: ", doc.metadata, "\n", doc.page_content)
        
    return state

def create_app(retriever):
    workflow = StateGraph(GraphState)

    # Define the nodes
    workflow.add_node("websearch", web_search)  # web search
    workflow.add_node("retrieve", retrieve)  # retrieve
    workflow.add_node("grade_documents", grade_documents)  # grade documents
    workflow.add_node("generate", generate)  # generate
    workflow.add_node("print_result", print_result)  # print final result

    # Build graph
    workflow.set_conditional_entry_point(
        route_question,
        {
            "websearch": "websearch",
            "vectorstore": "retrieve",
        },
    )

    workflow.add_edge("retrieve", "grade_documents")
    workflow.add_conditional_edges(
        "grade_documents",
        decide_to_generate,
        {
            "websearch": "websearch",
            "generate": "generate",
        },
    )
    workflow.add_edge("websearch", "generate")
    workflow.add_conditional_edges(
        "generate",
        grade_generation_v_documents_and_question,
        {
            "not supported": "generate",
            "useful": "print_result", # print final result
            "not useful": "websearch",
        },
    )

    # End workflow after print_result
    workflow.add_edge("print_result", END)
    # Compile
    app = workflow.compile()

    return app

def main(retriever): 
    # Create app workflow
    app = create_app(retriever)
    continue_app = True

    # Begin application
    print("\n")
    print("\n")
    print("\n")
    print("Hello, I am RAGInABox. I use retrieval augmented generation, or RAG, to retrieve documents that are relevant to your questions and augment my generated response using the context from the documents you provide.")

    # Application loop
    while continue_app == True:
        print("\n")
        print("Ask me a question and I will search through your knowledge base to answer it.")
        # Get query from user input
        query = input("Enter your question: ")

        # Generate full result
        inputs = {"question": query}
        print (f"Question: {query}")
        for output in app.stream(inputs):
            for key, value in output.items():
                print(f"Finished running: {key}:")
        result_full = value["generation"]

        # Prompt user to ask another question, or quit
        response = input("Would you like to ask another question? (yes/no): ")
        # If user says anything other than 'yes'
        if response.lower() != 'yes':
            # Exit app
            continue_app = False
            print("Goodbye, I hope I helped")

# Application entry point
if __name__ == "__main__":
    ### Configure environment
    # Run install_dependencies the first time you run the app to install dependencies, then comment out
    install_dependencies()
    
    debug = False
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    os.environ["USER_AGENT"] = "RAGInABox"
    # Add API keys to a config.py file, see example_config.py
    os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
    os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
    ### LLM
    local_llm = "llama3"

    ### Create agent
    retriever = build_vectorstore()
    retrieval_grader = create_retrieval_grader(local_llm, retriever, debug)
    rag_chain = create_rag_chain(local_llm, retriever, debug)
    hallucination_grader = create_hallucination_grader(local_llm, retriever, debug)
    answer_grader = create_answer_grader(local_llm, debug)
    question_router = create_question_router(local_llm, retriever, debug)
    web_search_tool = create_web_search_tool()

    # Start application
    main(retriever)