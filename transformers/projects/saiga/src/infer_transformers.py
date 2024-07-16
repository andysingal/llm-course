from typing import List
import copy
import json
from tqdm import tqdm

import fire
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

from src.util.io import read_jsonl
from src.util.dl import gen_batch


def generate(
    model: AutoModelForCausalLM,
    tokenizer: AutoTokenizer,
    prompts: List[str],
    generation_config: GenerationConfig,
    source_max_length: int = 6160,
):
    data = tokenizer(
        prompts,
        return_tensors="pt",
        truncation=True,
        max_length=source_max_length,
        padding=True,
        add_special_tokens=False
    )
    assert data["input_ids"][0][0] != data["input_ids"][0][1]
    data = {k: v.to(model.device) for k, v in data.items()}
    output_ids = model.generate(
        **data,
        generation_config=generation_config
    )
    outputs = []
    for sample_output_ids, sample_input_ids in zip(output_ids, data["input_ids"]):
        sample_output_ids = sample_output_ids[len(sample_input_ids):]
        sample_output = tokenizer.decode(sample_output_ids, skip_special_tokens=True)
        outputs.append(sample_output)
    return outputs


def generate_answers(
    model_name: str,
    input_path: str,
    output_path: str,
    batch_size: int = 1,
    load_in_8bit: bool = False,
):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    generation_config = GenerationConfig.from_pretrained(model_name)

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        load_in_8bit=load_in_8bit,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        attn_implementation="flash_attention_2",
    )
    model.eval()

    if batch_size > 1:
        assert tokenizer.padding_side == "left", "Batched inference for right padding side is impossible"
    records = read_jsonl(input_path)

    with open(output_path, "w") as w:
        for batch in tqdm(gen_batch(records, batch_size)):
            prompts = []
            for r in batch:
                if "instruction" in r:
                    messages = [{"role": "user", "content": r["instruction"]}]
                elif "messages" in r or "prompt" in r:
                    messages = r.get("messages", r.get("prompt"))

                assert messages
                if messages[-1]["role"] == "assistant":
                    messages = messages[:-1]
                prompt = tokenizer.apply_chat_template(
                    messages, tokenize=False, add_generation_prompt=True
                )
                prompts.append(prompt)
            outputs = generate(
                model=model,
                tokenizer=tokenizer,
                prompts=prompts,
                generation_config=generation_config
            )
            for record, prompt, output in zip(batch, prompts, outputs):
                print(prompt)
                print(output)
                print()
                print()
                record["instruction"] = record["instruction"].encode("utf-8").decode("utf-8", "ignore")
                if "input" in record and record["input"]:
                    record["input"] = record["input"].encode("utf-8").decode("utf-8", "ignore")
                record["answer"] = output.encode("utf-8").decode("utf-8", "ignore")
                w.write(json.dumps(record, ensure_ascii=False).strip() + "\n")


if __name__ == "__main__":
    fire.Fire(generate_answers)
