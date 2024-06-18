from typing import List

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.agents import Tool
from langchain_experimental.utilities import PythonREPL
from langchain_community.tools.tavily_search import TavilySearchResults

def get_tools() -> List[Tool]:
    """
    Returns a list of tools that can be used by an agent.
    """
    tools = []

    # Create the tools
    internet_search = get_tabily_search_tool()
    repl_tool = get_python_interpreter_tool()

    tools.append(internet_search)
    tools.append(repl_tool)

    return tools

def get_tabily_search_tool() -> Tool:
    """
    Returns a tool that searches the internet for a query using the Tavily API.

    Returns:
        TavilySearchResults: A tool that searches the internet for a query using the Tavily API.
    """
    internet_search = TavilySearchResults()
    internet_search.name = 'internet_search'
    internet_search.description = 'Returns a list of relevant document snippets for a textual query retrieved from the internet.'

    class TavilySearchInput(BaseModel):
        query: str = Field(description='Query to search the internet with')

    internet_search.args_schema = TavilySearchInput

    return internet_search


def get_python_interpreter_tool() -> Tool:
    """
    Creates a tool that executes python code and returns the result.

    Returns:
        Tool: A tool that executes python code and returns the result.
    """
    python_repl = PythonREPL()

    repl_tool = Tool(
        name='python_repl',
        description='Executes python code and returns the result. The code runs in a static sandbox without interactive mode, so print output or save output to a file.',
        func=python_repl.run,
    )
    repl_tool.name = 'python_interpreter'

    # from langchain_core.pydantic_v1 import BaseModel, Field
    class ToolInput(BaseModel):
        code: str = Field(description='Python code to execute.')

    repl_tool.args_schema = ToolInput

    return repl_tool

