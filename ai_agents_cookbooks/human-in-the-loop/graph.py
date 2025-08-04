from langgraph.graph import StateGraph, START, END
from researcher_agent.agent import researcher_agent
from langgraph.checkpoint.memory import InMemorySaver
from researcher_state import ResearcherState






graph_builder = StateGraph(ResearcherState)
graph_builder.add_node("researcher_agent", researcher_agent)
graph_builder.add_edge(START, "researcher_agent")

checkpointer = InMemorySaver()
graph = graph_builder.compile(checkpointer=checkpointer)







