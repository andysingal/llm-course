```py
from datasets import Dataset
from trl import OnlineDPOConfig, OnlineDPOTrainer
from transformers import (
    AutoModelForCausalLM,
    AutoModelForSequenceClassification,
    AutoTokenizer,
)
NUM_DUMMY_SAMPLES = 100

tokenizer = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolLM-135M-Instruct")
tokenizer.add_special_tokens({"pad_token": "[PAD]"})
# The model to optimise
model = AutoModelForCausalLM.from_pretrained("HuggingFaceTB/SmolLM-135M-Instruct")
# The reference model to calculate the KL divergence against
ref_model = AutoModelForCausalLM.from_pretrained("HuggingFaceTB/SmolLM-135M-Instruct")
# The model to score completions with. In practice, you will need a reward model.
reward_model = AutoModelForSequenceClassification.from_pretrained("HuggingFaceTB/SmolLM-135M-Instruct", num_labels=1)

train_dataset = Dataset.from_dict(
    {"prompt": ["Q: Hi how are you? A:"] * NUM_DUMMY_SAMPLES})
eval_dataset = Dataset.from_dict(
    {"prompt": ["Q: What do you like to eat A:"] * NUM_DUMMY_SAMPLES})

args = OnlineDPOConfig(output_dir="online-dpo-model")
trainer = OnlineDPOTrainer(
    model=model,
    ref_model=ref_model,
    reward_model=reward_model,
    args=args,
    tokenizer=tokenizer,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)
trainer.train()

```


source:
- [online-dpo](https://huggingface.co/docs/trl/main/online_dpo_trainer)
