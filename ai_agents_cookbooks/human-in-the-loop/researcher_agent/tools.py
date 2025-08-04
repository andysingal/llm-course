from typing import List
from langchain_core.tools import tool
from config import get_tavily
from langgraph.types import interrupt

@tool
def get_human_feedback(question: List[str]):
    """generate a list of questions to get human feedback."""
    value = interrupt(question)
    return value
    


@tool
def search_web(question: str) -> str:
    """Search the web for the given question using the Tavily client."""
    tavily_client = get_tavily()
    response = tavily_client.search(question)
    return response





