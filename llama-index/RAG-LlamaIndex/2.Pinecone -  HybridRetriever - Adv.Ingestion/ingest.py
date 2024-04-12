import os
import openai
import asyncio
import argparse

from dotenv import load_dotenv
from pinecone import Pinecone, PodSpec

from llama_index.core import SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.readers.file import UnstructuredReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.extractors import (
    TitleExtractor,
    # QuestionsAnsweredExtractor,
    # SummaryExtractor,
    # KeywordExtractor,
)
from llama_parse import LlamaParse

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
llama_parse_api_key = os.environ.get("LLAMA_PARSE_API_KEY")

MODEL = os.getenv("MODEL", "gpt-4-0125-preview")
EMBEDDING = os.getenv("EMBEDDING", "text-embedding-3-large")


def get_pinecone_index(pc, index_name):
    pinecone_index = pc.Index(index_name)
    return pinecone_index


def get_pinecone_vector_store(pinecone_index):
    vector_store = PineconeVectorStore(
        pinecone_index=pinecone_index,
        add_sparse_vector=True,
    )
    return vector_store


def create_pinecone_pod(pc, index_name):
    print("Creating pinecone pod")
    pc.create_index(
        name=index_name,
        dimension=3072,
        metric="dotproduct",
        spec=PodSpec(environment="gcp-starter"),
    )


def get_documents(input_dir):
    llama_parser = LlamaParse(
        api_key=llama_parse_api_key, result_type="markdown", verbose=True
    )

    file_extractor = {
        ".pdf": llama_parser,
        ".html": UnstructuredReader(),
        ".txt": UnstructuredReader(),
    }
    print("Reading directory")
    director_reader = SimpleDirectoryReader(
        input_dir=input_dir, file_extractor=file_extractor
    )
    print("Starting document reading")
    documents = director_reader.load_data(show_progress=True)
    return documents


def run_pipeline(documents, vector_store, llm, num_workers):
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=512, chunk_overlap=126),
            TitleExtractor(llm=llm, num_workers=num_workers),
            # QuestionsAnsweredExtractor(questions=3, llm=llm, num_workers=num_workers),
            # SummaryExtractor(
            #    summaries=["prev", "self"], llm=llm, num_workers=num_workers
            # ),
            # KeywordExtractor(keywords=5, llm=llm, num_workers=num_workers),
            OpenAIEmbedding(model=EMBEDDING),
        ],
        vector_store=vector_store,
    )
    for doc in documents:  # Small patch to remove last_accessed_date from metadata
        k = vars(doc)
        del k["metadata"]["last_accessed_date"]
    pipeline.run(documents=documents, show_progress=True, num_workers=num_workers)


async def main():
    print("Starting ingestion")
    input_dir = "./data/source_files/"
    index_name = "rag-index"
    num_cores = os.cpu_count()
    num_workers = min(4, num_cores)
    pc = Pinecone(api_key=pinecone_api_key)
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "--gen",
        action="store_true",
        help="Generate new pinecone index",
    )
    args = parser.parse_args()
    if args.gen:
        create_pinecone_pod(pc, index_name)
    llm = OpenAI(temperature=0.1, model=MODEL, max_tokens=1024)
    pinecone_index = get_pinecone_index(pc, index_name)
    vector_store = get_pinecone_vector_store(pinecone_index)
    documents = get_documents(input_dir)
    print("Starting ingestion pipeline")
    run_pipeline(documents, vector_store, llm, num_workers)


if __name__ == "__main__":
    asyncio.run(main())
