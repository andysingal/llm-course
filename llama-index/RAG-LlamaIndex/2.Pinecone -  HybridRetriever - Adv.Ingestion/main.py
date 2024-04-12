import os
import openai
import chainlit as cl

from pinecone import Pinecone
from llama_index.core import Settings, VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore

openai.api_key = os.environ.get("OPENAI_API_KEY")
pinecone_api_key = os.environ.get("PINECONE_API_KEY")

MODEL = os.getenv("MODEL", "gpt-4-0125-preview")
EMBEDDING = os.getenv("EMBEDDING", "text-embedding-3-large")


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


@cl.on_chat_start
async def start():
    index = load_context()

    query_engine = index.as_query_engine(
        streaming=True,
        similarity_top_k=4,
        vector_store_query_mode="hybrid",
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
