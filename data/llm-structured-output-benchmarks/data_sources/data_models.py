import dataclasses
from enum import Enum
from typing import Any, Type

from pydantic import BaseModel
from pydantic_core import PydanticUndefined


# Multilabel classification model
def multilabel_classification_model(multilabel_classes):
    class MultiLabelClassification(BaseModel):
        classes: list[
            Enum("MultilabelClasses", {name: name for name in multilabel_classes})
        ]

    return MultiLabelClassification


def pydantic_to_dataclass(
    klass: Type[BaseModel],
    classname: str = None,
) -> Any:
    """
    Dataclass from Pydantic model

    Transferred entities:
        * Field names
        * Type annotations, except of Annotated etc
        * Default factory or default value

    Validators are not transferred.

    Order of fields may change due to dataclass's positional arguments.

    """
    # https://stackoverflow.com/questions/78327471/how-to-convert-pydantic-model-to-python-dataclass
    dataclass_args = []
    for name, info in klass.model_fields.items():
        if info.default_factory is not None:
            dataclass_field = dataclasses.field(
                default_factory=info.default_factory,
            )
            dataclass_arg = (name, info.annotation, dataclass_field)
        elif info.default is not PydanticUndefined:
            dataclass_field = dataclasses.field(
                default=info.get_default(),
            )
            dataclass_arg = (name, info.annotation, dataclass_field)
        else:
            dataclass_arg = (name, info.annotation)
        dataclass_args.append(dataclass_arg)
    dataclass_args.sort(key=lambda arg: len(arg) > 2)
    return dataclasses.make_dataclass(
        classname or f"{klass.__name__}",
        dataclass_args,
    )
