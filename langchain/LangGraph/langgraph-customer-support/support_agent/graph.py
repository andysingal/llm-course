from dotenv import load_dotenv

load_dotenv()

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt.tool_node import ToolNode

from support_agent.nodes.safe_agent import assistant_with_tools
from support_agent.tools.safe_tools import safe_tools

from langgraph.graph import END, StateGraph

from support_agent.consts import (
    ASSISTANT,
    COLLECT_INFO,
    SAFE_ACTION,
    VERIFY_INFORMATION,
)
from support_agent.nodes.assistant_node import assistant_node, collect_info
from support_agent.nodes.verify_information import verify_information
from support_agent.state import AssistantGraphState, RequiredInformation


def provided_all_details(state: AssistantGraphState) -> str:
    if "required_information" not in state:
        return "need to collect more information"
    provided_information: RequiredInformation = state["required_information"]
    if (
        provided_information.provided_name
        and provided_information.provided_id
        and provided_information.provided_city_of_birth
        and provided_information.provided_4_digits
    ):
        return "all information collected"

    else:
        return "need to collect more information"


def verified(state: AssistantGraphState) -> str:
    verified_successfully = state["verified"]

    if verified_successfully:
        return "agent_with_tools"
    else:
        return ASSISTANT


def route_safe_no_safe(state: AssistantGraphState) -> str:
    ai_message = state["messages"][-1]

    first_tool_call = ai_message.tool_calls[0]
    if first_tool_call["name"] in [tool.name for tool in safe_tools]:
        return "safe_tools"
    else:
        raise END


workflow = StateGraph(AssistantGraphState)
workflow.add_node(ASSISTANT, assistant_node)
workflow.add_node(COLLECT_INFO, collect_info)
workflow.add_node(VERIFY_INFORMATION, verify_information)
workflow.add_node("agent_with_tools", assistant_with_tools)
workflow.add_node("safe_tools", ToolNode(safe_tools))


workflow.set_entry_point(ASSISTANT)
workflow.add_edge(ASSISTANT, COLLECT_INFO)
workflow.add_conditional_edges(
    COLLECT_INFO,
    provided_all_details,
    {
        "need to collect more information": "assistant",
        "all information collected": "verify_information",
    },
)
workflow.add_conditional_edges(
    VERIFY_INFORMATION,
    verified,
    {"agent_with_tools": "agent_with_tools", ASSISTANT: ASSISTANT},
)
workflow.add_edge("safe_tools", END)
workflow.add_conditional_edges(
    "agent_with_tools", route_safe_no_safe, {"safe_tools": "safe_tools", END: END}
)
memory = SqliteSaver.from_conn_string(":checkpoints.sqlite:")
graph = workflow.compile(checkpointer=memory)

graph.get_graph().draw_mermaid_png(output_file_path="graph.png")
