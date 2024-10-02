```py
import bs4
from langchain_community.document_loaders import WebBaseLoader

# 여러 개의 url 지정 가능
url1 = "https://blog.langchain.dev/customers-replit/"
url2 = "https://blog.langchain.dev/langgraph-v0-2/"

loader = WebBaseLoader(
    web_paths=(url1, url2),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("article-header", "article-content")
        )
    ),
)
docs = loader.load()
len(docs)
```
