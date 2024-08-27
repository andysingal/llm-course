# import os
# import json
# from flask import jsonify, request
# from flask_restful import Resource, current_app
# from werkzeug.utils import secure_filename
# import numpy as np

# from app.utils import (save_index_and_bib,
#                        process_single_pdf,
#                        get_metadata_and_relevant_passages,
#                        generator_answer,
#                        prepare_rag_prompt)

# from config import PDF_DATA_DIR, INDEX_AND_BIB_DIR, BIB_JSON_NAME, DEBUG


# class ManageIndex(Resource):
#     def get(self):
#         "Get request to fetch dictionary of uuid and filename of all PDF document in our Index."
#         try:
#             indexed_chunks = current_app.config.get("INDEX")
#             uuid_mapping = {data["file_metadata"]["uuid"]:os.path.basename(data["file_metadata"]["pdf_path"]) for data in indexed_chunks}
#             return jsonify(uuid_mapping)
#         except Exception as e:
#             print(f'Error occur while getting uuid and document mapping:{e}.')
#             return {"message":"Error while getting uuid and PDF document mapping"}, 500


#     def post(self):
#         "Post request to add new document in the Index."
#         try:
#             if 'file' not in request.files:
#                 return {'message': 'No file part in the request'}, 400
#             file = request.files['file']
#             if file.filename == '':
#                 return {'message': 'No file selected for uploading'}, 400
#             if file and file.filename.lower().endswith('.pdf'):

#                 indexed_chunks = current_app.config.get("INDEX")
#                 embedding_model = current_app.config.get('EMBEDDING_MODEL')

#                 # Save PDF on disk
#                 filename = secure_filename(file.filename)
#                 filepath = os.path.join(PDF_DATA_DIR, filename)
#                 file.save(filepath)
                
#                 # update new document chunks, embeddings and bibliography_dict
#                 single_index = process_single_pdf(filepath, embedding_model)
#                 indexed_chunks_list = indexed_chunks.tolist() if isinstance(indexed_chunks, np.ndarray) else indexed_chunks
#                 indexed_chunks_list.extend(single_index)
#                 indexed_chunks = np.array(indexed_chunks_list)

#                 # Load the existing bibliograph data
#                 with open(os.path.join(INDEX_AND_BIB_DIR, BIB_JSON_NAME), 'r') as file:
#                     bibliography_dict = json.load(file)

#                 current_app.config['EMBEDDINGS'] = save_index_and_bib(indexed_chunks, bibliography_dict= None)
#                 current_app.config["INDEX"] = indexed_chunks 
#                 current_app.config['BIBLIOGRAPHY'] = bibliography_dict

#                 return {'filename': filename, 'uid': single_index[0]["file_metadata"]["uuid"]}, 201
#             return {'message': 'Allowed file type is PDF'}, 400
#         except Exception as e:
#             print(f'Error occur while adding new document in the Index:{e}.')
#             return {"message":"Error while adding new document in the Index."}, 500


#     def delete(self, uid):
#         "Delete request to delete a document from the Index by its uuid"
#         try:
#             indexed_chunks = current_app.config.get("INDEX")
#             bibliography_dict = current_app.config.get('BIBLIOGRAPHY')

#             new_indexed_chunks = []
#             uid_found = False
#             for data in indexed_chunks:
#                 if uid == data["file_metadata"]["uuid"]:
#                     uid_found = True
#                     pdf_path = data["file_metadata"]["pdf_path"] 
#                 else:
#                     new_indexed_chunks.append(data)

#             if uid_found:
#                 if pdf_path in bibliography_dict:
#                     del bibliography_dict[data["file_metadata"]["pdf_path"]]

#                 # Convert list back to numpy array
#                 indexed_chunks = np.array(new_indexed_chunks)
#                 current_app.config['EMBEDDINGS']  = save_index_and_bib(indexed_chunks,bibliography_dict) 
#                 current_app.config["INDEX"] = indexed_chunks 
#                 current_app.config['BIBLIOGRAPHY'] = bibliography_dict
        
#                 return {'message': f'Document with UID {uid} and filename {os.path.basename(pdf_path)} deleted successfully from Index'}, 200
#             return {'message': f'Document with UID {uid} not found in Index'}, 404
#         except Exception as e:
#             return {'message': f'Error occur while deleting the document with UID {uid} in Index'}, 500


# class QueryIndex(Resource):
#     def post(self):
#         try:
#             query = request.json.get('query', '')
#             if not query:
#                 return {'message': 'No query provided'}, 400
            
#             document_embedding = current_app.config['EMBEDDINGS']
#             indexed_chunks = current_app.config["INDEX"]
#             embedding_model = current_app.config['EMBEDDING_MODEL']
#             answer_generator = current_app.config['GENERATION_MODEL']
#             reranker_model = current_app.config['RERANKER_MODEL']
#             bibliography_dict = current_app.config.get('BIBLIOGRAPHY')


#             metadata, passages = get_metadata_and_relevant_passages(query,
#                                                                     indexed_chunks,
#                                                                     embedding_model,
#                                                                     document_embedding,
#                                                                     reranker_model,
#                                                                     bibliography_dict)
#             prompt = prepare_rag_prompt(query,passages)
#             if DEBUG:
#                 print(prompt)
#             answer = generator_answer(prompt,answer_generator)
#             return {"query":query,'answer': answer, 'metadata': metadata}, 200
#         except Exception as e:
#             print(e)
#             return {'message': f'Error occur while generating a answer for query: {query}.'}, 500


# class Bibliography(Resource):
#     def get(self):
#         try:
#             "Get request to fetch dictionary of all Bibliography with NeuralIPS citation style."
#             bibliography_dict = current_app.config.get('BIBLIOGRAPHY')
#             return jsonify(bibliography_dict)
#         except Exception as e:
#             print(f'Error occur while getting bibliography:{e}.')
#             return {"message":"Error while getting Bibliography"}, 500
        
# def initialize_routes(api):
#     api.add_resource(QueryIndex, '/api/query')
#     api.add_resource(ManageIndex,'/api/documents','/api/documents/<string:uid>')
#     api.add_resource(Bibliography,'/api/bibliography')
