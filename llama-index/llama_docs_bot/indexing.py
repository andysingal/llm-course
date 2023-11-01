import os
import nest_asyncio
nest_asyncio.apply()

from .markdown_docs_reader import MarkdownDocsReader
from llama_index import (
    SimpleDirectoryReader, 
    VectorStoreIndex,
    StorageContext, 
    load_index_from_storage
)
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.node_parser import HierarchicalNodeParser, get_leaf_nodes
from llama_index.retrievers import AutoMergingRetriever
from llama_index.schema import Document, MetadataMode
from llama_index.storage.docstore import SimpleDocumentStore
from llama_index.tools import QueryEngineTool, ToolMetadata 


# load documents
def load_markdown_docs(filepath):
    """Load markdown docs from a directory, excluding all other file types."""
    loader = SimpleDirectoryReader(
        input_dir=filepath, 
        required_exts=[".md"],
        file_extractor={".md": MarkdownDocsReader()},
        recursive=True
    )

    documents = loader.load_data()

    # combine all documents into one
    documents = [
        Document(text="\n\n".join(
                document.get_content(metadata_mode=MetadataMode.ALL) 
                for document in documents
            )
        )
    ]

    # chunk into 3 levels
    # majority means 2/3 are retrieved before using the parent
    large_chunk_size = 1536
    node_parser = HierarchicalNodeParser.from_defaults(
        chunk_sizes=[
            large_chunk_size, 
            large_chunk_size // 3,
        ]
    )

    nodes = node_parser.get_nodes_from_documents(documents)
    return nodes, get_leaf_nodes(nodes)


def get_query_engine_tool(directory, description, postprocessors=None):
    try:
        storage_context = StorageContext.from_defaults(
            persist_dir=f"./data_{os.path.basename(directory)}"
        )
        index = load_index_from_storage(storage_context)

        retriever = AutoMergingRetriever(
            index.as_retriever(similarity_top_k=12), 
            storage_context=storage_context
        )
    except:
        nodes, leaf_nodes = load_markdown_docs(directory)

        docstore = SimpleDocumentStore()
        docstore.add_documents(nodes)
        storage_context = StorageContext.from_defaults(docstore=docstore)

        index = VectorStoreIndex(leaf_nodes, storage_context=storage_context)
        index.storage_context.persist(persist_dir=f"./data_{os.path.basename(directory)}")

        retriever = AutoMergingRetriever(
            index.as_retriever(similarity_top_k=12), 
            storage_context=storage_context
        )

    query_engine = RetrieverQueryEngine.from_args(
        retriever,
        node_postprocessors=postprocessors or [],
    )

    return QueryEngineTool(query_engine=query_engine, metadata=ToolMetadata(name=directory, description=description))
