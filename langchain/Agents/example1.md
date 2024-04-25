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
