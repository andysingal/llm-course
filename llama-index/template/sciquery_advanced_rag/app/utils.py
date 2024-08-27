import os
import json
import uuid
from glob import glob
from typing import Tuple, List, Dict, Optional, Union, Callable
from functools import partial
import re

import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder
from sentence_transformers.util import cos_sim
import transformers
import torch


from app.pdf_processing_utils import get_sections, chunk_texts, manage_bib_json, display_chunk
from config import (EMBEDDING_MODEL_PATH, 
                    PDF_DATA_DIR, 
                    INDEX_AND_BIB_DIR, 
                    BIB_JSON_NAME, 
                    INDEX_ARRAY_NAME,
                    DEBUG,
                    DEVICE,

                    GENERATION_KWARGS,
                    MAX_TOKENS,
                    RERANKER_MODEL_PATH,
                    TOP_K_RETRIEVED,
                    TOP_K_RANKED)


def get_relevant_chunks_idx(query_embedding: np.ndarray, doc_embeddings: np.ndarray, top: int=3) -> Tuple[List[int],List[float]]:
    """ Query the index with cosine similarity """
    similarities = cos_sim(query_embedding, doc_embeddings)[0]
    most_relevant_idx = similarities.argsort(descending=True)[:top]
    return most_relevant_idx, similarities[most_relevant_idx]


def load_generation_pipeline() -> Union[transformers.pipelines.text_generation.TextGenerationPipeline, Callable]:
    "Load Text Generation Pipeline based on Device Type"
    if DEVICE != "MPS":
        pipeline = transformers.pipeline(
            "text-generation",
            model=LLAMA_MODEL_PATH,
            model_kwargs={
                "torch_dtype": torch.bfloat16,
                "quantization_config": {"load_in_4bit": True},
                "low_cpu_mem_usage": True,
                },
                )
    else:
        from mlx_lm import load, generate
        model, tokenizer = load(LLAMA_MODEL_PATH_MLX)
        pipeline = partial(generate,model,tokenizer)
    return pipeline


def generator_answer(prompt: str, answer_generator: Callable) -> str:
    """Generate an answer based on the given prompt using the provided answer generator.

    Args:
        prompt (str): The input prompt to generate an answer for.
        answer_generator (Callable): The text generation pipeline or callable for generating answers.
    """
    def parse(string: str) -> str:
       return string.split("<|end_header_id|>")[-1]

    if DEVICE != "MPS":
        outputs = answer_generator(prompt,m=MAX_TOKENS,**GENERATION_KWARGS)
        return outputs[0]["generated_text"][-1]
    else:
        kwargs = {"temp": GENERATION_KWARGS["temperature"],
                #   "repetition_penalty": None,
                #   "repetition_context_size": 20,
                  "top_p": GENERATION_KWARGS["top_p"]}
        return parse(answer_generator(prompt=prompt,max_tokens=MAX_TOKENS,**kwargs))


def load_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(EMBEDDING_MODEL_PATH)


def load_reranker_model() -> CrossEncoder:
    return CrossEncoder(RERANKER_MODEL_PATH)


def should_create_index_and_bib() -> bool:
    "Check if the index and bibliographies files need to be created."
    bibliographies_path = os.path.join(INDEX_AND_BIB_DIR, BIB_JSON_NAME)
    chunk_data_path = os.path.join(INDEX_AND_BIB_DIR, INDEX_ARRAY_NAME)
    return not (os.path.isfile(bibliographies_path) and os.path.isfile(chunk_data_path))


def process_single_pdf(pdf_path: str, embedding_model: SentenceTransformer) -> List[Dict]:
    unique_string = str(uuid.uuid4())
    sections, bibliography_dict, file_metadata = get_sections(pdf_path)
    file_metadata["uuid"] = unique_string

    #prepare chunks
    chunked_texts = chunk_texts(sections,file_metadata)

    if DEBUG:
        print(f'{"==="*5} Display chunks for file {pdf_path} {"==="*5}')
        display_chunk(chunked_texts)
    
    #save bibliographies
    if bibliography_dict is not None and len(bibliography_dict) > 0:
        operations = {"add_or_update": {file_metadata["pdf_path"]: bibliography_dict}}
        manage_bib_json(os.path.join(INDEX_AND_BIB_DIR, BIB_JSON_NAME), operations)
    
    # Get embedding for each passage/sections and save it in same dict
    for item in chunked_texts:
        item["vector"] = embedding_model.encode(item["passage"], convert_to_numpy=True)
    return chunked_texts


