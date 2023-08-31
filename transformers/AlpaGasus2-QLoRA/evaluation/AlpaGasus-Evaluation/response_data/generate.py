from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM
import torch
import json
import jsonlines
import fire

def main(
  base_model: str = "meta-llama/Llama-2-13b-hf",
  lora_weight: str = "alpaca2 or alpagasus2",
  auth_token: str = "",
  test_path: str = "AlpaGasus2-QLoRA/test_data/",
  save_path: str = "",
):
  
  if lora_weight == "alpaca2":
    lora_weight = "Abe13/Llama-2-13b-hf-SFT_Lora_Alpaca-juniper-v2"
  elif lora_weight == "alpagasus2":
    lora_weight = "StudentLLM/Alpagasus-2-13B-QLoRA"

  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  
  tokenizer = AutoTokenizer.from_pretrained(lora_weight)
  tokenizer.pad_token = tokenizer.eos_token
  
  config = PeftConfig.from_pretrained(lora_weight)
  model = AutoModelForCausalLM.from_pretrained(
      base_model,
      trust_remote_code=True,
      use_auth_token=auth_token,
  ).to(device)
  model = PeftModel.from_pretrained(model, lora_weight)

  test_data = ['koala_test_set.jsonl', 'sinstruct_test_set.jsonl', 'vicuna_test_set.jsonl']
  col = ['prompt', 'instruction', 'text']   # Columns of each test dataset
  

  for i in range(len(test_data)):
    result = []
    path = test_path + test_data[i]
    count = 0
    name = test_data[i].split('_')[0]
    sv_path = save_path + lora_weight + "_" +  name + "_seed_0.json"
    with jsonlines.open(path) as f:
      for line in f:
        if col[i]:
          input_data = f"Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{line[col[i]]}\n\n### Response:\n"
        else:
          if line['instances'][0]['input']:
            input_data = f"Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n### Instruction:\n{line['instruction']}\n\n### Input:\n{line['instances'][0]['input']}\n\n### Response:\n"
          else:
            input_data = f"Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{line['instruction']}\n\n### Response:\n"
        model_inputs = tokenizer(input_data, return_tensors='pt').to(device)
        num_tokens = len(tokenizer.tokenize(input_data))
        max_length = 512 + num_tokens if 512 + num_tokens <= 4096 else 4096
        model_output = model.generate(**model_inputs, max_length=max_length)   
        model_output = tokenizer.decode(model_output[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)
        model_output = model_output.split("Response:")[1]    # post-processing
        if lora_weight == 'alpaca2':
          model_output = model_output.split("### End")[0]
        elif lora_weight == 'alpagasus2':
          model_output = model_output.split("###")[0]
        count += 1
        output = {}
        index = name + '_' + str(count)
        output['question_id'] = index
        output[col[i]] = line[col[i]]
        if col[i] == 'instruction':
          if line['instances'][0]['input']:
            output['instances'] = [{'input': line['instances'][0]['input']}]
          else:
            output['instances'] = [{'input': ""}]
        output[lora_weight] = model_output
        result.append(output)
  
    with open(sv_path, "x") as json_file:
      json.dump(result, json_file, indent=4)

if __name__ == "__main__":
  fire.Fire(main)
