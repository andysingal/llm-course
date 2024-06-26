from typing import Any

import marvin

from frameworks.base import BaseFramework, experiment


class MarvinFramework(BaseFramework):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        marvin.settings.openai.chat.completions.model = self.llm_model

    def run(
        self, n_runs: int, expected_response: Any, inputs: dict
    ) -> tuple[list[Any], float, float]:
        @experiment(n_runs=n_runs, expected_response=expected_response)
        def run_experiment(inputs):
            response = marvin.cast(self.prompt.format(**inputs), self.response_model)
            return response

        predictions, percent_successful, accuracy = run_experiment(inputs)
        return predictions, percent_successful, accuracy