def prepare_index_and_bib(embedding_model: SentenceTransformer) -> Tuple[List, np.ndarray, Dict]:
    "Prepare the index and bibliographies by processing PDF files, chunking text, and saving embeddings and return index and bib files"
    indexed_chunks = []
    try:
        pattern = os.path.join(PDF_DATA_DIR, '*.pdf')
        pdf_files = glob(pattern)

        if DEBUG:
            pdf_files = pdf_files[:3]
        
        for pdf in pdf_files:
            indexed_chunks.extend(process_single_pdf(pdf, embedding_model))

        # Save embeddings and text data as an numpy arrary
        np.save(os.path.join(INDEX_AND_BIB_DIR, INDEX_ARRAY_NAME), indexed_chunks)
        return load_index_and_bib()
    except Exception as e:
        print(f"An error occurred while creating index and Bib file: {e}")


def save_index_and_bib(indexed_chunks: List, bibliography_dict: Optional[Dict] = None) -> np.ndarray:
    "Save the index and bibliographies."
    try:
        np.save(os.path.join(INDEX_AND_BIB_DIR, INDEX_ARRAY_NAME), indexed_chunks)
        document_embeddings = np.array([data["vector"] for data in indexed_chunks])
        print(f'{"==="*5} Saving Embedding size is {document_embeddings.shape} {"==="*5}')
        
        if bibliography_dict:
            # Save the updated data back to the JSON file
            with open(os.path.join(INDEX_AND_BIB_DIR, BIB_JSON_NAME), 'w') as file:
                json.dump(bibliography_dict, file, indent=4)
            print(f'{"==="*5} Saved Bib dict with {len([v is not None and len(v) > 0 for _,v in bibliography_dict.items()])} bibliography {"==="*5}')

        return document_embeddings
    except Exception as e:
        print(f"An error occurred while saving index and Bib file: {e}")


def load_index_and_bib() -> Tuple[List, np.ndarray, Dict]:
    "Load the index and bibliographies from saved files."
    try:
        indexed_chunks = np.load(os.path.join(INDEX_AND_BIB_DIR, INDEX_ARRAY_NAME), allow_pickle=True)
        document_embeddings = np.array([data["vector"] for data in indexed_chunks])
        print(f'{"==="*5} Loaded Embedding size is {document_embeddings.shape} {"==="*5}')
        
        # Load the existing bibliograph data
        with open(os.path.join(INDEX_AND_BIB_DIR, BIB_JSON_NAME), 'r') as file:
            bibliography_dict = json.load(file)
        print(f'{"==="*5} Loaded Bib dict with {len([v is not None and len(v) > 0 for k,v in bibliography_dict.items()])} bibliography {"==="*5}')

        return indexed_chunks, document_embeddings, bibliography_dict
    except Exception as e:
        print(f"An error occurred while loading index and Bib file: {e}")


def identify_num_citation(text: str) -> str:
    "Identify number citation in the given text and return list of all unique number"
    
    citation_numbers = []
    pattern = r'\[\d+(?:-\d+)?(?:, \d+)*\]'
    matches = re.findall(pattern, text)
    
    for match in matches:
        # Remove square brackets
        match = match[1:-1]    
        # Split by comma to handle multiple numbers
        parts = match.split(', ')
        
        for part in parts:
            # Check if the part contains a range
            if '-' in part:
                start, end = map(int, part.split('-'))
                citation_numbers.extend(range(start, end + 1))
            else:
                citation_numbers.append(int(part))
    unique_num = list(set(citation_numbers))
    return [f'[{num}]' for num in unique_num]


def remove_num_bracket(text: str) -> str:
    "Remove brackets around number, this helps in identifying the author citation"
    pattern = r'\((\d\S*)\)'#pattern to match (number)
    def replacer(match):
        return match.group(1)
    # Replace all occurrences of the pattern in the passage
    return re.sub(pattern, replacer, text)


