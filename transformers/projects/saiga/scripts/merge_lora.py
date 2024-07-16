import fire
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftConfig, PeftModel


def merge_lora(model_name: str, output_path: str, device_map: str = "auto"):
    config = PeftConfig.from_pretrained(model_name)
    base_model_path = config.base_model_name_or_path

    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        load_in_8bit=False,
        torch_dtype=torch.bfloat16,
        device_map=device_map,
    )

    lora_model = PeftModel.from_pretrained(
        base_model, model_name, torch_dtype=torch.bfloat16, device_map=device_map
    )

    lora_model = lora_model.merge_and_unload()
    lora_model.train(False)

    lora_model.save_pretrained(output_path)


if __name__ == "__main__":
    fire.Fire(merge_lora)
