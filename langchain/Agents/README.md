- Agent tools https://qiita.com/sakue_103/items/f8180758df4f281e0bc6

```
from langchain.tools import tool
from langchain.utilities import SerpAPIWrapper
from langchain.chains import LLMMathChain
chain = LLMMathChain(llm=chat_model, verbose=True)

# serp api
# google search를 위해서 google-search-results 패키지를 설치해야 한다.
# SERPAPI_API_KEY에 serpapi key 값을 환경 변수로 등록해야 한다.
@tool("search")
def search_api(query : str) -> str:
    """Searchs the api for the query""" # tool decorator를 사용하면 docstring으로 이에 대한 설명을 적는다.
    search = SerpAPIWrapper()
    result = search.run(query)
    return result

@tool("math")
def math(query : str) -> str:
    """useful for when you need to answer questions about math"""
    llm_math_chain = LLMMathChain(llm=chat_model, verbose=True)
    return llm_math_chain.run(query)

tools = [search_api, math]
```
