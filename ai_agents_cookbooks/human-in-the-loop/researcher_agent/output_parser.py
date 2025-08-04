from typing import List
from pydantic import BaseModel, Field
from typing_extensions import Literal

class Researcher_parser(BaseModel):
    
    research_result: str = Field(
        "summary of search result in markdown format, clean and organized, maximum 50 words"
    )