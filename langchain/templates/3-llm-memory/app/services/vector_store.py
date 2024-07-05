import uuid
from typing import Dict, List

from langchain_core.documents import Document

from opensearchpy import OpenSearch

from services.data_loader import DataLoader
from services.embedding_function import EmbeddingFunction


class VectorStore:
    def __init__(
        self,
        search_hostname: str,
        search_port: str,
        search_auth: tuple,
        content_dir: str,
        embedding_function: EmbeddingFunction,
    ):
        self.content_dir = content_dir
        self.data_loader = DataLoader(content_dir)
        self.embedding_function = embedding_function

        self.search_client = OpenSearch(
            hosts=[{"host": search_hostname, "port": search_port}],
            http_auth=search_auth,
            use_ssl=True,
            verify_certs=False,
        )

        self.index_name = "chat_documents"
        self.index_settings = {
            "settings": {"index": {"number_of_shards": 4}, "index.knn": True},
            "mappings": {
                "properties": {
                    "embeddings": {
                        "type": "knn_vector",
                        "dimension": self.embedding_function.get_embedding_dimensions(),
                    },
                }
            },
        }

        self.ensure_index_exists()

        self.search_pipeline_name = "nlp-search-pipeline"
        self.search_pipeline_settings = {
            "description": "Post processor for hybrid search (combine keyword and vector)",
            "phase_results_processors": [
                {
                    "normalization-processor": {
                        "normalization": {"technique": "min_max"},
                        "combination": {
                            "technique": "arithmetic_mean",
                            "parameters": {"weights": [0.3, 0.7]},
                        },
                    }
                }
            ],
        }

        self.ensure_search_pipeline_exists()

        self.default_search_query_body = {
            "_source": False,
            "fields": ["page_content", "metadata.source"],
        }

    ########
    # Setup
    ########
    def ensure_index_exists(self) -> None:
        try:
            self.search_client.indices.get(self.index_name)
        except:
            self.refresh_index()

    def refresh_index(self) -> None:
        try:
            self.search_client.indices.delete(self.index_name)
        except:
            do_nothing = None

        self.search_client.indices.create(self.index_name, body=self.index_settings)
        self.load_documents_from_disk_into_index()

    def ensure_search_pipeline_exists(self) -> None:
        # TODO: redo when https://github.com/opensearch-project/opensearch-py/issues/474 lands
        try:
            self.search_client.http.get(
                f"/_search/pipeline/{self.search_pipeline_name}"
            )
        except:
            self.refresh_search_pipeline()

    def refresh_search_pipeline(self) -> None:
        try:
            self.search_client.http.delete(
                f"/_search/pipeline/{self.search_pipeline_name}"
            )
        except:
            do_nothing = None

        self.search_client.http.put(
            f"/_search/pipeline/{self.search_pipeline_name}",
            body=self.search_pipeline_settings,
        )

    ########
    # Loader
    ########
    def load_documents_from_disk_into_index(self) -> None:
        documents = self.data_loader.load_documents_from_disk()
        self.load_documents_into_index(documents)

    def load_documents_into_index(self, documents: List[Document]) -> None:
        for document in documents:
            # Todo: use bulk upload
            search_body = document.dict()
            search_body["embedding_model"] = self.embedding_function.embedding_model
            search_body["embeddings"] = self.embedding_function(document.page_content)

            self.search_client.index(
                index=self.index_name,
                body=search_body,
                id=str(uuid.uuid1()),
                refresh=True,
            )

    def add_document(self, title: str, body: str) -> None:
        document_file_path = self.data_loader.save_document_to_disk(title, body)
        self.load_document_into_index(document_file_path)

    def load_document_into_index(self, document_file_path: str) -> None:
        documents = self.data_loader.load_document_from_disk(document_file_path)
        self.load_documents_into_index(documents)

    ########
    # Search
    ########
    def query(self, text: str, size: int = 3) -> List:
        return self.hybrid_query(text=text, size=size)

    def hybrid_query(self, text: str, size: int = 3) -> List:
        query_embeddings = self.embedding_function.embed_query(text)

        params = {"search_pipeline": self.search_pipeline_name}

        search_query = self.default_search_query_body.copy()
        search_query["size"] = size
        search_query["query"] = {
            "hybrid": {
                "queries": [
                    {"match": {"page_content": {"query": text}}},
                    {
                        "knn": {
                            "embeddings": {
                                "vector": query_embeddings,
                                "k": size,
                            }
                        }
                    },
                ]
            }
        }

        results = self.search_client.search(
            index=self.index_name, body=search_query, params=params
        )

        results = results["hits"]["hits"]

        return results

    def keyword_query(self, text: str, size: int = 3) -> List:
        search_query = self.default_search_query_body.copy()
        search_query["size"] = size
        search_query["query"] = {"match": {"page_content": {"query": text}}}

        results = self.search_client.search(index=self.index_name, body=search_query)
        results = results["hits"]["hits"]

        return results

    def vector_query(self, text: str, size: int = 3) -> List:
        query_embeddings = self.embedding_function.embed_query(text)

        search_query = self.default_search_query_body.copy()
        search_query["size"] = size
        search_query["query"] = {
            "knn": {
                "embeddings": {
                    "vector": query_embeddings,
                    "k": size,
                }
            }
        }

        results = self.search_client.search(index=self.index_name, body=search_query)
        results = results["hits"]["hits"]

        return results

    def find_document(self, query: str) -> Dict:
        search_query = self.default_search_query_body.copy()
        search_query["size"] = 1
        # TODO: don't use wildcard, use tokenizer
        search_query["query"] = {"wildcard": {"metadata.source": f"*{query}*"}}

        results = self.search_client.search(index=self.index_name, body=search_query)
        result = {}

        if results["hits"]["hits"]:
            result = {
                "source": results["hits"]["hits"][0]["fields"]["metadata.source"][0],
                "page_content": results["hits"]["hits"][0]["fields"]["page_content"][0],
            }

        return result
