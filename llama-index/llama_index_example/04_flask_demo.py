# Import modules
import os

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from llama_index.core import SimpleDirectoryReader, ServiceContext, SummaryIndex
from llama_index.llms.ollama import Ollama


# 定义你的LLM
llm = Ollama(model="pxlksr/defog_sqlcoder-7b-2:Q8")
llm.temperature = 0.2
llm.base_url = "http://1.92.64.112:11434"

# 定义你的服务上下文
model_dir = os.path.abspath('data/embed_model/bge-small-en-v1.5')
service_context = ServiceContext.from_defaults(
    llm=llm, embed_model="local:" + model_dir
)

# 加载你的数据
documents = SimpleDirectoryReader("data").load_data()
index = SummaryIndex.from_documents(documents, service_context=service_context)

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
        query_engine = index.as_query_engine()
        response = query_engine.query(query)
        return jsonify({"response": str(response)})
    else:
        return jsonify({"error": "query field is missing"}), 400


if __name__ == '__main__':
    app.run()