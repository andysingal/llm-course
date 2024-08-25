[Agent-YOLO](https://note.com/pon_pon_ponkichi/n/n1f1b0b662e7c)

```py
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os

# Setting up the OpenAI API key
dotenv_path = ".env"
load_dotenv(dotenv_path)

OPENAI_API_BASE = os.getenv('OPENAI_API_BASE')
OPENAI_API_VERSION = os.getenv('OPENAI_API_VERSION')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

os.environ["AZURE_OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["AZURE_OPENAI_ENDPOINT"] = OPENAI_API_BASE

llm = AzureChatOpenAI(
    api_version=OPENAI_API_VERSION, 
    azure_deployment="gpt4o" # azure_deployment = "deployment_name"
    )

```

```py
import base64
from ultralytics import YOLO
from collections import Counter

from langchain_core.output_parsers import StrOutputParser
from langchain.tools import tool  # Import the tool decorator

##### Configure an object detection agent with gpt4o #####

def encode_image(image_path):
    """Encode an image file to a base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

@tool
def ObjectDetectTool(image_path: str = None):
    """A tool that recognizes images and describes what they depict. Input should be an image path."""
    
    base64_image = encode_image(image_path)
    image_template = {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
        }
    }
    
    system_prompt = "Please describe the provided image."
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": [
            # {"type": "text", "text": "Describe the images as an alternative text"},
            image_template
        ]}
    ]
    
    chain = llm | StrOutputParser()
    
    return chain.invoke(messages)

##### Configure an object counting agent with YOLO #####

def detect_objects_in_image(image_path):
    """Detect objects in an image using YOLO and count their occurrences."""
    # Load YOLO model
    # model = YOLO("yolov9c.pt")
    model = YOLO("yolov10n.pt")
    
    # Run inference on the image
    results = model(image_path)
    
    # Get detection results
    classes = results[0].boxes.cls.tolist()
    names = results[0].names

    # Use Counter for counting
    class_counts = Counter()
    # Iterate through the results and count occurrences
    for cls in classes:
        name = names[int(cls)]
        class_counts[name] += 1
    
    # Count objects by class
    object_counts = {}  # Define as a dictionary

    # Add results to the dictionary
    for name, count in class_counts.items():
        object_counts[name] = f"{count} items"

    print(object_counts)
    
    return object_counts

@tool
def ObjectCountTool(image_path: str = None):
    """A tool that counts the number of objects in the image and returns the counts. Input should be an image path."""
    object_counts = detect_objects_in_image(image_path)
    return object_counts
```

## Agent

```py
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

tools = [ObjectCountTool, ObjectDetectTool]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You're a helpful assistant"), 
    ("human", "{input}"), 
    ("placeholder", "{agent_scratchpad}"),
])

# Prepare the Tool Calling Agent
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Execute the Tool Calling Agent
agent_executor.invoke({"input": "What is in 'apple.jpg'? Also, please tell me the count."})
```

