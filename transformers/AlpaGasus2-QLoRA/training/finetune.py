from typing import List
import fire
import os

from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
from datasets import load_dataset
import sentencepiece
from peft import LoraConfig, prepare_model_for_kbit_training
from trl import SFTTrainer
import json
import torch
import logging

import utils

def train(
    # model/data params
    base_model: str = "",  # required argument
    data_path: str = "", # required argument. You can only load a dataset that consists of 'instruction', 'input', and 'output' formats.
    data_type: str = "hf", # required argument. If you want to load your own dataset, please put the type of your dataset. You can also load HuggingFace dataset if you set 'hf'.
    output_dir: str = "./results",
    hub_path: str = "", # Your HuggingFace Hub path to upload fine-tuned model
    auth_token: str = "", # Please put your HuggingFace user authorization code. This token needs when loading LLaMA2 model.
    # training hyperparams
    batch_size: int = 128, # The batch size of Stanford Alpaca
    micro_batch_size: int = 4,
    num_epochs: int = 3,   # Set to 3 if you want to fine-tune 7b models. Set to 5 if you want to fine-tune 13b models.
    learning_rate: float = 2e-5, # Set to 2e-5 if you want to fine-tune 7b models. Set to 1e-5 if you want to fine-tune 13b models.
    cutoff_len: int = 256,
    val_set_size: float = 0.05,
    # bnb hyperparams
    load_in_4bit: bool = True,
    bnb_4bit_quant_type: str = 'nf4',
    bnb_4bit_double_quant: bool = True,
    # lora hyperparams
    lora_r: int = 8,
    lora_alpha: int = 32,
    lora_dropout: float = 0.05,
    lora_bias: str = "none",
    lora_task_type: str = "CAUSAL_LM",
    lora_target_modules: List[str] = [
        "q_proj",
        "v_proj",
    ],
):
    if int(os.environ.get("LOCAL_RANK", 0)) == 0:
        print(
            f"Training Alpaca-LoRA model with params:\n"
            f"base_model: {base_model}\n"
            f"data_path: {data_path}\n"
            f"data_type: {data_type}\n"
            f"output_dir: {output_dir}\n"
            f"hub_paht: {hub_path}"
            f"auth_token: {auth_token}\n"
            f"batch_size: {batch_size}\n"
            f"micro_batch_size: {micro_batch_size}\n"
            f"num_epochs: {num_epochs}\n"
            f"learning_rate: {learning_rate}\n"
            f"cutoff_len: {cutoff_len}\n"
            f"val_set_size: {val_set_size}\n"
            f"load_in_4bit: {load_in_4bit}\n"
            f"bnb_4bit_quant_type: {bnb_4bit_quant_type}\n"
            f"bnb_4bit_double_quant: {bnb_4bit_double_quant}\n"
            f"lora_r: {lora_r}\n"
            f"lora_alpha: {lora_alpha}\n"
            f"lora_dropout: {lora_dropout}\n"
            f"lora_bias: {lora_bias}\n",
            f"lora_task_type: {lora_task_type}\n",
            f"lora_target_modules: {lora_target_modules}\n"
        )
    assert (
        base_model
    )

    device_map = "auto"

    # Load dataset
    if data_type == "hf":
        dataset = load_dataset(data_path)
        if val_set_size > 0:
            dataset = dataset.train_test_split(test_size=val_set_size)
    else:
        dataset = utils.loading_dataset(data_path, data_type, val_set_size)

    # Quantization configuration
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=load_in_4bit,
        bnb_4bit_quant_type=bnb_4bit_quant_type,
        bnb_4bit_double_quant=bnb_4bit_double_quant,
        bnb_4bit_compute_type=torch.float16,
    )

    # Load Model with Quantization config
    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        quantization_config=bnb_config,
        trust_remote_code=True,
        device_map=device_map,
        use_auth_token=auth_token,
    )

    # Model Preprocessing
    model.config.use_cache = False
    model.config.pretraining_tp = 1
    model = prepare_model_for_kbit_training(model)

    # Load Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        base_model,
        max_seq_length=cutoff_len,
        trust_remote_code=True,
        use_auth_token=auth_token,
    )

    # Tokenizer specific option
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # LoRA configuration
    peft_config = LoraConfig(
        r=lora_r,
        lora_alpha=lora_alpha,
        lora_dropout=lora_dropout,
        bias=lora_bias,
        task_type=lora_task_type,
        target_modules=lora_traget_modules,
    )

    # TrainingArguments
    if not val_set_size > 0:
        steps = utils.max_steps_calc(num_epochs, batch_size, len(dataset))
    gradient_accumulation_steps = utils.gradient_acc_calc(batch_size, micro_batch_size)


    training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=num_epochs if val_set_size > 0 else None,
            per_device_train_batch_size=micro_batch_size,
            per_device_eval_batch_size=micro_batch_size if val_set_size > 0 else None,
            gradient_accumulation_steps=gradient_accumulation_steps,
            eval_accumulation_steps=gradient_accumulation_steps if val_set_size > 0 else None,
            save_strategy="epoch" if val_set_size > 0 else "steps",
            evaluation_strategy="epoch" if val_set_size > 0 else None,
            save_steps=None if val_set_size > 0 else 10,
            save_total_limit=1,
            weight_decay=0,
            learning_rate=learning_rate,
            warmup_ratio=0.03,
            max_steps=-1 if val_set_size > 0 else steps,
            lr_scheduler_type="cosine",
            logging_steps=1,
        )
    
    # SFTTrainer
    trainer=SFTTrainer(
        model=model,
        train_dataset=dataset["train"] if val_set_size > 0 else dataset,
        eval_dataset=dataset["test"] if val_set_size > 0 else None,
        peft_config=peft_config,
        dataset_text_field="text",
        max_seq_length=cut_off_len,
        tokenizer=tokenizer,
        args=training_args,
        packing=False
    )

    trainer.train()

    trainer.model.save_pretrained(hub_path)
    
    if hub_path:
        del model
        torch.cuda.empty_cache()

        model = AutoPeftModelForCausalLM.from_pretrained(
            hub_path, device_map="auto", torch_dtype=torch.bfloat16
        )
        model = model.merge_and_unload()

        model.push_to_hub(hub_path, use_temp_dir=False)
        tokenizer.push_to_hub(hub_path, use_temp_dir=False)

if __name__ == "__main__":
    fire.Fire(train)
