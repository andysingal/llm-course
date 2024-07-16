import random
from typing import List, Dict

import torch
from torch.utils.data import Dataset
from transformers import AutoTokenizer
from tqdm import tqdm


class ChatDataset(Dataset):
    def __init__(
        self,
        original_records: List[Dict],
        tokenizer: AutoTokenizer,
        max_tokens_count: int,
        sample_rate: float = 1.0,
        only_target_loss: bool = True,
        add_global_bos: bool = True,
        add_global_eos: bool = True,
        labels_pad_token_id: int = -100,
    ):
        self.original_records = original_records
        self.sample_rate = sample_rate
        self.tokenizer = tokenizer
        self.max_tokens_count = max_tokens_count
        self.only_target_loss = only_target_loss
        self.labels_pad_token_id = labels_pad_token_id
        self.add_global_bos = add_global_bos
        self.add_global_eos = add_global_eos
        self.is_printed = False

        self.records = []
        for record in tqdm(original_records):
            if random.random() > self.sample_rate:
                continue
            tensors = self.convert_record(record)
            if tensors is None:
                continue
            self.records.append(tensors)

    def __len__(self):
        return len(self.records)

    def __getitem__(self, index):
        return self.records[index]

    def get_tokens(self, messages):
        tokens = self.tokenizer.apply_chat_template(
            messages,
            add_special_tokens=False,
            tokenize=True,
            add_generation_prompt=False,
        )
        if tokens[0] == self.tokenizer.bos_token_id:
            tokens = tokens[1:]
        return tokens

    def convert_record(self, record):
        input_ids, labels = [], []

        for message in record["messages"]:
            message_input_ids = self.get_tokens([message])
            message_labels = message_input_ids
            if len(input_ids) + len(message_input_ids) > self.max_tokens_count - 2:
                break

            labels_mask = [
                self.labels_pad_token_id for _ in range(len(message_input_ids))
            ]
            if (
                message["role"] not in ("assistant", "bot", "gpt")
                and self.only_target_loss
            ):
                message_labels = labels_mask

            input_ids.extend(message_input_ids)
            labels.extend(message_labels)

        if not input_ids:
            return None

        original_input_ids = self.get_tokens(record["messages"])
        assert input_ids == original_input_ids[: len(input_ids)], f"{input_ids} vs {original_input_ids}"

        if self.add_global_bos and input_ids[0] != self.tokenizer.bos_token_id:
            input_ids.insert(0, self.tokenizer.bos_token_id)
            labels.insert(0, self.labels_pad_token_id)

        if input_ids[-2] == self.tokenizer.eos_token_id:
            input_ids = input_ids[:-1]
            labels = labels[:-1]

        if self.add_global_eos and input_ids[-1] != self.tokenizer.eos_token_id:
            input_ids.append(self.tokenizer.eos_token_id)
            labels.append(self.tokenizer.eos_token_id)

        if not self.is_printed:
            print(input_ids)
            print(labels)
            print(
                "Full prompt:",
                self.tokenizer.decode(input_ids, skip_special_tokens=False),
            )
            self.is_printed = True

        input_ids = torch.LongTensor(input_ids)
        labels = torch.LongTensor(labels)
        attention_mask = input_ids.new_ones(input_ids.size())
        assert (
            input_ids.size(0)
            == labels.size(0)
            == attention_mask.size(0)
            <= self.max_tokens_count
        )
        return {
            "input_ids": input_ids,
            "labels": labels,
            "attention_mask": attention_mask,
        }
