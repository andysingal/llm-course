from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
from llama_index.core.base.llms.types import ChatMessage
from llama_index.llms.ollama import Ollama
import json

# 定义你的LLM
llm = Ollama(model="qwen:7b-chat")
llm.temperature = 0.7
llm.base_url = "http://1.92.64.112:11434"

def generate_events(query):
    """Generator function to yield events from the opperai API."""
    # Calls the opperai API to start a chat session that streams responses
    messages = [
        # ChatMessage(
        #     role="system", content="You are a pirate with a colorful personality"
        # ),
        ChatMessage(role="user", content=query),
    ]
    for message in messages:
        print(message.role.value, message.content)
    # llm.astream_chat
    response = llm.astream_chat(messages)
    print(response)
    # response.print_response_stream()

    # Loops through each piece of data received from the streaming API
    for data in response:
        print(data)  # Prints the raw response data for debugging
        data = json.dumps({'data': data.delta})  # Converts the data into JSON format, assuming `data.delta` is the relevant information
        yield f"data: {data}\n\n"  # Yields the data in a format suitable for SSE (Server-Sent Events)

# 启动 Flask server
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/chat', methods=['GET', 'POST'])
@cross_origin()
def chat():
    query = request.args.get('query') if request.method == 'GET' else request.form.get('query')
    if query is not None:
        messages = [
            # ChatMessage(
            #     role="system", content="You are a pirate with a colorful personality"
            # ),
            ChatMessage(role="user", content=query),
        ]
        for message in messages:
            print(message.role.value, message.content)
        response = llm.chat(messages)
        print(response)
        return jsonify({"response": str(response)})
    else:
        return jsonify({"error": "query field is missing"}), 400

# Defines a route in the Flask app that clients can connect to for receiving streamed events
@app.route('/events')
@cross_origin()
def sse_request():
    query = request.args.get('query') if request.method == 'GET' else request.form.get('query')
    """Route to handle SSE (Server-Sent Events) requests."""
    # Returns a streaming response that yields data from the `generate_events` generator function
    return Response(generate_events(query), content_type='text/event-stream')

if __name__ == '__main__':
    app.run()

#
# from flask import Flask, Response
# from flask_cors import CORS
#
# from opperai import Client
# from opperai.types import ChatPayload, Message
#
# import time
# import json
#
# # Initialize the opperai client with the API key
# client = Client(api_key="op-*****")
#
# # Create a new Flask application
# app = Flask(__name__)
#
# # Enable Cross-Origin Resource Sharing (CORS) for the entire app to accept requests from the specified origin
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
#
# def generate_events():
#     """Generator function to yield events from the opperai API."""
#     # Calls the opperai API to start a chat session that streams responses
#     response = client.functions.chat(
#         "function/path",  # API endpoint or model to use
#         ChatPayload(
#             messages=[Message(role="user", content="Tell me a very short story.")],  # Initial message to start the chat
#         ),
#         stream=True  # Enables streaming responses
#     )
#
#     # Loops through each piece of data received from the streaming API
#     for data in response:
#         print(data)  # Prints the raw response data for debugging
#         data = json.dumps({'data': data.delta})  # Converts the data into JSON format, assuming `data.delta` is the relevant information
#         yield f"data: {data}\n\n"  # Yields the data in a format suitable for SSE (Server-Sent Events)
#
# # Defines a route in the Flask app that clients can connect to for receiving streamed events
# @app.route('/events')
# def sse_request():
#     """Route to handle SSE (Server-Sent Events) requests."""
#     # Returns a streaming response that yields data from the `generate_events` generator function
#     return Response(generate_events(), content_type='text/event-stream')
#
# # Checks if this script is executed as the main program and runs the Flask app
# if __name__ == '__main__':
#     app.run(debug=True, threaded=True, port=5001)  # Runs the app with debugging enabled, in threaded mode, on port 5001

