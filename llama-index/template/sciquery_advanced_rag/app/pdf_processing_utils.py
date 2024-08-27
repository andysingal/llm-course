import os
import re
import json
from typing import List, Dict, Tuple, Optional

import pymupdf
from config import DEBUG

def is_int(s: str) -> bool:
    "Check if the input string can be converted to an integer."
    try:
        int(s)
        return True
    except ValueError:
        return False


def remove_reference(text_blocks: List[str]) -> Tuple[Optional[int], Optional[Dict[str, Dict[str, str]]]]:
    """Remove Reference text blocks from a list of text blocks.

    Returns:
        tuple: Tuple containing the index of the reference block.
    """

    # List of possible reference section headings
    reference_headings = [
        r'^Reference\b', 
        r'^References\b', 
        r'^References:\b'
    ]
    # Compile the regex patterns
    reference_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in reference_headings]

    reference_block_found = False
    # Iterate through blocks and find the starting index of reference section
    for i, block in enumerate(text_blocks):
        for pattern in reference_patterns:
            if pattern.search(block):
                reference_block_found = True
                break
        if reference_block_found:
            block_idx = i
            break

    if not reference_block_found:
        return None
    else:
        return block_idx


def get_page_text(pdf_path: str, fn:str ) -> Tuple[List[str], Optional[Dict[str, Dict[str, str]]], Optional[Dict[str, str]]]:
    "Extract text sections from a PDF document, process them, and return each page and file metadata."
    doc = pymupdf.open(pdf_path)
    pages = []
    for page_number,page in enumerate(doc): # iterate the document pages
        metadata = {"file_name":fn, "page_num":page_number+1, "title":doc.metadata["title"], "pdf_path": pdf_path}
        processed_page_blocks = [""]
        blocks = page.get_text('blocks',flags=16)
        tabs = page.find_tables()  # detect the tables

        for block in blocks:
            if block[6] != 1: #ignore image blocks
                text_bbox = pymupdf.Rect(block[:4]) #bounding box of a text block

                intersect_with_table = False
                for tab in tabs:
                    table_bbox = pymupdf.Rect(tab.bbox) #bounding box of a table
                    if table_bbox.intersects(text_bbox):
                            intersect_with_table = True
                            break
                
                txt = block[4].replace("\n"," ")
                txt = txt.strip()        
                if intersect_with_table:
                    table_txt = block[4].replace('\n','* ').strip()
                    if table_txt == "* ".join([ x if x is not None else '' for x in tab.header.names]).strip(): #First heading cell
                        processed_page_blocks.append(f'Header: {table_txt} ')
                    else: #other concat to previous block
                        processed_page_blocks[len(processed_page_blocks)-1] += f'Cell: {table_txt} '
                elif len(txt.replace('\n',' ')) != 0 and not is_int(txt):
                    processed_page_blocks.append(txt)
            
        ref_block_idx = remove_reference(processed_page_blocks)
        if ref_block_idx:
            processed_page_blocks = processed_page_blocks[:ref_block_idx]
        
        blocks_ = [""]
        for txt in processed_page_blocks:
            if txt and (txt[0].islower() or not txt[0].isalnum()):
                blocks_[len(blocks_)-1] += f' {txt}' # No new line because most likely this block is part of previous passage
            elif txt:
                blocks_[len(blocks_)-1] += f'\n{txt}' # new line because most likely a new passage.
        pages.append({"text":"\n".join(blocks_),"metadata":metadata})
    return pages


def display_chunk(chunks: List[str]) -> None:
    "Display chunks"
    for i, chunk in enumerate(chunks):
        chunk = chunk["passage"]
        count = len(chunk.split())
        print(f"Chunk {i + 1} (Words: {count}):")
        print(chunk)
        print("-" * 50)
