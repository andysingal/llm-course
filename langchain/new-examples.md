```py
from langchain.retrievers.self_query.base import SelfQueryRetriever
from typing import Any, Dict

from typing import Any, Dict


class CustomSelfQueryRetriever(SelfQueryRetriever):
    def _get_docs_with_query(
        self, query: str, search_kwargs: Dict[str, Any]
    ) -> List[Document]:
        """Get docs, adding score information."""
        docs, scores = zip(
            *self.vectorstore.similarity_search_with_score(query, **search_kwargs)
        )
        for doc, score in zip(docs, scores):
            doc.metadata["score"] = score

        return docs

retriever = CustomSelfQueryRetriever.from_llm(
    llm = llm,
    vectorstore = vectorstore,
    document_contents = document_content_description,
    metadata_field_info = metadata_field_info,
    enable_limit=True, 
    search_type = "similarity_score_threshold",
    search_kwargs={"score_threshold": 0.80, "k": 5},
    verbose=True
)


result = retriever.invoke("your query")
```
Source: https://stackoverflow.com/questions/79165072/getting-document-similarity-scores-with-selfqueryretriever-langchain

