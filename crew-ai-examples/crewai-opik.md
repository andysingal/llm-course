```py
from crewai.utilities.events import (
    TaskCompletedEvent,
)
from crewai.utilities.events.base_event_listener import BaseEventListener
from crewai.task import Task
from crewai.utilities.evaluators.task_evaluator import TaskEvaluator
from crewai.utilities.events.crewai_event_bus import CrewAIEventsBus
from opik.evaluation.metrics import Hallucination


class EvalListenerSetup(BaseEventListener):
    def __init__(self):
        super().__init__()

    def setup_listeners(self, crewai_event_bus: CrewAIEventsBus):
        @crewai_event_bus.on(TaskCompletedEvent)
        def on_task_completed(source: Task, event: TaskCompletedEvent):
            if source.name == "conflicts_of_interest_task":
                evaluator = TaskEvaluator(source.agent)
                evaluation = evaluator.evaluate(source, event.output)
                hallucination_eval = Hallucination()
                hallucination_result = hallucination_eval.score(
                    input=source.prompt() + "\n\n" + source.prompt_context,
                    output=event.output,
                )
                print("evaluation", evaluation.quality)
                print("evaluation", evaluation.suggestions)
                print("------")
                print(hallucination_result.value)
                print(hallucination_result.reason)
```
