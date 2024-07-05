import json
import os
import sys

from pathlib import Path
from typing import Generator, List

from jinja2 import Template
from ollama import Client

from services.app_logger import AppLogger
from services.embedding_function import EmbeddingFunction
from services.vector_store import VectorStore

# TODO better way to do this (import from parent dir)?
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from models import ChatMessage, ChatMessageRole


class LlmClient:
    def __init__(
        self,
        ollama_instance_url: str,
        model: str,
        embedding_function: EmbeddingFunction,
        vector_store: VectorStore,
        logger: AppLogger,
        debug: bool = False,
    ):
        self.ollama_instance_url = ollama_instance_url
        self.model = model
        self.embedding_function = embedding_function
        self.vector_store = vector_store
        self.logger = logger
        self.debug = debug

        self.client = Client(host=ollama_instance_url)
        self.client_options = {
            # "num_ctx": 8000,
            "temperature": 0.2,
            # "top_k": 40,
            # "top_p": 0.9,
        }

        self.prompt_templates_dir = Path(__file__).parent / "prompts"

        self.system_prompt = ""
        with open(f"{self.prompt_templates_dir}/system.j2", "r") as file:
            self.system_prompt = file.read()

        self.rag_prompt_template_string = ""
        with open(f"{self.prompt_templates_dir}/rag_with_sources.j2", "r") as file:
            self.rag_prompt_template_string = file.read()

        self.rag_prompt_template = Template(self.rag_prompt_template_string)

        self.chat_summary_prompt_template_string = ""
        with open(f"{self.prompt_templates_dir}/chat_summary.j2", "r") as file:
            self.chat_summary_prompt_template_string = file.read()

        self.chat_summary_prompt_template = Template(
            self.chat_summary_prompt_template_string
        )

    def get_llm_response(self, input: str = "", use_rag: bool = True) -> str:
        if use_rag:
            chat_prompt = self.get_rag_prompt(input)
        else:
            chat_prompt = input

        self.log_llm_messages(caller="get_llm_response", messages=[chat_prompt])

        response = self.client.generate(
            model=self.model,
            options=self.client_options,
            keep_alive=-1,
            system=self.system_prompt,
            prompt=chat_prompt,
        )
        output = response["response"]
        output = self.clean_output(output)

        return output

    def get_llm_response_stream(
        self, input: str = "", use_rag: bool = True
    ) -> Generator[str, None, None]:
        if use_rag:
            chat_prompt = self.get_rag_prompt(input)
        else:
            chat_prompt = input

        self.log_llm_messages(caller="get_llm_response_stream", messages=[chat_prompt])

        response = self.client.generate(
            model=self.model,
            options=self.client_options,
            keep_alive=-1,
            system=self.system_prompt,
            prompt=chat_prompt,
            stream=True,
        )

        for chunk in response:
            output = chunk["response"]
            output = self.clean_output(output)

            yield output

    def get_llm_chat_response_stream(
        self, messages: List[dict], use_rag: bool = True
    ) -> Generator[str, None, None]:
        messages = self.prepend_system_prompt_to_messages(messages=messages)

        if use_rag:
            messages = self.render_last_message_with_rag_prompt(messages=messages)

        self.log_llm_messages(caller="get_llm_chat_response_stream", messages=messages)

        response = self.client.chat(
            model=self.model,
            options=self.client_options,
            keep_alive=-1,
            messages=messages,
            stream=True,
        )

        for chunk in response:
            output = chunk["message"]["content"]
            output = self.clean_output(output)

            yield output

    def prepend_system_prompt_to_messages(self, messages: List[dict]) -> List[dict]:
        system_message = ChatMessage.convert_chat_message_to_llm_format(
            role=ChatMessageRole.SYSTEM.value, content=self.system_prompt
        )

        messages.insert(0, system_message)

        return messages

    def render_last_message_with_rag_prompt(self, messages: List[dict]) -> List[dict]:
        if messages[-1]["role"] != ChatMessageRole.USER.value:
            # this shouldn't happen
            raise
            return messages

        messages[-1]["content"] = self.get_rag_prompt(input=messages[-1]["content"])

        return messages

    def get_rag_prompt(self, input: str) -> str:
        context = self.get_relevant_context(input)

        chat_prompt = self.rag_prompt_template.render(
            {"question": input, "documents": context}
        )

        return chat_prompt

    def get_relevant_context(self, input: str, max_number_of_docs: int = 3) -> List:
        query_response = self.vector_store.query(text=input, size=max_number_of_docs)

        context = []

        if len(query_response) > 0:
            for document in query_response:
                context.append(
                    {
                        "content": document["fields"]["page_content"],
                        "source": document["fields"]["metadata.source"],
                    }
                )

        return context

    def get_chat_summary(self, chat_messages: List) -> str:
        chat_summary_prompt = self.chat_summary_prompt_template.render(
            {"chat_messages": chat_messages}
        )

        self.log_llm_messages(caller="get_chat_summary", messages=[chat_summary_prompt])

        response = self.client.generate(
            model=self.model,
            options=self.client_options,
            keep_alive=-1,
            system=self.system_prompt,
            prompt=chat_summary_prompt,
        )

        output = response["response"]
        output = self.clean_output(output)

        return output

    def clean_output(self, output: str) -> str:
        ending_token = "<|im_end|>"
        output = output.replace(ending_token, "")

        return output

    def log_llm_messages(self, caller: str, messages: list) -> None:
        if not self.debug:
            return

        messages_json = json.dumps(messages, indent=2)
        log_message_content = f"{caller}:\n{messages_json}"

        self.logger.log(log_message_content)
