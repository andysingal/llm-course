# python -m data_sources.generate_dataset generate-multilabel-data
import random
from collections import Counter
from typing import List

import pandas as pd
import typer
from datasets import load_dataset
from loguru import logger
from rich.progress import track

app = typer.Typer()


def download_default_dataset(text_column: str = "utt", label_column: str = "intent"):
    logger.info(
        "Downloading source data from https://huggingface.co/datasets/AmazonScience/massive"
    )
    dataset = load_dataset("AmazonScience/massive", "en-US", split="test")
    dataset = dataset.select_columns([text_column, label_column])

    logger.info("Processing the text and label columns")
    dataset = dataset.rename_columns({text_column: "text", label_column: "class_label"})
    class_names = dataset.features["class_label"].names

    dataset = dataset.map(
        lambda row: {"label": class_names[row["class_label"]]},
        remove_columns=["class_label"],
    )

    return dataset.to_pandas()


@app.command()
def generate_multilabel_data(
    source_data_pickle_path: str = None,
    source_dataframe_text_column: str = "text",
    source_dataframe_label_column: str = "label",
    dest_num_rows: int = 100,
    dest_num_labels_per_row: List[int] = [1, 2, 3, 4],
    weights_num_labels_per_row: List[float] = [0.35, 0.3, 0.2, 0.15],
):
    if not source_data_pickle_path:
        logger.info("No source data pickle file provided, downloading default dataset")
        source_dataframe = download_default_dataset()
    else:
        logger.info("Loading the source data from the provided pickle file")
        source_dataframe = pd.read_pickle(source_data_pickle_path)

    logger.info(f"Generating {dest_num_rows} synthetic rows")

    multilabel_data = {"text": [], "labels": []}
    for _ in track(range(dest_num_rows), description="Generating rows"):
        num_rows = random.choices(dest_num_labels_per_row, weights_num_labels_per_row)[
            0
        ]
        random_rows = source_dataframe.sample(num_rows)

        multilabel_data["text"].append(
            ". ".join(random_rows[source_dataframe_text_column].tolist())
        )
        multilabel_data["labels"].append(
            random_rows[source_dataframe_label_column].tolist()
        )

    multilabel_df = pd.DataFrame(multilabel_data)

    logger.info(f"First 5 rows:\n{multilabel_df.head()}")

    label_counter = Counter([len(label) for label in multilabel_df["labels"]])
    label_counter = pd.DataFrame.from_records(
        list(label_counter.items()), columns=["num_labels", "num_rows"]
    ).sort_values("num_labels")

    logger.info(f"Number of rows for each number of labels:\n{label_counter.head()}")

    multilabel_df.to_pickle("data/multilabel_classification.pkl")
    logger.info("Saved multilabel data to: data/multilabel_classification.pkl")


@app.command()
def generate_ner_data():
    pass

if __name__ == "__main__":
    app()
