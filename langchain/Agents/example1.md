[Langchain (Upgraded) + DeepSeek-R1 + RAG Just Revolutionized AI Forever](https://gaodalie.substack.com/p/langchain-upgraded-deepseek-r1-rag)


```py
from langchain import hub
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_experimental.tools.python.tool import PythonAstREPLTool
from langchain_openai import ChatOpenAI

# Set up the LLM
llm = ChatOpenAI(
    openai_api_key = 'REPLACE_THIS_WITH_YOUR_OPENAI_API_KEY',
    temperature = 0,
    model = 'gpt-3.5-turbo')

# Content of the prompt template
template = '''
Answer the following question as best you can. 
Do not use a tool if not required. 
Question: {question}
'''

# Create the prompt template
prompt_template = PromptTemplate.from_template(template)
prompt = hub.pull('hwchase17/react')

# Set up the Python REPL tool
python_repl = PythonAstREPLTool()
python_repl_tool = Tool(
    name = 'Python REPL',
    func = python_repl.run,
    description = '''
    A Python shell. Use this to execute python commands. 
    Input should be a valid python command. 
    When using this tool, sometimes output is abbreviated - make sure 
    it does not look abbreviated before using it in your answer.
    '''
)

# Set up the DuckDuckGo Search tool
search = DuckDuckGoSearchRun()
duckduckgo_tool = Tool(
    name = 'DuckDuckGo Search',
    func = search.run,
    description = '''
    A wrapper around DuckDuckGo Search. 
    Useful for when you need to answer questions about current events. 
    Input should be a search query.
    '''
)

# Create an array that contains all the tools used by the agent
tools = [python_repl_tool, duckduckgo_tool]

# Create a ReAct agent
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, 
    tools = tools,
    verbose = True, # explain all reasoning steps
    handle_parsing_errors=True, # continue on error 
    max_iterations = 10 # try up to 10 times to find the best answer
)

# Ask your question (replace this with your question)
question = "What is '(4876 * 1032 / 85) ^ 3'?"
output = agent_executor.invoke({'input': prompt_template.format(question=question)})
```



Example2
```py
from langchain.chains import LLMMathChain  # Need to pip install numexpr

from langchain.agents import Tool
from langchain.agents import initialize_agent, AgentType
from langchain_experimental.utilities import PythonREPL

from langchain.retrievers.tavily_search_api import TavilySearchAPIRetriever

from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os

# Set OpenAI API key
dotenv_path = ".env"
load_dotenv(dotenv_path)

OPENAI_API_BASE = os.getenv('OPENAI_API_BASE')
OPENAI_API_VERSION = os.getenv('OPENAI_API_VERSION')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

os.environ["AZURE_OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["AZURE_OPENAI_ENDPOINT"] = OPENAI_API_BASE

llm = AzureChatOpenAI(
    api_version=OPENAI_API_VERSION,
    azure_deployment="gpt4o"  # azure_deployment = "deployment_name"
)

llm_math_chain = LLMMathChain(llm=llm, verbose=True)

# Prepare and verify TavilySearchAPIRetriever
retriever = TavilySearchAPIRetriever(k=3)

python_repl = PythonREPL()
# You can create the tool to pass to an agent

tools = [
    Tool(
        name="python_repl",
        description="A Python shell. Use this to execute Python commands. Input should be a valid Python command. If you want to see the output of a value, you should print it out with `print(...)`.",
        func=python_repl.run,
    ),
    Tool(
        name="Search",
        func=retriever.invoke,
        description="Useful for when you need to answer questions about current events"
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="Useful for when you need to answer questions about math"
    )
]

print(f"length of tools: {len(tools)}")
for i in range(len(tools)):
    print(f"description of tool: {tools[i].description}")

# Initialize the agent
agent_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

# Run the agent
agent_chain.invoke(
    "Search for how many gold medals Japan has won in the 2024 Paris Olympics, and then provide the square of that number."
)
```
