# from flask import Flask
# from flask_restful import Api

# from app.utils import (should_create_index_and_bib,
#                        prepare_index_and_bib,
#                        load_index_and_bib,
#                        load_embedding_model,
#                        load_generation_pipeline,
#                        load_reranker_model)


# def setup_app(app: Flask) -> tuple:
#     embedding_model = load_embedding_model()
#     answer_generator = load_generation_pipeline()
#     reranker_model = load_reranker_model()

#     if should_create_index_and_bib():
#         print('Index and bibliography not found. Creating ....')
#         indexed_chunks, document_embeddings, bibliography_dict = prepare_index_and_bib(embedding_model)
#     else:
#         print('Index and bibliography found. Loading ....')
#         indexed_chunks, document_embeddings, bibliography_dict = load_index_and_bib()

#     app.config['EMBEDDINGS'] = document_embeddings
#     app.config["INDEX"] = indexed_chunks
#     app.config['BIBLIOGRAPHY'] = bibliography_dict
#     app.config['EMBEDDING_MODEL'] = embedding_model
#     app.config['GENERATION_MODEL'] = answer_generator
#     app.config['RERANKER_MODEL'] = reranker_model


# def create_app():
#     app = Flask(__name__)
#     api = Api(app)
#     setup_app(app)

#     from app.routes import initialize_routes
#     initialize_routes(api)
#     return app
