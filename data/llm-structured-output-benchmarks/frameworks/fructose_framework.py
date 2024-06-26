import re
from typing import Any

from fructose import Fructose
from loguru import logger

from data_sources.data_models import pydantic_to_dataclass
from frameworks.base import BaseFramework, experiment


class FructoseFramework(BaseFramework):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.fructose_client = Fructose(model=self.llm_model)

        # Convert Pydantic model to dataclass for Fructose
        self.response_model = pydantic_to_dataclass(self.response_model)

    def run(
        self, n_runs: int, expected_response: Any, inputs: dict
    ) -> tuple[list[Any], float, float]:
        prompt_fields = re.findall(r"\{(.*?)\}", self.prompt)

        if len(prompt_fields) > 1:
            raise ValueError(
                "Fructose only supports a single input field in the prompt. Please update the prompt to have only one field within curly brackets: { }"
            )

        @experiment(n_runs=n_runs, expected_response=expected_response)
        @self.fructose_client
        def run_experiment(text: str) -> self.response_model: ...

        # Fructose prompt is passed into the function docstring
        docstring_args = f"""\n\nArgs:\n    text (str): The text to analyze\n\nReturns:\n    {self.response_model.__qualname__}: The items present in the text"""
        run_experiment.__doc__ = self.prompt + docstring_args

        predictions, percent_successful, accuracy = run_experiment(
            text=inputs[prompt_fields[0]]
        )

        return predictions, percent_successful, accuracy
