from dotenv import load_dotenv

load_dotenv()
from typing import List, Union

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.pydantic_v1 import BaseModel
from langserve import add_routes

from support_agent.graph import graph


class ChatInputType(BaseModel):
    input: List[Union[HumanMessage, AIMessage, SystemMessage]]


def test_locally():
    for output in graph.stream(
        {"user_question": "What information do you have on me?"},
        config={"configurable": {"thread_id": 888}},
    ):
        for key, value in output.items():
            if "messages" in value:
                try:
                    last_msg = value["messages"][-1]
                    last_msg.pretty_print()
                except Exception as e:
                    print(last_msg)
    print(graph.get_state({"configurable": {"thread_id": 3}}))


def start() -> None:
    app = FastAPI(
        title="Gen UI Backend",
        version="1.0",
        description="A simple api server using Langchain's Runnable interfaces",
    )

    origins = [
        "http://localhost",
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # unnable = graph.with_types(input_type=ChatInputType, output_type=dict)

    add_routes(app, graph, path="/chat", playground_type="chat")
    print("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    # start()
    test_locally()
