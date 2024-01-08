import argparse
import auto_gptq
from transformers import GPTQConfig, AutoModelForCausalLM, AutoTokenizer

# Function to get the device based on user input or system capability
def get_device(device_map):
    if device_map == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    return device_map

# Function to configure and return the quantized model
# https://huggingface.co/docs/transformers/main_classes/quantization#transformers.GPTQConfig
def configure_model(model_id, bits, dataset, tokenizer, group_size, device):
    gptq_config = GPTQConfig(bits=bits, dataset=dataset, tokenizer=tokenizer, group_size=group_size, desc_act=True)
    model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=gptq_config)
    model.to(device)
    return model

# Main function to execute the script logic
def main(model_id, bits, dataset, group_size, device_map):
    device = get_device(device_map)
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = configure_model(model_id, bits, dataset, tokenizer, group_size, device)

    model_dir = f"{model_id}_quantized_{bits}bit"
    model.save_pretrained(model_dir)
    tokenizer.save_pretrained(model_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quantize a GPT model.")
    parser.add_argument("--model_id", default="mistralai/Mistral-7B-v0.1", type=str, help="The pretrained model ID.")
    parser.add_argument("--bits", default=4, type=int, help="Number of bits for quantization.")
    parser.add_argument("--dataset", default="wikitext2", type=str, help="The dataset to use.")
    parser.add_argument("--group_size", default=128, type=int, help="Group size for quantization.")
    parser.add_argument("--device_map", default="auto", type=str, help="Device map for loading the model.")
    parser.add_argument("--use_exllama", default="True", type=bool, help="Whether to use exllama backend. Defaults to True if unset. Only works with bits = 4.")
    parser.add_argument("--desc_act", default="False", type=bool, help=" Whether to quantize columns in order of decreasing activation size. Setting it to False can significantly speed up inference but the perplexity may become slightly worse. Also known as act-order.")

    args = parser.parse_args()

    main(model_id=args.model_id, bits=args.bits, dataset=args.dataset, group_size=args.group_size, device_map=args.device_map)
