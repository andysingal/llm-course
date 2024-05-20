- Agent tools https://qiita.com/sakue_103/items/f8180758df4f281e0bc6
- Cohere Notebooks https://github.com/cohere-ai/notebooks/blob/main/notebooks/Vanilla_Multi_Step_Tool_Use.ipynb 

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

Different tools: https://www.jianshu.com/p/9e646767e5b6 


[Custom Input Schema With Validation Logic in LangChain](https://www.liberiangeek.net/2023/11/how-to-specify-custom-input-schema-with-validation-logic-in-langchain/)

- https://towardsdatascience.com/can-llms-replace-data-analysts-building-an-llm-powered-analyst-851578fa10ce

- https://velog.io/@jjlee6496/Functions-Tools-and-agents-with-Langchain-5-9ban48au
- [Custom Tool](https://www.liberiangeek.net/2023/11/how-to-create-custom-tools-in-langchain/)

- https://langchain114.com/docs/modules/agents/how_to/custom-functions-with-openai-functions-agent/
- [Running Agent as an Iterator](https://linuxhint.com/run-agent-iterator-langchain/)
- [Advanced Tool func](https://velog.io/@jjlee6496/Functions-Tools-and-agents-with-Langchain-6%EC%99%84)
- https://zhuanlan.zhihu.com/p/670788630 

- Multiple documents parsing: https://deeplearning-lab.com/llm/langchain-part-1-2-basicfunction-agent/

```import os
from util import config_util
 
config = config_util.ConfigClsf().get_config()
openai_api_key = os.getenv('OPENAI_API_KEY', config['OPENAI']['API'])
 
from langchain.agents import Tool
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from pydantic import BaseModel, Field
from langchain.agents import AgentType, initialize_agent
from langchain.embeddings import HuggingFaceEmbeddings
 
 
class DocumentInput(BaseModel):
    question: str = Field()
 
hf_embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={'device': 'cuda'},
)
 
llm = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo-0613",
    openai_api_key=openai_api_key
)
 
tools = []
files = [
    {
        "name": "alphabet-earnings",
        "path": "../dataset/2023Q1_alphabet_earnings_release.pdf",
    },
    {
        "name": "tesla-earnings",
        "path": "../dataset/TSLA-Q1-2023-Update.pdf",
    },
]
 
for file in files:
    loader = PyPDFLoader(file["path"])
    pages = loader.load_and_split()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(pages)
    embeddings = hf_embeddings
    retriever = FAISS.from_documents(docs, embeddings).as_retriever()
 
    # Wrap retrievers in a Tool
    tools.append(
        Tool(
            args_schema=DocumentInput,
            name=file["name"],
            description=f"useful when you want to answer questions about {file['name']}",
            func=RetrievalQA.from_chain_type(llm=llm, retriever=retriever),
        )
    )
 
 
 
agent = initialize_agent(
    agent=AgentType.OPENAI_FUNCTIONS,
    tools=tools,
    llm=llm,
    verbose=True,
)
 
print(agent({"input": "did alphabet or tesla have more revenue?"}))
```

  Issues to watch:
  ```
  https://github.com/langchain-ai/langchain/issues/12348
  https://github.com/langchain-ai/langchain/issues/16423 
  ```

Resources:
- https://mer.vin/2024/02/crewai-rag-using-tools/
- https://mer.vin/
- https://blog.lancedb.com/track-ai-trends-crewai-agents-rag/
- https://github.com/tirth-hihoriya/Langchain-agents/tree/master

Crew Examples 
- https://github.com/aday913/crewai-langchain-testing/blob/main/scholar_crew.py
- https://github.com/zemskymax/cpp_ai_programmer/blob/main/main.py

Tool Examples
- https://mer.vin/2024/05/praison-ai-langchain-tavily-wrapper/ 
