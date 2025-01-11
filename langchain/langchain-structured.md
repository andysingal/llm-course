```py
from langchain_openai import ChatOpenAI
# Uncomment the following if you have the specific Pydantic version from LangChain
# from langchain_core.pydantic_v1 import BaseModel
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel

# Define the schema using Pydantic
class GetUserDetails(BaseModel):
    '''Extract user contact details.'''
    name: str
    age: int  #  age is required in the above text data to extract but i purposely omitted so since it integer Type it assign default value to age which is zero   
    address: str
    cars: list
    degree: str
    country_from: str

# Load environment variables
load_dotenv()

# Initialize the LLM
llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

# Configure the LLM to output structured data
structured_llm = llm.with_structured_output(GetUserDetails)

# Invoke the LLM with unstructured input
response = structured_llm.invoke(
    "My Name is Sreeni, I live in Dallas, TX, and I hold a degree in MS Computer Science. "
    "I have two cars: Toyota and Lexus. I am originally from India."
)

# Print the extracted structured data
print(response.model_dump())  # Structured output as a dictionary
print(response)  # Human-readable response
```
