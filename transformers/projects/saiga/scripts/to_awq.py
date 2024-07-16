import fire

from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer


quant_config = {"zero_point": True, "q_group_size": 128, "w_bit": 4, "version": "GEMM"}


def to_awq(model_path, quant_path):
    model = AutoAWQForCausalLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model.quantize(tokenizer, quant_config=quant_config)

    model.save_quantized(quant_path)
    tokenizer.save_pretrained(quant_path)


if __name__ == "__main__":
    fire.Fire(to_awq)
