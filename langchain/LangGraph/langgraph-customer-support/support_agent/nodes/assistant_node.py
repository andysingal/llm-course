from typing import Any, Dict, List

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI

from support_agent.state import AssistantGraphState, RequiredInformation

llm = ChatMistralAI(model="mistral-large-latest")
system = """You are a a helper assistant \n tasked with helping a customer.
            1. You first need to collect their information before you can validated them.
            2. After your collect ALL information say thank you and that you
               are going to validate that information in the backend systems.
            
            The information needs to be collected: 

            class RequiredInformation(BaseModel):
                provided_name: Optional[str] = Field(
                    description="the provided full name of the user"
                )
                provided_id: Optional[int] = Field(description="the provided id name of the user")
                provided_city_of_birth: Optional[str] = Field(
                    description="the provided city of birth of the user"
                )
                provided_4_digits: Optional[int] = Field(
                    description="the provided user last 4 digits of credit card"
                )

            make sure you have the information before you can proceed, but only one field at a time
            if the input from user was wrong please tell them why.
            
            DO NOT FILL IN THE USERS INFORMATION, YOU NEED TO COLLECT IT.
            """
assistant_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        (
            "human",
            "User question: {user_question}"
            "Chat history: {messages}"
            "\n\n What the user have provided so far {provided_required_information} \n\n",
        ),
    ]
)


def assistant_node(state: AssistantGraphState) -> Dict[str, Any]:
    get_information_chain = assistant_prompt | llm
    res = get_information_chain.invoke(
        {
            "user_question": state["user_question"],
            "provided_required_information": state["required_information"],
            "messages": state["messages"] if "messages" in state else [],
        }
    )

    return {"messages": [res]}


def combine_required_info(info_list: List[RequiredInformation]) -> RequiredInformation:
    info_list = [info for info in info_list if info is not None]

    if len(info_list) == 1:
        return info_list[0]
    combined_info = {}
    for info in info_list:
        for key, value in info.dict().items():
            if value is not None:
                combined_info[key] = value
    return RequiredInformation(**combined_info)


def collect_info(state: AssistantGraphState) -> Dict[str, Any]:
    information_from_stdin = str(input("\nenter information\n"))
    structured_llm_user_info = llm.with_structured_output(RequiredInformation)

    information_chain = assistant_prompt | structured_llm_user_info
    res = information_chain.invoke(
        {
            "user_question": state["user_question"],
            "provided_required_information": information_from_stdin,
            "messages": state["messages"],
        }
    )
    if "required_information" in state:
        required_info = combine_required_info(
            info_list=[res, state.get("required_information")]
        )
    else:
        required_info = res
    return {
        "required_information": required_info,
        "messages": [HumanMessage(content=information_from_stdin)],
    }
