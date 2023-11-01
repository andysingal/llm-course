from typing import Callable, Optional

from llama_index.utils import globals_helper
from llama_index.schema import MetadataMode

class LimitRetrievedNodesLength:

    def __init__(self, limit: int = 3000, tokenizer: Optional[Callable] = None):
        self._tokenizer = tokenizer or globals_helper.tokenizer
        self.limit = limit

    def postprocess_nodes(self, nodes, query_bundle):
        included_nodes = []
        current_length = 0

        for node in nodes:
            current_length += len(self._tokenizer(node.node.get_content(metadata_mode=MetadataMode.LLM)))
            if current_length > self.limit:
                break
            included_nodes.append(node)

        return included_nodes
