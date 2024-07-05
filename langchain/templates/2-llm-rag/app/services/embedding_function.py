from langchain.embeddings.infinity import InfinityEmbeddings


class EmbeddingFunction:
    def __init__(
        self,
        infinity_instance_url: str,
        embedding_model: str = "all-MiniLM-L6-v2",
    ):
        self.embedding_model = embedding_model
        self.ef = InfinityEmbeddings(
            model=self.embedding_model, infinity_api_url=infinity_instance_url
        )

    def __call__(self, input):
        embeddings = self.ef.embed_query(input)
        return embeddings

    # AppEmbeddingFunction' object has no attribute 'embed_documents'
    def embed_documents(self, documents):
        return self.ef.embed_documents(documents)

    # AppEmbeddingFunction' object has no attribute 'embed_query'
    def embed_query(self, text):
        text = self.get_normalized_input_text(text)
        return self.ef.embed_query(text)

    def get_normalized_input_text(
        self, input: str | dict, dict_key: str = "input"
    ) -> str:
        text = ""

        if isinstance(input, str):
            text = input
        elif isinstance(input, dict):
            text = input[dict_key]

        return text

    def get_embedding_dimensions(self) -> int:
        # TODO: don't hardcode / get dynamically?
        mapping = {"all-MiniLM-L6-v2": 384}
        placeholder_dimensions = 0

        try:
            dimensions = mapping[self.embedding_model]
        except:
            dimensions = placeholder_dimensions

        return dimensions
