from credentials import openai_api_key
import base64
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage, AIMessage

#image encoder
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
    
#tool to describe the image
class ImageDescriberTool(BaseTool):
    name = "Image describer tool"
    description = "Use this tool when given the image path that needs to be described. " \
                  "It will return texts describing the image from the given image path."

    def _run(self, user_question, image_path):
        image = encode_image(image_path)
        chain = ChatOpenAI(model_name="gpt-4-vision-preview", openai_api_key=openai_api_key,
    temperature=0)
        print("Image descriptor tool is run...")
        msg = chain.invoke(
            [   AIMessage(
                content="You are a useful bot that is especially good at answering user's question based on question asked."
            ),
                HumanMessage(
                    content=[
                        {"type": "text", "text": f"{user_question}"},
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
