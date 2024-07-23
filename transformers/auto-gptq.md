```py
!pip install transformers auto_gptq torch torchvision torchaudio accelerate datasets requests -q

import torch
import logging
import warnings
import time
import os
from auto_gptq import AutoGPTQForCausalLM
from transformers import AutoTokenizer

# Record the start time of the script
start_time = time.time()

# Ignore specific warnings
warnings.filterwarnings("ignore", category=FutureWarning, message="`resume_download` is deprecated")

# Suppress less important logging messages
logging.getLogger("transformers").setLevel(logging.CRITICAL)
logging.getLogger("auto_gptq").setLevel(logging.CRITICAL)
logging.getLogger("huggingface_hub").setLevel(logging.CRITICAL)
logging.getLogger("auto_gptq.modeling._base").setLevel(logging.CRITICAL)

# Set the cache directory for Hugging Face transformers
os.environ['TRANSFORMERS_CACHE'] = os.path.expanduser('~/.cache/huggingface/hub')

# Check for GPU availability and set the device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the tokenizer for the specific model
tokenizer = AutoTokenizer.from_pretrained("rinna/youri-7b-instruction-gptq")

# Load the quantized model for faster inference
model = AutoGPTQForCausalLM.from_quantized("rinna/youri-7b-instruction-gptq",
                                           use_safetensors=True,
                                           checkpoint_format='gptq')

# Move the model to the GPU if available
model.to(device)

# Prompt the model with a question
prompt = "What kind of country is Colombia?"

# Tokenize the prompt
token_ids = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")

# Move token IDs to the GPU
token_ids = token_ids.to(device)

# Generate a response from the model
with torch.no_grad():
    output_ids = model.generate(
        input_ids=token_ids,
        max_length=200,  # Set maximum response length
        do_sample=True,
        temperature=0.5,   # Control randomness in output
        pad_token_id=tokenizer.eos_token_id,
        bos_token_id=tokenizer.bos_token_id,
        eos_token_id=tokenizer.eos_token_id
    )

# Decode the generated response and print it
output = tokenizer.decode(output_ids.tolist()[0])
print(output)

# Record the end time and calculate the total execution time
end_time = time.time()
print(f"Total execution time of the script: {end_time - start_time:.2f} seconds")
```


### flask version
```py
from flask import Flask, request, jsonify
import torch
import logging
import warnings
import time
import os
from auto_gptq import AutoGPTQForCausalLM
from transformers import AutoTokenizer

app = Flask(__name__)

# Manage model and tokenizer as global variables
model = None
tokenizer = None

def load_model():
    global model, tokenizer
    start_time = time.time()

    # Ignore specific warnings
    warnings.filterwarnings("ignore", category=FutureWarning, message="resume_download is deprecated")

    # Suppress less important logging messages
    logging.getLogger("transformers").setLevel(logging.CRITICAL)
    logging.getLogger("auto_gptq").setLevel(logging.CRITICAL)
    logging.getLogger("huggingface_hub").setLevel(logging.CRITICAL)
    logging.getLogger("auto_gptq.modeling._base").setLevel(logging.CRITICAL)

    # Set cache directory for Hugging Face transformers
    os.environ['TRANSFORMERS_CACHE'] = os.path.expanduser('~/.cache/huggingface/hub')

    # Check for GPU availability
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained("rinna/youri-7b-instruction-gptq")

    # Load quantized model
    model = AutoGPTQForCausalLM.from_quantized("rinna/youri-7b-instruction-gptq",
                                               use_safetensors=True,
                                               checkpoint_format='gptq')

    # Move model to GPU if available
    model.to(device)

    end_time = time.time()
    print(f"Model preloading time: {end_time - start_time:.2f} seconds")

# Load model when application starts
load_model()

@app.route('/generate', methods=['POST'])
def generate():
    global model, tokenizer
    data = request.json
    input_text = data.get("input_text", "")

    # Create prompt
    prompt = input_text + "Response:"

    # Tokenize prompt, truncate if necessary
    token_ids = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt", truncation=True)

    # Generate response
    with torch.no_grad():
        output_ids = model.generate(
            input_ids=token_ids.to(model.device),  # Move input to model's device
            max_length=200,
            do_sample=True,
            temperature=0.8,
            pad_token_id=tokenizer.eos_token_id,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id
        )

    # Decode response and remove prompt length
    prompt_length = token_ids.size(1)
    output = tokenizer.decode(output_ids[0][prompt_length:], skip_special_tokens=True)

    return jsonify({"response": output})

if __name__ == '__main__':
    app.run(debug=False)
```
