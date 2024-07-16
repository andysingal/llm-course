import os
import json

import fire
import wandb
import torch
from transformers import DataCollatorForTokenClassification, Trainer
from unsloth import FastLanguageModel, UnslothTrainingArguments
from unsloth.trainer import _create_unsloth_optimizer

from src.dataset import ChatDataset
from src.util.io import read_jsonl

os.environ["TOKENIZERS_PARALLELISM"] = "false"


class CustomTrainer(Trainer):
    def create_optimizer(self):
        embedding_learning_rate = getattr(self.args, "embedding_learning_rate", None)
        if embedding_learning_rate is None:
            return super().create_optimizer()
        if self.optimizer is None:
            optimizer_cls, optimizer_kwargs = Trainer.get_optimizer_cls_and_kwargs(self.args)
            self.optimizer = _create_unsloth_optimizer(
                self.model,
                optimizer_cls,
                optimizer_kwargs,
                embedding_learning_rate,
            )
        return self.optimizer


def train(
    config_path: str,
    train_path: str,
    val_path: str,
    output_dir: str,
    sample_rate: float = 1.0,
):
    with open(config_path) as r:
        config = json.load(r)

    max_tokens_count = config["max_tokens_count"]
    max_seq_length = config.get("max_seq_length", max_tokens_count)
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=config["model_name"],
        max_seq_length=max_seq_length,
        dtype=torch.bfloat16,
        load_in_8bit=config["load_in_8bit"],
        load_in_4bit=config["load_in_4bit"],
        attn_implementation="flash_attention_2",
    )
    tokenizer.bos_token = config["bos_token"]
    tokenizer.eos_token = config["eos_token"]
    tokenizer.pad_token = config["pad_token"]
    tokenizer.padding_side = "left"
    tokenizer.save_pretrained(output_dir)

    lora_config = config.get("lora")
    if lora_config:
        model = FastLanguageModel.get_peft_model(
            model, **config["lora"], max_seq_length=max_seq_length
        )

    train_records = read_jsonl(train_path)
    val_records = read_jsonl(val_path)

    datasets = []
    for records in (train_records, val_records):
        datasets.append(
            ChatDataset(
                records,
                tokenizer,
                max_tokens_count=max_tokens_count,
                sample_rate=sample_rate,
                only_target_loss=config["only_target_loss"],
                add_global_bos=config.get("add_global_bos", True),
                add_global_eos=config.get("add_global_eos", True),
            )
        )
    train_dataset, val_dataset = datasets
    data_collator = DataCollatorForTokenClassification(tokenizer, pad_to_multiple_of=8)

    trainer_config = config["trainer"]
    if trainer_config.get("report_to", "wandb") == "wandb":
        wandb.init(project="rulm_self_instruct", name=config_path)
    trainer = CustomTrainer(
        model=model,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=data_collator,
        args=UnslothTrainingArguments(**trainer_config, output_dir=output_dir),
    )
    trainer.train()
    model.save_pretrained(output_dir)


if __name__ == "__main__":
    fire.Fire(train)
