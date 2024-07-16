import json
import random

import mmh3
import fire
from datasets import load_dataset


def compose_sft_dataset(config_path: str, train_path: str, val_path: str):
    with open(config_path) as r:
        config = json.load(r)

    records = []
    dataset_name = config.get("dataset_name", "IlyaGusev/lmsys_clean_ru_preferences")
    revision = config["dataset_revision"]
    for row in load_dataset(dataset_name, split="train", revision=revision):
        max_length_ratio = config.get("max_length_ratio", 2.1)
        max_length_ratio_prob = config.get("max_length_ratio_prob", 0.0)
        if len(str(row["chosen"])) > len(str(row["rejected"])) * max_length_ratio:
            if random.random() > max_length_ratio_prob:
                continue

        sonnet_approved_only = config.get("sonnet_approved_only", False)
        if sonnet_approved_only and not row["sonnet_approved"]:
            continue

        if not row["chosen"][0]["content"].strip():
            continue

        if not row["rejected"][0]["content"].strip():
            continue

        mapping = {"bot": "assistant"}
        for message in row["prompt"]:
            message["role"] = mapping.get(message["role"], message["role"])
        for message in row["chosen"]:
            message["role"] = mapping.get(message["role"], message["role"])
        for message in row["rejected"]:
            message["role"] = mapping.get(message["role"], message["role"])

        records.append(row)

    random.shuffle(records)

    train_records = []
    val_records = []
    for r in records:
        s = str(r["prompt"])
        h = mmh3.hash(s, signed=False)
        if h % 100 < 97:
            train_records.append(r)
        else:
            val_records.append(r)
    with open(train_path, "w") as w:
        for record in train_records:
            w.write(json.dumps(record, ensure_ascii=False).strip() + "\n")
    with open(val_path, "w") as w:
        for record in val_records:
            w.write(json.dumps(record, ensure_ascii=False).strip() + "\n")


if __name__ == "__main__":
    fire.Fire(compose_sft_dataset)
