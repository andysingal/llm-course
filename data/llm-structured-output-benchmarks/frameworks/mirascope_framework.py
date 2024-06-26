import re
from typing import Any, Type

from mirascope.openai import OpenAIExtractor
from pydantic import create_model

from frameworks.base import BaseFramework, experiment


class MirascopeFramework(BaseFramework):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Identify all the input fields in the prompt and create the pydantic model
        prompt_fields = re.findall(r"\{(.*?)\}", self.prompt)
        mirascope_pydantic_fields = {field: (str, "") for field in prompt_fields}
        mirascope_pydantic_fields["extract_schema"] = (Type[self.response_model], self.response_model)
        mirascope_pydantic_fields["prompt_template"] = (str, self.prompt)

        # Mirascope TaskExtractor model
        # TODO: Swap the Extractor based on self.llm_model
        TaskExtractor = create_model(
            "TaskExtractor",
            __base__=OpenAIExtractor[self.response_model],
            **mirascope_pydantic_fields
        )

        self.mirascope_client = TaskExtractor()

    def run(
        self, n_runs: int, expected_response: Any, inputs: dict
    ) -> tuple[list[Any], float, float]:
        @experiment(n_runs=n_runs, expected_response=expected_response)
        def run_experiment(inputs):
            # Pass the inputs to the mirascope TaskExtractor
            for field, value in inputs.items():
                setattr(self.mirascope_client, field, value)

            response = self.mirascope_client.extract(retries=2)
            return response

        predictions, percent_successful, accuracy = run_experiment(inputs)
        return predictions, percent_successful, accuracy
