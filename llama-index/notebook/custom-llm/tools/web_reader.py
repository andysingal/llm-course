```py
from llama_index.core import SummaryIndex
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.readers.web import SimpleWebPageReader

def load_index(url: str):
    documents = SimpleWebPageReader(html_to_text=True).load_data([url])
    index = SummaryIndex.from_documents(documents)
    
    return index

def asQueryEngineTool(index):
    
    query_engine = index.as_query_engine()
    
    return QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name="web_reader_engine",
            description="This tool can retrieve content from a web page"
        )
    )
    
index = load_index(
    url="https://www.gettingstarted.ai/crewai-beginner-tutorial"
)

web_reader_engine = asQueryEngineTool(index)

web_reader_engine = QueryEngineTool(
    query_engine=query_engine,
    metadata=ToolMetadata(
        name="web_reader_engine",
        description="This tool can retrieve content from a web page"
    )
)
```
