from llama_index.core import StorageContext, load_index_from_storage
import os
from llama_index.core.base.response.schema import Response
import json


def get_rag_response_from_query():
    rag = dict()
    os.environ["OPENAI_API_KEY"] = "sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    storage_context = StorageContext.from_defaults(persist_dir="vectorstorage")
    recursive_index = load_index_from_storage(storage_context)

    query_engine = recursive_index.as_query_engine(similarity_top_k=25)
    query = """
    This document contains medical record in each page of the document. 
    List the history of Present Illness from the medical prescription in sentences.
    List the medications in bullet points the patient has been taking from the medical prescription.
    List the blood test values that are high and low from all the blood test reports.
    If the document contains a table that describes a blood test value, do not output it as a table, but as a sentence providing that value.
    """

    response = query_engine.query(query)
    return response.response


if __name__ == '__main__':
    r = get_rag_response_from_query()
    print(type(r))
