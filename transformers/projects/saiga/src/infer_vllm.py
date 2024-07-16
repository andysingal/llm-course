from typing import Optional
import json

import fire
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer

from src.util.io import read_jsonl

SYSTEM_PROMPT = "Ты — Сайга, русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им."


def infer_vllm(
    model_name: str,
    input_path: str,
    output_path: str,
    temperature: float = 0.6,
    top_p: float = 0.9,
    top_k: int = 30,
    max_tokens: int = 2048,
    max_seq_len: int = 8192,
    repetition_penalty: float = 1.1,
    enable_system_prompt: bool = False,
    remove_bos_token: bool = False,
    quantization: Optional[str] = None
):
    sampling_params = SamplingParams(
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        max_tokens=max_tokens,
        repetition_penalty=repetition_penalty,
    )
    llm = LLM(
        model=model_name,
        max_seq_len_to_capture=max_seq_len,
        quantization=quantization,
    )
    tokenizer = llm.get_tokenizer()
    records = read_jsonl(input_path)
    role_mapping = {
        "bot": "assistant",
        "gpt": "assistant",
        "human": "user",
    }
    prompts = []
    for r in records:
        if "instruction" in r:
            messages = [{"role": "user", "content": r["instruction"]}]
        elif "messages" in r or "prompt" in r:
            messages = r.get("messages", r.get("prompt"))

        assert messages
        if messages[0]["role"] != "system" and enable_system_prompt:
            messages.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
        for m in messages:
            m["role"] = role_mapping.get(m["role"], m["role"])
        if messages[-1]["role"] == "assistant":
            messages = messages[:-1]

        prompt = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        if remove_bos_token:
            prompt = prompt.replace(tokenizer.bos_token, "")

        prompts.append(prompt)

    print(prompts[0])
    outputs = llm.generate(prompts, sampling_params)
    with open(output_path, "w") as w:
        for record, output in zip(records, outputs):
            prompt = output.prompt
            prompt_token_ids = output.prompt_token_ids
            assert prompt_token_ids[0] != prompt_token_ids[1], prompt_token_ids
            generated_text = output.outputs[0].text
            print(prompt)
            print(generated_text)
            print(prompt_token_ids)
            print()
            print()
            record["answer"] = generated_text.encode("utf-8").decode("utf-8", "ignore")
            w.write(json.dumps(record, ensure_ascii=False).strip() + "\n")


if __name__ == "__main__":
    fire.Fire(infer_vllm)
