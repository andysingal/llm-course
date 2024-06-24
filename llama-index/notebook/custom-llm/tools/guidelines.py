```py
import os
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.readers.file import PDFReader

def load_index(file_path, index_name):
    data = PDFReader().load_data(file=file_path)
    
    if os.path.exists('embeddings/' + index_name):
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir='embeddings/' + index_name)
        )
    else:
        index = VectorStoreIndex.from_documents(data, show_progress=False)
        index.storage_context.persist(persist_dir='embeddings/' + index_name)
        
    return index

def asQueryEngineTool(index):
    query_engine = index.as_query_engine()
    
    return QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name="guidelines_engine",
            description="This tool can retrieve content from the guidelines"
        )
    )
    
file_path = os.path.join("data", "content-guidelines.pdf")
guidelines_index = load_index(file_path, index_name="guidelines")

guidelines_engine = asQueryEngineTool(guidelines_index)
```
