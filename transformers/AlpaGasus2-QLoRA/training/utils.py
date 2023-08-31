from datasets import load_dataset

# Loading json type dataset using load_dataset of datasets library
def loading_dataset(data_path, data_type, val_set_size):
  data = load_dataset(data_type, data_files = data_path)
  dataset = data['train']
  
  # This is the formatting function of dataset.
  # We follow the data format of Stanford Alpaca
  def formatting_prompts_func(example):
    if example['input']:
      text = f"Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n### Instruction:\n{example['instruction']}\n\n### Input:\n{example['input']}\n\n### Response:\n{example['output']}"
    else:
      text = f"Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{example['instruction']}\n\n### Response:\n{example['output']}"
    return {'text': text}

  dataset = dataset.map(formatting_prompts_func)
  dataset = dataset.remove_columns(["instruction", "output", "input"])

  if val_set_size > 0:
    dataset = dataset.train_test_split(test_size = val_set_size)
    
  return dataset

# max_steps calculation function
def max_steps_calc(epochs, batch, data_line_count):
  return int(data_line_count / batch * epochs)

# gradient accumulation steps calculation function
def gradinet_acc_calc(batch, micro_batch_size):
  return batch // micro_batch_size
