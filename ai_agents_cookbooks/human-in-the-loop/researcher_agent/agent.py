
from typing import Literal
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command
from config import get_openai_api_key
from researcher_state import ResearcherState
from researcher_agent.prompt import agent_system_prompt
from researcher_agent.tools import get_human_feedback, search_web
from researcher_agent.output_parser import Researcher_parser


tools = [get_human_feedback, search_web]

def researcher_agent(state: ResearcherState) -> Command[Literal['__end__']]:
   
    researcher_agent = create_react_agent(
        "openai:gpt-4o-mini",
        tools=tools,
        prompt=agent_system_prompt, 
        response_format = Researcher_parser
    )

    response = researcher_agent.invoke(state)

    # extract structured output
    research_result = response['structured_response'].research_result

    update = {
        "input": state['messages'],
        "research_result": research_result
    }
    
    return Command(goto='__end__', update=update)