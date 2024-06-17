from typing import Annotated, Optional, TypedDict

from langchain_core.pydantic_v1 import BaseModel, Field
from langgraph.graph import add_messages


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


class AssistantGraphState(TypedDict):

    user_question: str
    required_information: RequiredInformation
    messages: Annotated[list, add_messages]
    verified: bool
