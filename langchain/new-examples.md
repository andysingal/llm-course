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

## Hashtag generator

<img width="537" alt="Screenshot 2025-04-21 at 8 07 12 AM" src="https://github.com/user-attachments/assets/4bc5ca6f-2e64-417a-82ac-b01de5efff9b" />

<img width="503" alt="Screenshot 2025-04-21 at 8 07 38 AM" src="https://github.com/user-attachments/assets/21889739-3032-4ac7-9ce3-272969546164" />

## Automate Employee FAQs with Vector Search!

<img width="451" alt="Screenshot 2025-04-27 at 10 00 01 AM" src="https://github.com/user-attachments/assets/f89f7e6e-6aad-43ed-98ab-7e5d9163399e" />

### EXAMPLES
- [Building a Writing Assistant with LangChain and Qwen-2.5-32B](https://www.analyticsvidhya.com/blog/2025/03/writing-assistant/)

