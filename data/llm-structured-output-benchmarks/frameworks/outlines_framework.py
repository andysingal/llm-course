from typing import Any

import outlines

from frameworks.base import BaseFramework, experiment


class OutlinesFramework(BaseFramework):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # TODO: Handle openai model
        if self.llm_model_family == "transformers":
            outlines_model = outlines.models.transformers(
                self.llm_model, device=self.device
            )
        else:
            raise ValueError(f"Model family: {self.llm_model_family} not supported")

        self.outline_generator = outlines.generate.json(
            outlines_model, self.response_model
        )

    def run(
        self, n_runs: int, expected_response: Any, inputs: dict
    ) -> tuple[list[Any], float, float]:
        @experiment(n_runs=n_runs, expected_response=expected_response)
        def run_experiment(inputs):
            response = self.outline_generator(self.prompt.format(**inputs))
            return response

        predictions, percent_successful, accuracy = run_experiment(inputs)
        return predictions, percent_successful, accuracy
