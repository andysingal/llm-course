[Gemini](https://github.com/PraveenKS30/GenerativeAI/tree/main/native_sdk/Gemini)

[IMAGE TO TEXT LLM](https://github.com/NISARGAGOWDRU/image-to-text-llm/blob/main/vision.py)


[Gen AI & LLM Security for developers](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/responsible-ai/gemini_prompt_attacks_mitigation_examples.ipynb)

[Gemini 2.0](https://note.com/npaka/n/n36ac85db4114)

```py

from typing import List

import vertexai
from vertexai.preview import reasoning_engines

# TODO(developer): Update and un-comment below lines
# PROJECT_ID = "your-project-id"
# staging_bucket = "gs://YOUR_BUCKET_NAME"

vertexai.init(
    project=PROJECT_ID, location="us-central1", staging_bucket=staging_bucket
)

class LangchainApp:
    def __init__(self, project: str, location: str) -> None:
        self.project_id = project
        self.location = location

    def set_up(self) -> None:
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_google_vertexai import ChatVertexAI

        system = (
            "You are a helpful assistant that answers questions "
            "about Google Cloud."
        )
        human = "{text}"
        prompt = ChatPromptTemplate.from_messages(
            [("system", system), ("human", human)]
        )
        chat = ChatVertexAI(project=self.project_id, location=self.location)
        self.chain = prompt | chat

    def query(self, question: str) -> Union[str, List[Union[str, Dict]]]:
        """Query the application.
        Args:
            question: The user prompt.
        Returns:
            str: The LLM response.
        """
        return self.chain.invoke({"text": question}).content

# Locally test
app = LangchainApp(project=PROJECT_ID, location="us-central1")
app.set_up()
print(app.query("What is Vertex AI?"))

# Create a remote app with Reasoning Engine
# Deployment of the app should take a few minutes to complete.
reasoning_engine = reasoning_engines.ReasoningEngine.create(
    LangchainApp(project=PROJECT_ID, location="us-central1"),
    requirements=[
        "google-cloud-aiplatform[langchain,reasoningengine]",
        "cloudpickle==3.0.0",
        "pydantic==2.7.4",
    ],
    display_name="Demo LangChain App",
    description="This is a simple LangChain app.",
    # sys_version="3.10",  # Optional
    extra_packages=[],
)
# Example response:
# Model_name will become a required arg for VertexAIEmbeddings starting...
# ...
# Create ReasoningEngine backing LRO: projects/123456789/locations/us-central1/reasoningEngines/...
# ReasoningEngine created. Resource name: projects/123456789/locations/us-central1/reasoningEngines/...
# ...
```
