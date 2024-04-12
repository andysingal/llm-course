import os
import openai
import chainlit as cl

from llama_index.core import Settings, load_index_from_storage, StorageContext
from llama_index.llms.openai import OpenAI
from llama_index.core.callbacks import CallbackManager
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.service_context import ServiceContext

openai.api_key = os.environ.get("OPENAI_API_KEY")


@cl.cache
def load_context():
    storage_context = StorageContext.from_defaults(
        persist_dir="./storage",
    )
    index = load_index_from_storage(storage_context)
    return index


@cl.on_chat_start
async def start():
    index = load_context()

    Settings.llm = OpenAI(
        model="gpt-3.5-turbo", temperature=0.1, max_tokens=1024, streaming=True
    )
    Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
    Settings.context_window = 4096
    Settings.callback_manager = CallbackManager([cl.LlamaIndexCallbackHandler()])

    service_context = ServiceContext.from_defaults()
    query_engine = index.as_query_engine(
        streaming=True, similarity_top_k=2, service_context=service_context
    )
    cl.user_session.set("query_engine", query_engine)

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
    query_engine = cl.user_session.get("query_engine")
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
    message_history = message_history[-4:]
    cl.user_session.set("message_history", message_history)

    if response.source_nodes:
        await set_sources(response, response_message)
