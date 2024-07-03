# This script processes Google Keep documents exported from Google Keep as JSON to use in vector embeddings
import os
import json
from datetime import datetime, timezone

def save_to_text_doc(processed_doc, doc_name, output_dir):
    # Create new .txt file document
    with open(f"{output_dir}/{doc_name}.txt", 'w') as currDoc:
        currDoc.write(processed_doc)
    
def process_document(doc, output_dir):
    # Set tags to journal, since all documents should be journal entries
    tags = "Journal"
    # Convert UTC time included in json to date
    date = datetime.fromtimestamp(doc['createdTimestampUsec'] / 1e6, tz=timezone.utc).strftime('%Y-%m-%d')
    # Extract text content of document
    processed_doc = doc['textContent']
    # Format doc name
    doc_name = f"Date - {date} Tags - {tags}"
    # Save formatted document to text file
    save_to_text_doc(processed_doc, doc_name, output_dir)
    print("Saved ", doc_name)

# Configure input dir of json files from Google Keep and output dir
input_dir = "google_keep_json"
output_dir = "../../exampledocuments"

# Process all files in input_dir
files = os.listdir(input_dir)
for file in files:
    # Only open .json
    if file.endswith('.json'):
        with open(f"{input_dir}/{file}", 'r') as currDoc:
            doc = json.load(currDoc)
            process_document(doc, output_dir)

