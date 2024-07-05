import threading

from flask import Flask, current_app, g, jsonify, render_template, request, Response

from config import Config

from services.llm_client import LlmClient
from services.embedding_function import EmbeddingFunction
from services.vector_store import VectorStore


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        app_boot()

    @app.errorhandler(404)
    def not_found(e):
        return render_template(
            "404.html",
            title=current_app.config["APP_NAME"],
            model=current_app.config["MODEL"],
        )

    if not app.config["DEBUG"]:

        @app.errorhandler(Exception)
        def handle_error(e):
            return render_template(
                "error.html",
                title=current_app.config["APP_NAME"],
                model=current_app.config["MODEL"],
            )

    @app.route("/", methods=["GET"])
    def index():
        return render_template(
            "index.html",
            title=current_app.config["APP_NAME"],
            model=current_app.config["MODEL"],
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
        llm_client = get_llm_client()

        return Response(
            llm_client.get_llm_response_stream(input=user_input),
            mimetype="text/event-stream",
        )

    @app.route("/refresh", methods=["GET"])
    def refresh():
        vector_store = get_vector_store()
        vector_store.refresh_index()

        return render_template(
            "page.html",
            title=current_app.config["APP_NAME"],
            model=current_app.config["MODEL"],
            message="Index Refreshed",
        )

    return app


def app_boot():
    llm_client = get_llm_client()

    # Eagerly load the LLM
    # Use thread to not block render
    # TODO: not sure if this does anything
    thread = threading.Thread(target=llm_client.get_llm_response)
    thread.start()


def get_llm_client():
    if "llm_client" not in g:
        embedding_function = get_embedding_function()
        vector_store = get_vector_store()

        g.llm_client = LlmClient(
            ollama_instance_url=current_app.config["OLLAMA_INSTANCE_URL"],
            model=current_app.config["MODEL"],
            embedding_function=embedding_function,
            vector_store=vector_store,
        )

    return g.llm_client


def get_embedding_function():
    if "embedding_function" not in g:
        g.embedding_function = EmbeddingFunction(
            infinity_instance_url=current_app.config["INFINITY_INSTANCE_URL"],
            embedding_model=current_app.config["EMBEDDING_MODEL"],
        )

    return g.embedding_function


def get_vector_store():
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


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=app.config["APP_PORT"], debug=app.config["DEBUG"])
