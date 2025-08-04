from typing import Annotated, TypedDict
from langgraph.graph import add_messages

class ResearcherState(TypedDict):
    messages: Annotated[list, add_messages]
    input: str
    research_result: str