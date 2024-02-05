import torch
from datasets import load_dataset
from peft import LoraConfig, get_peft_model
from transformers import AutoTokenizer, AutoModelForCausalLM
from trl import DPOTrainer


if __name__ == "__main__":
	model_name = "..."
	dataset = load_dataset(...)
	
	tokenizer = AutoTokenizer.from_pretrained(model_name)
	tokenizer.pad_token = tokenizer.eos_token

	model = AutoModelForCausalLM.from_pretrained(
		model_name,
		low_cpu_mem_usage=True,
		torch_dtype=torch.bfloat16,
		load_in_4bit=True,
		use_flash_attention_2=True,
		bnb_4bit_compute_dtype=torch.bfloat16,
		bnb_4bit_quant_type="nf4",
	)
	model.resize_token_embeddings(len(tokenizer))
	model.config.pad_token_id = tokenizer.pad_token_id
	model.config.use_cache = False

	ref_model = AutoModelForCausalLM.from_pretrained(
		model_name,
		low_cpu_mem_usage=True,
		torch_dtype=torch.bfloat16,
		load_in_4bit=True,
		use_flash_attention_2=True,
		bnb_4bit_compute_dtype=torch.bfloat16,
	).eval()

	peft_config = LoraConfig(
		lora_alpha=128,
		lora_dropout=0.05,
		r=64,
		bias="none",
		task_type="CAUSAL_LM",
		target_modules=[
			"q_proj",
			"k_proj",
			"v_proj",
		],
	)
	model = get_peft_model(model, peft_config)

	training_args = DPOConfig(
		num_train_epochs=3,
		learning_rate=5e-07,
		per_device_train_batch_size=1,
		do_eval=True,
		per_device_eval_batch_size=1,
		adam_epsilon=1e-08,
		lr_scheduler_type="linear",
		warmup_ratio=0.1,
		seed=42,
		logging_steps=100,
		save_steps=500,
		save_strategy="steps",
		output_dir="./output-dir",
		gradient_checkpointing=True,
		bf16=True,
		remove_unused_columns=False,
	)

	dpo_trainer = DPOTrainer(
		model,
		ref_model,
		args=training_args,
		beta=training_args.beta,
		train_dataset=dataset["train"],
		eval_dataset=dataset["test"],
		tokenizer=tokenizer,
		max_length=training_args.max_length,
		max_prompt_length=training_args.max_prompt_length,
		peft_config=peft_config,
	)
	dpo_trainer.train()
	dpo_trainer.save_model()