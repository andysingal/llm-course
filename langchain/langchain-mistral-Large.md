```py
!pip install -qU langchain-mistralai

from typing import List
from pydantic import BaseModel
from langchain_mistralai import ChatMistralAI

# Mistral AI setup
llm = ChatMistralAI(model="mistral-large-2407", temperature=0)

# Initial prompt
llm.invoke(
    "Write python code to simulate the positions of 3 bodies given their "
    "initial positions, velocities and mass"
) 
# -> AIMessage(content="To simulate the positions of three bodies...", ...)

# Code interpreter tool definition
class code_interpreter(BaseModel):
    """Execute Python code"""
    import_statements: List[str]
    dependencies: List[str]
    code_block: str

# Binding the code interpreter tool with Mistral AI
llm_with_tools = llm.bind_tools([code_interpreter], tool_choice="any")

# Final prompt with access to the code interpreter
llm_with_tools.invoke(
    "Write python code to simulate the positions of 3 bodies given their "
    "initial positions, velocities and mass"
)
```
