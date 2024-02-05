"""
    This is the documentaion of the Llama2-7B-chat model from hugging face models
    This model has 7 billion parameters develped by Meta
    
    This is used for QnA purposes on local machine for testing...
    
    Model hardware config:
        - GPU: Nvidia RTX 40 Series (12GB) --> CUDA support 
        - RAM: 32GB
        - i7 processor 13th gen
"""
import torch
from transformers import BitsAndBytesConfig
from langchain.embeddings.huggingface import HuggingFaceInstructEmbeddings

from llama_index.llms import HuggingFaceLLM
from llama_index import ServiceContext, SimpleDirectoryReader, \
    VectorStoreIndex, get_response_synthesizer, set_global_service_context
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.prompts import PromptTemplate
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores import ChromaVectorStore
from llama_index.postprocessor import SimilarityPostprocessor

from chromadb import PersistentClient
from chromadb.utils import embedding_functions

from dotenv import load_dotenv
from transformers import AutoTokenizer
import os


load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

LLM = "meta-llama/Llama-2-7b-chat-hf"
EMBED_MODEL = "hkunlp/instructor-large"
DEVICE_MAP = "auto"
DEVICE = "cuda"


class Llama2_7B_Chat:
    """Class for Llama-7B Chat model from HuggingFace"""

    def __init__(self) -> None:
        """Constrcutor of the class Llama2_7B_Chat"""

        print("==================== starting constructor... ======================")

        # Start chroma client
        self.__chroma_client = PersistentClient('./chroma_db')

        # for model bit quantization for more effiency in computation by the LLM
        self.__quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            llm_int8_enable_fp32_cpu_offload=True
        )
        
        tokenizer = AutoTokenizer.from_pretrained(LLM)

        # HuggingFaceLLM object - uses pretrained models from HuggingFace (Llama2-7B-chat model)
        self.__llm = HuggingFaceLLM(
            model_name=LLM,
            tokenizer=tokenizer,
            is_chat_model=True,
            max_new_tokens=512,
            query_wrapper_prompt=PromptTemplate(
                "<s> [INST] {query_str} [/INST]"),
            context_window=4000,
            model_kwargs={
                "quantization_config": self.__quantization_config,
                "token": HF_TOKEN
            },
            tokenizer_kwargs={
                "token": HF_TOKEN
            },
            device_map=DEVICE_MAP
        )

        # embedding model - pretrained embedding model (it is wrapper around sentence_transformers)
        self.__embed_model = HuggingFaceInstructEmbeddings(
            model_name=EMBED_MODEL,
            model_kwargs={
                "device": DEVICE
            }
        )

        self.__index = None

        # Service context
        self.__service_context = ServiceContext.from_defaults(
            llm=self.__llm, embed_model=self.__embed_model)

        set_global_service_context(self.__service_context)

    def create_index(self, data_dir: str) -> None:
        """Creates the Vector Index for querying with LLM"""

        print("============= creating index.... ================")

        # embedding function for chromadb
        embedding_func = embedding_functions.HuggingFaceEmbeddingFunction(
            api_key=HF_TOKEN,
            model_name=EMBED_MODEL
        )

        # Load the documents from data_dir
        docs = SimpleDirectoryReader(data_dir).load_data()

        # Creating collection in chroma database
        chroma_collection = self.__chroma_client.get_or_create_collection("data_embeddings",
                                                                          embedding_function=embedding_func)

        # Creating Chroma Vector Store
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

        # Create storage context using chroma vector store
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store)

        self.__index = VectorStoreIndex.from_documents(docs, storage_context=storage_context)

    def start_query_engine(self):
        """Initialize the query engine"""

        print("=========== starting query engine... ===============")

        # configure retriever
        retriever = VectorIndexRetriever(
            index=self.__index,
            similarity_top_k=6
        )

        # configure node postproceesors
        s_processor = SimilarityPostprocessor(similarity_cutoff=0.65)

        # configure response synthesizer
        response_synthesizer = get_response_synthesizer()

        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            node_postprocessors=[s_processor],
            response_synthesizer=response_synthesizer
        )

        return query_engine

    def ask_llm(self, user_query: str, query_engine):
        """
            Ask LLM for querying data based on context

            returns: (RESPONSE_TYPE, List[NodeWithScore])
        """

        # print("User asking -->", user_query)

        response = query_engine.query(user_query)

        return response, response.source_nodes


def reset_model():
    """resets the model's knowledge base"""

    os.system("rm -rf Data_*")
    os.system("rm -rf vector_store_data/")
    os.system("rm -rf chroma_db/")
