```py
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator, field_validator
from typing import List

class Suggestions(BaseModel):
    words: List[str] = Field(description="""list of substitute words based on context""")

    @field_validator('words')
    def check_list_format(cls, value, info):  # using info parameter
        if len(value) > 1 and all(item[0].isnumeric() for item in value):
            raise ValueError("The input appears to be a numbered list, which is not supported.")
        return value

parser = PydanticOutputParser(pydantic_object=Suggestions)


template =""" Offer a list of suggestions to substitute the specified target_word based the presented context
{format_instruction}

target_word={target_word}
context={context}
"""
target_word="behavior"

context="""The behavior of the students in the classroom was disruptive and made it difficult for the teacher to conduct the lesson."""

prompt_template = PromptTemplate(
    template=template,
    input_variables=["target_word","context"],
    partial_variables={"format_instructions":parser.get_format_instructions()}

```
