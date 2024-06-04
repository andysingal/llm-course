```py
from typing import Optional

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

class Comic(BaseModel):
    """Information about a comic."""

    # ^ Doc-string for the entity Comic.
    # This doc-string is sent to the LLM as the description of the schema Comic,
    # and it can help to improve extraction results.

    # Note that:
    # 1. Each field is `optional` -- this allows the model to decline to extract it!
    # 2. Each field has a `description` -- this description is used by the LLM.
    # Having a good description can help improve extraction results.
    comic: Optional[str] = Field(
        default=None, description="The name of the comic"
    )


from langchain_core.prompts import ChatPromptTemplate

# Define a custom prompt to provide instructions and any additional context.
# 1) You can add examples into the prompt template to improve extraction quality.
# 2) Introduce additional parameters to take context into account (e.g., include metadata
#    about the document from which the text was extracted.)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract relevant information from the text. "
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value.",
        ),
        # Please see the how-to about improving performance with
        # reference examples.
        # MessagesPlaceholder('examples'),
        ("human", "{text}"),
    ]
)

llm = ChatOpenAI()
runnable = prompt | llm.with_structured_output(schema=Comic)

text = "What is Kaiji about?"
runnable.invoke({"text": text})
```
