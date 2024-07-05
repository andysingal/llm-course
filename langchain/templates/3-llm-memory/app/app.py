import json
import threading

from flask import Flask, current_app, g, jsonify, render_template, request, Response

from config import Config
from database import init_app, db
from models import User, Chat, ChatMessageRole

from services.app_logger import AppLogger
from services.chat_manager import ChatManager
from services.cli_commands import register_cli_commands
from services.llm_client import LlmClient
from services.embedding_function import EmbeddingFunction
from services.vector_store import VectorStore


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_app(app)

    with app.app_context():
        app_boot()

        chat_manager = get_chat_manager()
        logger = get_app_logger()
        # https://stackoverflow.com/a/76884963
        register_cli_commands(app, chat_manager, logger)

    @app.errorhandler(404)
    def not_found(e):
        user = get_user()

        return render_template(
            "404.html",
            title=current_app.config["APP_NAME"],
            model=current_app.config["MODEL"],
            user=user,
        )

    if not app.config["DEBUG"]:

        @app.errorhandler(Exception)
        def handle_error(e):
            user = get_user()

            return render_template(
                "error.html",
                title=current_app.config["APP_NAME"],
                model=current_app.config["MODEL"],
                user=user,
            )

    @app.route("/", methods=["GET"])
    def index():
        user = get_user()
        chat = get_chat()
        chat_json = json.dumps(chat.to_dict())

        return render_template(
            "index.html",
            title=current_app.config["APP_NAME"],
            model=current_app.config["MODEL"],
            user=user,
            chat=chat,
            chat_json=chat_json,
        )

    @app.route("/refresh", methods=["GET"])
    def refresh():
        user = get_user()

        vector_store = get_vector_store()
        vector_store.refresh_index()

        return render_template(
            "page.html",
            title=current_app.config["APP_NAME"],
            model=current_app.config["MODEL"],
            user=user,
            message="Index Refreshed",
        )

    @app.route("/document", methods=["POST"])
    def add_document():
        title = request.json["title"]
        body = request.json["body"]

        vector_store = get_vector_store()
        vector_store.add_document(title, body)

        return jsonify({}), 200

    @app.route("/document/find/<query>", methods=["GET"])
    def find_document(query: str):
        vector_store = get_vector_store()
        result = vector_store.find_document(query)

        return jsonify(result), 200

    @app.route("/prompt", methods=["POST"])
    def prompt():
        user_input = request.json["prompt"].strip()
        llm_client = get_llm_client()

        output = llm_client.get_llm_response(input=user_input)

        return jsonify({"output": output})

    @app.route("/prompt-stream", methods=["POST"])
    def prompt_stream():
        user_input = request.json["prompt"].strip()

        user = get_user()
        chat = get_chat()
        chat_manager = get_chat_manager()

        chat_manager.create_chat_message(
            body=user_input, role=ChatMessageRole.USER, chat=chat, user=user
        )

        chat_summary = ""
        chat_summary_last_message_id = 0

        if chat.chat_summary and chat.chat_summary.body:
            chat_summary = chat.chat_summary.body
            chat_summary_last_message_id = chat.chat_summary.last_message_id

        return Response(
            chat_manager.get_llm_response_stream_and_save_messages(
                assistantRole=ChatMessageRole.ASSISTANT,
                chat=chat,
                chat_messages=chat.chat_messages,
                chat_summary=chat_summary,
                chat_summary_last_message_id=chat_summary_last_message_id,
            ),
            mimetype="text/event-stream",
        )

    # @app.route("/chats", methods=["GET"])
    # def chats():
    #     chats = db.session.execute(db.select(Chat)).scalars().all()
    #     chats = list(map(lambda chat: chat.to_dict(), chats))

    #     return jsonify(chats), 200

    # @app.route("/chats/<id>", methods=["GET"])
    # def chat(id: int):

    @app.route("/chats/<id>/chat-messages", methods=["DELETE"])
    def delete_chat_messages(id: int):
        chat = get_chat()
        chat_manager.delete_chat_messages_and_summary_for_chat(chat=chat)

        return jsonify(), 204

    return app


def app_boot():
    llm_client = get_llm_client()

    # Eagerly load the LLM
    # Use thread to not block render
    # https://github.com/ollama/ollama/blob/main/docs/faq.md#how-can-i-preload-a-model-into-ollama-to-get-faster-response-times
    thread = threading.Thread(target=llm_client.get_llm_response, args=("", False))
    thread.start()


def get_llm_client() -> LlmClient:
    if "llm_client" not in g:
        embedding_function = get_embedding_function()
        vector_store = get_vector_store()
        logger = get_app_logger()

        g.llm_client = LlmClient(
            ollama_instance_url=current_app.config["OLLAMA_INSTANCE_URL"],
            model=current_app.config["MODEL"],
            embedding_function=embedding_function,
            vector_store=vector_store,
            logger=logger,
            debug=current_app.config["DEBUG"],
        )

    return g.llm_client


def get_embedding_function() -> EmbeddingFunction:
    if "embedding_function" not in g:
        g.embedding_function = EmbeddingFunction(
            infinity_instance_url=current_app.config["INFINITY_INSTANCE_URL"],
            embedding_model=current_app.config["EMBEDDING_MODEL"],
        )

    return g.embedding_function


def get_vector_store() -> VectorStore:
    if "vector_store" not in g:
        embedding_function = get_embedding_function()

        g.vector_store = VectorStore(
            search_hostname=current_app.config["SEARCH_HOSTNAME"],
            search_port=current_app.config["SEARCH_PORT"],
            search_auth=(
                current_app.config["SEARCH_USER"],
                current_app.config["SEARCH_PASSWORD"],
            ),
            content_dir=current_app.config["CONTENT_DIR"],
            embedding_function=embedding_function,
        )

    return g.vector_store


def get_user() -> User:
    if "user" not in g:
        g.user = db.session.execute(db.select(User).limit(1)).scalar_one()

    return g.user


def get_chat() -> Chat:
    if "chat" not in g:
        g.chat = db.session.execute(db.select(Chat).limit(1)).scalar_one()

    return g.chat


def get_chat_manager() -> ChatManager:
    if "chat_manager" not in g:
        llm_client = get_llm_client()

        g.chat_manager = ChatManager(
            db_uri=current_app.config["SQLALCHEMY_DATABASE_URI"], llm_client=llm_client
        )

    return g.chat_manager


def get_app_logger() -> AppLogger:
    if "app_logger" not in g:
        g.app_logger = AppLogger(log_dir="logs", log_file="app.log")

    return g.app_logger


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=app.config["APP_PORT"], debug=app.config["DEBUG"])
