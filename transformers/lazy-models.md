```py
from transformers import LlamaForCausalLM, AutoConfig, AutoTokenizer
from accelerate.utils import set_seed
from accelerate.big_modeling import init_empty_weights
from safetensors.torch import load_file
from pathlib import Path
import json
from safetensors import safe_open
from accelerate.utils import retie_parameters
from transformers import GenerationConfig
from transformers.utils.hub import get_checkpoint_shard_files
import time

set_seed(42)

llama_path = Path("/mnt/superfast/llama-3-8B")

tokenizer = AutoTokenizer.from_pretrained(llama_path)
inputs = tokenizer("Tell me about a girl that", return_tensors="pt")


config = AutoConfig.from_pretrained(llama_path)
use_keep_in_fp32_modules = False

resolved_archive_file, sharded_metadata = get_checkpoint_shard_files(
                llama_path,
                llama_path/"model.safetensors.index.json"
            )
loaded_state_dict_keys = sharded_metadata["all_checkpoint_keys"]

config = LlamaForCausalLM._autoset_attn_implementation(
            config, use_flash_attention_2=False, torch_dtype=None, device_map=None
        )
with init_empty_weights():
    factory_model = LlamaForCausalLM(config)

index_filename = llama_path / "model.safetensors.index.json"

with open(index_filename, "r") as f:
    index = json.load(f)

if "weight_map" in index:
    index = index["weight_map"]
checkpoint_files = sorted(list(set(index.values())))
checkpoint_files = [llama_path / f for f in checkpoint_files]

model_keys = set(factory_model.state_dict().keys())
new_state_dict = {}

for checkpoint_file in checkpoint_files:
    with safe_open(checkpoint_file, framework="pt") as f:
        metadata = f.metadata()
        weight_names = f.keys()
    file_state = load_file(checkpoint_file)
    new_state_dict.update(file_state)
factory_model.load_state_dict(new_state_dict, strict=True, assign=True)

retie_parameters(factory_model, [["lm_head.weight"]])

factory_model.eval()

factory_model.generation_config = GenerationConfig.from_pretrained(
                    llama_path
                )

start_time = time.time()
output = factory_model.generate(**inputs, max_new_tokens=20, num_return_sequences=1)

end_time = time.time()
time_taken = end_time - start_time
new_tokens = len(output[0]) - inputs.input_ids.shape[1]
print(f"{time_taken:.3f}s | {new_tokens/time_taken:.3f} tokens/second | {tokenizer.batch_decode(output, skip_special_tokens=True)} | ")
```
