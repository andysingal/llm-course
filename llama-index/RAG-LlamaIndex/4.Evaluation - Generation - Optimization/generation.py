import os
import openai

from llama_index.core import SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.core.llama_dataset.generator import RagDatasetGenerator


openai.api_key = os.environ.get("OPENAI_API_KEY")
MODEL = os.getenv("MODEL", "gpt-4-0125-preview")
print(f"model = {MODEL}")


def get_documents(input_dir):
    documents = SimpleDirectoryReader(input_dir).load_data(show_progress=True)
    return documents


def generate_dataset(documents):
    llm = OpenAI(model=MODEL, temperature=0.1)

    dataset_generator = RagDatasetGenerator.from_documents(
        documents,
        llm=llm,
        num_questions_per_chunk=1,
        show_progress=True,
    )

    rag_dataset = dataset_generator.generate_dataset_from_nodes()
    return rag_dataset


def main():
    input_dir = "./data/source_files/"
    documents = get_documents(input_dir)
    rag_dataset = generate_dataset(documents)
    rag_dataset.save_json("./output/rag_dataset.json")


if __name__ == "__main__":
    main()