def identify_author_citations(text: str) -> str:
    """ 
    Identify all author citation in the given text and return list of all unique authors
    
    Regex to match a string of text within parentheses that includes author names followed by a 
    year (with optional letters) and optionally multiple such citations separated by semicolons.
    """
    text = remove_num_bracket(text)

    pattern = r'\(([^()]+? \d{4}[a-z]?(?:; [^()]+? \d{4}[a-z]?)*?)\)' #generated using claude

    citations = re.findall(pattern, text)
    all_citations = []
    for citation in citations:
        all_citations.extend( map(str.strip, citation.split(';')) )
    return list(set(all_citations))


def get_citation_data(text: str, pdf_path: str, bibliography_dict: Dict) -> List[Union[str,Dict]]:
    "Extract citation information from a given text passage. It citiation style is NeurIPS then also return Metadata"
    num_citation = identify_num_citation(text)
    if len(num_citation) > 0:
        bib = bibliography_dict.get(pdf_path,None)
        if bib:
            filtered_bib = {}
            for num in num_citation:
                filtered_bib[num] = bib.get(num,'')
            return [filtered_bib]
        return []
    else:
        author_citation =  identify_author_citations(text)
        return author_citation if len(author_citation) > 0 else []


def get_metadata_and_relevant_passages(
        query: str,
        indexed_chunks: List,
        embedding_model: SentenceTransformer,
        document_embedding: np.ndarray,
        reranker_model: CrossEncoder,
        bibliography_dict: Dict
        ) -> Tuple[List[Dict], List[str]]:
    "Retrieved TOP_K_RETRIEVED relevant chunks/passages for the given query, ReRank them and choose TOP_K_RANKED chunks." 
    reranker_query = query
    if 'mixedbread' in EMBEDDING_MODEL_PATH:
        query = f'Represent this sentence for searching relevant passages: {query}'

    query_embedding = embedding_model.encode([query], convert_to_numpy=True)
    idxs, sims  =  get_relevant_chunks_idx(query_embedding, document_embedding, top=TOP_K_RETRIEVED)
    print(f'Index Id for top {TOP_K_RETRIEVED} relevant chunks for this query are {idxs} with their similarities {sims}')

    metadata = []
    relevant_passages = []
    for idx in idxs:
        chunk = indexed_chunks[idx]
        pdf_path = chunk["file_metadata"]["pdf_path"]
        passage = chunk["passage"]
        metadata.append(
            {"passage":passage,
             "pdf_path":pdf_path,
             "citations": get_citation_data(passage,pdf_path,bibliography_dict)
             })
        relevant_passages.append(chunk["passage"])

    ranked_result = reranker_model.rank(reranker_query, relevant_passages, return_documents=True, top_k=TOP_K_RANKED)

    metadata_ = []
    passages = []
    for i,r in enumerate(ranked_result):
        corpus_id = r['corpus_id']
        score = r['score']
        print(f'Document {corpus_id+1} ranked {i+1} with score {score}')
        metadata_.append(metadata[corpus_id])
        passages.append(relevant_passages[corpus_id])
    return metadata_, passages


def prepare_rag_prompt(query: str, passages: List[str]) -> str:
    "Prepare RAG Prompt using context and query. Concat all passsage together and add it as a context."
    context = "\n\n".join(passages)
    prompt = f"""
    <|begin_of_text|>
    <|start_header_id|>
        system
    <|end_header_id|>
        You are an AI assistant tasked with answering questions based on provided context.
        Your goal is to provide accurate, relevant, and concise responses using only the information given in the context.
        If the context doesn't contain enough information to answer the question fully, state that clearly. 
        Do not make up or infer information beyond what's explicitly stated in the context.

        [INSTRUCTIONS]
        1. Carefully read the provided context and query.
        2. Analyze the information in the context that is relevant to the query.
        3. Formulate a clear and concise answer based solely on the given context.
        4. If the context doesn't provide sufficient information to answer the query, state this explicitly.
        5. Do not include any information that is not present in the given context.
    <|eot_id|>
    <|start_header_id|>
        user
    <|end_header_id|>
    Answer the user question based on the context provided below

    [CONTEXT]
    {context}

    [QUERY]
    {query}
    <|eot_id|>
    <|start_header_id|>
        assistant
    <|end_header_id|>
    """
    return prompt.strip()

