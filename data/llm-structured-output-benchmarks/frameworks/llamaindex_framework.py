from typing import Any

from llama_index.program.openai import OpenAIPydanticProgram

from frameworks.base import BaseFramework, experiment


class LlamaIndexFramework(BaseFramework):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # TODO: Swap the Program based on self.llm_model
        self.llamaindex_client = OpenAIPydanticProgram.from_defaults(
            output_cls=self.response_model,
            prompt_template_str=self.prompt,
            llm_model=self.llm_model,
        )

    def run(
        self, n_runs: int, expected_response: Any, inputs: dict
    ) -> tuple[list[Any], float, float]:
        @experiment(n_runs=n_runs, expected_response=expected_response)
        def run_experiment(inputs):
            response = self.llamaindex_client(**inputs, description="Data model of items present in the text")
            return response

        predictions, percent_successful, accuracy = run_experiment(inputs)
        return predictions, percent_successful, accuracy
