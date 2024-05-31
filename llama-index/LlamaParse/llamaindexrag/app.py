import traceback

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from query_response import get_rag_response_from_query

app = Flask(__name__)
CORS(app, support_credentials=True)
# app.secret_key = ""
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # 2 space indentation
app.config['JSON_SORT_KEYS'] = False  # avoids jsonify to sort the keys in alphabetical manner


@app.route('/')
@cross_origin(supports_credentials=True)
def home_page():
    result = [
        {
            'Created By': 'Global Medics Australia Pty Ltd : https://globalmedics.ai/',
            'description': 'RAG for medical documents',
        }
    ]
    return jsonify(result)


# predict will provide the response for the function created in Model Prediction.py
@app.route('/rag', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
def rag_medical_documents():
    if request.method == 'GET':
        try:

            response = get_rag_response_from_query()
            print(type(response))
            return response
        except:
            return jsonify({'trace': traceback.format_exc()})


if __name__ == '__main__':
    app.run(debug=False)
