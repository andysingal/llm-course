import os
import openai
import chainlit as cl

from pinecone import Pinecone
from llama_index.core import Settings, VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.postprocessor.cohere_rerank import CohereRerank
from llama_index.core.indices.query.query_transform.base import (
    StepDecomposeQueryTransform,
)
from llama_index.core.tools import QueryEngineTool
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.query_engine import CustomQueryEngine, RouterQueryEngine
from llama_index.core.base.response.schema import StreamingResponse

openai.api_key = os.environ.get("OPENAI_API_KEY")
cohere_api_key = os.environ.get("COHERE_API_KEY")
pinecone_api_key = os.environ.get("PINECONE_API_KEY")

MODEL = os.getenv("MODEL", "gpt-4-0125-preview")
EMBEDDING = os.getenv("EMBEDDING", "text-embedding-3-large")

direct_llm_prompt = (
    "Given the user query, respond as best as possible following this guidelines:\n"
    "- If the intent of the user is to get information about the abilities of the AI, respond with: "
    "The AI is a language model that can answer questions, generate text, summarize documents, and more. \n"
    "- If the intent of the user is harmful. Respond with: I cannot help with that. \n"
    "- If the intent of the user is to get information outside of the context given, respond with: "
    "I cannot help with that. Please ask something that is relevant with the documents in the context givem. \n"
    "Query: {query}"
)


class LlmQueryEngine(CustomQueryEngine):
    """Custom query engine for direct calls to the LLM model."""

    llm: OpenAI
    prompt: str

    def custom_query(self, query_str: str):
        llm_prompt = self.prompt.format(query=query_str)
        llm_response = self.llm.complete(llm_prompt, formatted=False)

        def response_gen(llm_response):
            for response_tuple in llm_response:
                if response_tuple[0] == "text":
                    text_response = response_tuple[1].replace("AI: ", "").strip()
                    yield text_response
                    continue

        return StreamingResponse(response_gen=response_gen(llm_response))


@cl.cache
def load_context():
    Settings.llm = OpenAI(temperature=0.1, model=MODEL, streaming=True)
    Settings.embed_model = OpenAIEmbedding(model=EMBEDDING, embed_batch_size=1)
    Settings.num_output = 1024
    Settings.context_window = 128000
    pc = Pinecone(api_key=pinecone_api_key)
    pinecone_index = pc.Index("rag-index")
    vector_store = PineconeVectorStore(
        pinecone_index=pinecone_index,
    )

    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
    )
    return index


@cl.step
async def router_query_engine():
    vector_query_engine = cl.user_session.get("vector_query_engine")
    llm_query_engine = cl.user_session.get("simple_query_engine")

    list_tool = QueryEngineTool.from_defaults(
        query_engine=llm_query_engine,
        name="LLM Query Engine",
        description=(
            "Useful for when the INTENT of the user isnt clear, is broad, "
            "or when the user is asking general questions that have nothing "
            "to do with SURA insurance. Use this tool when the other tool is not useful."
        ),
    )

    vector_tool = QueryEngineTool.from_defaults(
        query_engine=vector_query_engine,
        name="Vector Query Engine",
        description=(
            "Useful for retrieving specific context about Paul Graham or anything related "
            "to startup incubation, essay writing, programming languages, venture funding, "
            "Y Combinator, Lisp programming, or anything related to the field of technology "
            "entrepreneurship and innovation."
        ),
    )
    query_engine = RouterQueryEngine(
        selector=LLMSingleSelector.from_defaults(),
        query_engine_tools=[
            list_tool,
            vector_tool,
        ],
    )
    print("Router query engine created.")
    print(query_engine)
    return query_engine


@cl.on_chat_start
async def start():
    index = load_context()

    reranker = CohereRerank(api_key=cohere_api_key, top_n=3)
    step_decompose_transform = StepDecomposeQueryTransform(llm=MODEL, verbose=True)

    vector_query_engine = index.as_query_engine(
        streaming=True,
        similarity_top_k=6,
        node_postprocessors=[reranker],
        vector_store_query_mode="hybrid",
        query_transform=step_decompose_transform,
        response_synthesizer_mode=ResponseMode.REFINE,
    )

    simple_query_engine = LlmQueryEngine(
        llm=OpenAI(model="gpt-3.5-turbo"), prompt=direct_llm_prompt
    )

    cl.user_session.set("simple_query_engine", simple_query_engine)
    cl.user_session.set("vector_query_engine", vector_query_engine)

    message_history = []
    cl.user_session.set("message_history", message_history)

    await cl.Message(
        author="Assistant", content="Hello! Im an AI assistant. How may I help you?"
    ).send()


async def set_sources(response, response_message):
    label_list = []
    count = 1
    for sr in response.source_nodes:
        elements = [
            cl.Text(
                name="S" + str(count),
                content=f"{sr.node.text}",
                display="side",
                size="small",
            )
        ]
        response_message.elements = elements
        label_list.append("S" + str(count))
        await response_message.update()
        count += 1
    response_message.content += "\n\nSources: " + ", ".join(label_list)
    await response_message.update()


@cl.on_message
async def main(message: cl.Message):
    query_engine = await router_query_engine()
    message_history = cl.user_session.get("message_history")
    prompt_template = "Previous messages:\n"

    response_message = cl.Message(content="", author="Assistant")

    user_message = message.content

    for message in message_history:
        prompt_template += f"{message['author']}: {message['content']}\n"
    prompt_template += f"Human: {user_message}"

    response = await cl.make_async(query_engine.query)(prompt_template)

    for token in response.response_gen:
        await response_message.stream_token(token)
    if response.response_txt:
        response_message.content = response.response_txt
    await response_message.send()

    message_history.append({"author": "Human", "content": user_message})
    message_history.append({"author": "AI", "content": response_message.content})
    message_history = message_history[-6:]
    cl.user_session.set("message_history", message_history)

    if response.source_nodes:
        await set_sources(response, response_message)
