```py
import time
from collections import defaultdict

from langchain_core.callbacks import BaseCallbackHandler
from typing import List, Dict, Any, Optional
from uuid import UUID

from langchain_core.documents import Document


class MyCallback(BaseCallbackHandler):

    def __init__(self):
        super().__init__()

        # unix time
        self._start_times: dict[str, float] = {}
        # end unix time
        self._times_to_complete: dict[str, list[float]] = defaultdict(list)
        self._repr_stack = []


    def on_chain_start(
            self,
            serialized: Dict[str, Any],
            inputs: Dict[str, Any],
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            tags: Optional[List[str]] = None,
            metadata: Optional[Dict[str, Any]] = None,
            **kwargs: Any,
    ) -> Any:
        print(f"on_chain_start, run_id: {run_id}")

    def on_chain_end(
            self,
            outputs: Dict[str, Any],
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            **kwargs: Any,
    ) -> Any:
        print(f"on_chain_end, run_id: {run_id}")

    def on_retriever_start(
            self,
            serialized: Dict[str, Any],
            query: str,
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            tags: Optional[List[str]] = None,
            metadata: Optional[Dict[str, Any]] = None,
            **kwargs: Any,
    ) -> Any:
        repl = serialized["repr"]
        assert repl not in self._start_times, f"already started: {repl}"
        start_time = time.time()
        self._start_times[repl] = start_time
        # print(f"on_retriever_start, run_id: {run_id}, repr: {repl}")
        self._repr_stack.append(repl)


    def on_retriever_end(
            self,
            retrieval_results: List[Document],
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            **kwargs: Any,
    ) -> Any:
        # repl = serialized["repr"]
        repl = self._repr_stack.pop()
        assert repl in self._start_times, f"not started: {repl}"
        end_time = time.time()
        time_to_complete = end_time - self._start_times[repl]

        self._times_to_complete[repl].append(time_to_complete)
        # print(f"on_retriever_end, run_id: {run_id}, repr: {repl}, time_to_complete: {time_to_complete:.06f}")
        del self._start_times[repl]

def refreshed_config():
    return {
        "callbacks": [MyCallback()],
    }


my_callback = MyCallback()

config = {
    "callbacks": [my_callback],
}
sample_retrieve = retriever.invoke("test", config=config)
```
