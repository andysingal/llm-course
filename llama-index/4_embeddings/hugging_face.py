import logging
import os
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.legacy import GPTVectorStoreIndex, SimpleDirectoryReader
from llama_index.legacy import StorageContext, load_index_from_storage, ServiceContext, set_global_service_context
from langchain_g4f import G4FLLM
from g4f import models
import warnings

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore", category=FutureWarning, message=r'`clean_up_tokenization_spaces` was not set')
warnings.filterwarnings("ignore", category=DeprecationWarning)

def initialize_embedding_model(model_name: str):
    """
    Initialize the Hugging Face embedding model.

    Args:
        model_name (str): The name of the Hugging Face model to be used.
    """
    logger.debug(f"Using Hugging Face model: {model_name}")
    try:
        embed_model = HuggingFaceEmbedding(model_name=model_name)
        logger.debug("Hugging Face embedding model initialized successfully.")
        return embed_model
    except Exception as e:
        logger.error(f"Failed to initialize embedding model: {e}")
        raise

def load_documents(data_dir: str):
    """
    Load documents from the specified directory.

    Args:
        data_dir (str): The directory from which to load documents.
    """
    if not os.path.exists(data_dir):
        logger.error(f"Data directory not found: {data_dir}")
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    try:
        documents = SimpleDirectoryReader(data_dir).load_data()
        logger.debug(f"Documents loaded: {documents}")
        return documents
    except Exception as e:
        logger.error(f"Failed to load documents: {e}")
        raise

def create_service_context(embed_model: HuggingFaceEmbedding):
    """
    Create a ServiceContext with the provided embedding model and LLM disabled.

    Args:
        embed_model (HuggingFaceEmbedding): The embedding model to use in the ServiceContext.
    """
    llm = G4FLLM(model=models.default)
    try:
        service_context = ServiceContext.from_defaults(
            embed_model=embed_model,
            chunk_size=800,
            chunk_overlap=20,
            llm=llm,  # Explicitly disable LLM
        )
        logger.debug("Service context configured.")
        set_global_service_context(service_context)
        return service_context
    except Exception as e:
        logger.error(f"Failed to configure service context: {e}")
        raise

def create_and_persist_index(
    documents: list, service_context: ServiceContext, storage_dir: str
):
    """
    Create a vector store index from the documents and persist it to disk.

    Args:
        documents (list): A list of documents to index.
        service_context (ServiceContext): The service context to use for the index.
        storage_dir (str): The directory in which to persist the index.
    """
    try:
        index = GPTVectorStoreIndex.from_documents(
            documents, service_context=service_context
        )
        logger.debug("Index created successfully.")

        index.storage_context.persist(persist_dir=storage_dir)
        logger.debug("Index persisted to disk.")
        return index
    except Exception as e:
        logger.error(f"Failed to create or persist index: {e}")
        raise

def load_index(storage_dir: str, service_context: ServiceContext):
    """
    Load the index from the storage context.

    Args:
        storage_dir (str): The directory from which to load the index.
        service_context (ServiceContext): The service context to use when loading the index.
    """
    try:
        storage_context = StorageContext.from_defaults(persist_dir=storage_dir)
        logger.debug(f"Storage context created with persist directory: {storage_dir}")

        index = load_index_from_storage(
            storage_context=storage_context, service_context=service_context
        )
        logger.debug("Index loaded from storage.")
        return index
    except Exception as e:
        logger.error(f"Failed to load index from storage: {e}")
        raise

def generate_prompt(question, context):
    """
    Generate a prompt for querying the HRMS system.

    Args:
        question (str): The user's question.
        context (str): The document context for answering the question.

    Returns:
        str: Formatted prompt string.
    """
    return f""" 
        You are an AI assistant for a Human Resource Management System (HRMS), responsible for delivering clear and precise answers about company policies based on the provided context. Your responses should be thorough, professional, and maintain an approachable tone.

        **Guidelines:**
        1. Context-Based Responses: Always base your answer strictly on the provided context to ensure relevance.
        2. Completeness: Make sure your answers are comprehensive and coherent. Avoid including incomplete or broken sentences.
        3. Accuracy: Ensure that the information provided is accurate and aligns with the context.
        4. Relevance: If the context doesn’t cover the question, provide the most relevant information available or suggest asking a more specific question.
        5. Clarity: Maintain clear and concise language throughout your response to avoid any ambiguity.
        6. Tone: Keep your tone professional yet approachable, ensuring a human-like interaction.
        7. Handling Greetings: Respond appropriately and helpfully to simple greetings or casual inquiries without deviating from the context.
        8. Word Limit: Keep your response concise, with a maximum of 400 characters, unless the question requires a more detailed explanation.
        9. Format: Structure your response in a single, well-organized paragraph, making it easy to read.
        10. Language: Always respond in clear and correct English, avoiding jargon unless necessary.

        Context: {context}
        User Input: {question}
        """

def query_index(documents, index: GPTVectorStoreIndex, query: str):
    """
    Query the index and return the response.

    Args:
        index (VectorStoreIndex): The vector store index to query.
        query (str): The query string to search in the index.
    """
    try:
        query_engine = index.as_query_engine()
        logger.debug("Query engine created.")
        context = "\n".join([doc.page_content for doc in documents if hasattr(doc, 'page_content')])
        prompt = generate_prompt(query, context)

        response = query_engine.query(prompt)
        if response:
            print("__________________________________________")
            print("LlamaIndex response:", response.response)
        else:
            print("No response from LlamaIndex.")
        return response
    except Exception as e:
        logger.error(f"Failed to query index: {e}")
        raise

def main():
    # Initialize the embedding model
    model_name = "bert-base-nli-mean-tokens"
    embed_model = initialize_embedding_model(model_name)

    # Define data and storage directories
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data")
    storage_dir = "./storage"

    # Create the service context
    service_context = create_service_context(embed_model)

    documents = None
    # Check if the storage directory exists and is not empty (index exists)
    if os.path.exists(storage_dir) and os.listdir(storage_dir):
        logger.debug("Index exists. Loading from storage.")
        index = load_index(storage_dir, service_context)
    else:
        logger.debug("No existing index found. Creating and persisting a new index.")
        # Load documents from the data directory
        documents = load_documents(data_dir)

        # Create and persist the index
        index = create_and_persist_index(documents, service_context, storage_dir)

    # Query the index
    if not documents:
        documents = load_documents(data_dir)
    response = query_index(documents, index, "Tell me about the ownership of the assets")
    logger.debug(f"Final response: {response}")

if __name__ == "__main__":
    main()
