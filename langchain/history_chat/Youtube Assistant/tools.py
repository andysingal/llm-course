from credentials import openai_api_key
import base64
from time import sleep
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage, AIMessage

#image encoder
def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except:
        sleep(2)
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
        
    
    
#tool to describe the image
class ImageDescriberTool(BaseTool):
    name = "ImageDescriber"
    description = "Use this tool when given the image path that needs to be described. " \
                  "It will return texts describing the image from the given image path."

    def _run(self, image_path):
        image = encode_image(image_path)
        chain = ChatOpenAI(model_name="gpt-4-vision-preview", openai_api_key=openai_api_key,
    temperature=0)
        msg = chain.invoke(
            [   AIMessage(
                content="You are a useful bot that is especially good at answering user's question based on given input image."
            ),
                HumanMessage(
                    content=[
                        {"type": "text", "text": f"Describe image"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image}"
                            },
                        },
                    ]
                )
            ]
        )
        return msg.content

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")
