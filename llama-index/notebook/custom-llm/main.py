```py 
import os
from dotenv import load_dotenv

load_dotenv()

# llama_index
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent

# tools
from tools.guidelines import guidelines_engine
from tools.web_reader import web_reader_engine
from tools.report_generator import report_generator
from tools.web_loader import web_loader

llm = OpenAI(model="gpt-4o")

agent = ReActAgent.from_tools(
    tools=[
        guidelines_engine,
        web_reader_engine,
        report_generator
        ],
    llm=llm,
    verbose=True
)

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    response = agent.chat(user_input)
    print("Agent: ", response)

```
