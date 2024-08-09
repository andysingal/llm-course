from enum import Enum
import json

import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from pydantic import BaseModel, Field

client = OpenAI()
MODEL = "gpt-4o-2024-08-06"


query = """
Hi, I'm having trouble with my recent order. I received the wrong item and need to return it for a refund. 
Can you help me with the return process and let me know when I can expect my refund?
"""

# --------------------------------------------------------------
# Providing a JSON Schema
# --------------------------------------------------------------

system_prompt = """
You are an AI customer care assistant. You will be provided with a customer inquiry,
and your goal is to respond with a structured solution, including the steps taken to resolve the issue and the final resolution.
For each step, provide a description and the action taken.
"""


def get_ticket_response_json(query):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "ticket_resolution",
                "schema": {
                    "type": "object",
                    "properties": {
                        "steps": {
                            "type": "array",
                        },
                        "final_resolution": {
                            "type": "string",
                        },
                    },
                    "required": ["steps", "final_resolution"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        },
    )

    return response.choices[0].message


response = get_ticket_response_json(query)
response.model_dump()

response_json = json.loads(response.content)
for step in response_json["steps"]:
    print(f"Step: {step['description']}")
    print(f"Action: {step['action']}\n")
print(response_json["final_resolution"])

# --------------------------------------------------------------
# Using Pydantic
# --------------------------------------------------------------


class TicketResolution(BaseModel):
    class Step(BaseModel):
        description: str = Field(description="Description of the step taken.")
        action: str = Field(description="Action taken to resolve the issue.")

    steps: list[Step]
    final_resolution: str = Field(
        description="The final message that will be send to the customer."
    )
    confidence: float = Field(description="Confidence in the resolution (0-1)")


def get_ticket_response_pydantic(query: str):
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        response_format=TicketResolution,
    )

    return completion.choices[0].message.parsed


response_pydantic = get_ticket_response_pydantic(query)
response_pydantic.model_dump()

# --------------------------------------------------------------
# Example with Enums
# --------------------------------------------------------------

query = "Hi there, I have a question about my bill. Can you help me?"


class TicketCategory(str, Enum):
    """Enumeration of categories for incoming tickets."""

    GENERAL = "general"
    ORDER = "order"
    RETURN = "return"
    BILLING = "billing"


# Define your desired output structure using Pydantic
class Reply(BaseModel):
    content: str = Field(description="Your reply that we send to the customer.")
    category: TicketCategory
    confidence: float = Field(
        description="Confidence in the category prediction."
    )  # ge=0, le=1,


completion = client.beta.chat.completions.parse(
    model=MODEL,
    response_format=Reply,
    messages=[
        {
            "role": "system",
            "content": system_prompt,
        },
        {"role": "user", "content": query},
    ],
)

reply = completion.choices[0].message.parsed
reply.model_dump()

# --------------------------------------------------------------
# Text summarization
# --------------------------------------------------------------

"""
From: https://cookbook.openai.com/examples/structured_outputs_intro
"""


def get_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    html_content = soup.find("div", class_="mw-parser-output")
    content = "\n".join(p.text for p in html_content.find_all("p"))
    return content


urls = [
    # Article on CNNs
    "https://en.wikipedia.org/wiki/Convolutional_neural_network",
    # Article on LLMs
    "https://wikipedia.org/wiki/Large_language_model",
    # Article on MoE
    "https://en.wikipedia.org/wiki/Mixture_of_experts",
]

content = [get_article_content(url) for url in urls]


summarization_prompt = """
You will be provided with content from an article about an invention.
Your goal will be to summarize the article following the schema provided.
Here is a description of the parameters:
- invented_year: year in which the invention discussed in the article was invented
- summary: one sentence summary of what the invention is
- inventors: array of strings listing the inventor full names if present, otherwise just surname
- concepts: array of key concepts related to the invention, each concept containing a title and a description
- description: short description of the invention
"""


class ArticleSummary(BaseModel):
    invented_year: int
    summary: str
    inventors: list[str]
    description: str

    class Concept(BaseModel):
        title: str
        description: str

    concepts: list[Concept]


def get_article_summary(text: str):
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": summarization_prompt},
            {"role": "user", "content": text},
        ],
        response_format=ArticleSummary,
    )

    return completion.choices[0].message.parsed


summaries = []

for i in range(len(content)):
    print(f"Analyzing article #{i+1}...")
    summaries.append(get_article_summary(content[i]))
    print("Done.")
