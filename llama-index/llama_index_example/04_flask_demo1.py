from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from llama_index.core.base.llms.types import ChatMessage
from llama_index.llms.ollama import Ollama

# 定义你的LLM
llm = Ollama(model="qwen:7b-chat")
llm.temperature = 0.7
llm.base_url = "http://1.92.64.112:11434"

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

if __name__ == '__main__':
    app.run()
