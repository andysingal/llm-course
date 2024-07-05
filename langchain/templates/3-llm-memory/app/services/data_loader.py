from typing import List

from langchain_core.documents import Document

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from services.fs_utils import save_document_to_disk


class DataLoader:
    def __init__(self, content_dir: str):
        self.content_dir = content_dir
        self.directory_loader = DirectoryLoader(self.content_dir, glob="**/*.txt")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=2
        )

    def load_documents_from_disk(self) -> List[Document]:
        documents = self.directory_loader.load()
        documents = self.text_splitter.split_documents(documents)

        return documents

    def load_document_from_disk(self, document_file_path: str) -> List[Document]:
        text_loader = TextLoader(document_file_path)
        document = text_loader.load()
        documents = self.text_splitter.split_documents(document)

        return documents

    def save_document_to_disk(self, title: str, body: str) -> str:
        document_file_path = save_document_to_disk(
            directory_path=self.content_dir, title=title, body=body
        )

        return document_file_path
