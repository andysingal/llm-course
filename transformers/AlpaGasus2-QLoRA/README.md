# AlpaGasus2-QLoRA 🦙🦄🤏
This is an unofficial implementation of "AlpaGasus: Training a better Alpaca with Fewer Data." with LLaMA2 & QLoRA! The trained model is available at the [HuggingFace Hub](https://huggingface.co/StudentLLM).

This repository houses the source code that implements AlpaGasus2-QLoRA with LLaMA2 and QLoRA.
Model size variants are 7B and 13B, as we utilized [LLaMA2-7B-hf](https://huggingface.co/meta-llama/Llama-2-7b-hf) and [LLaMA2-13B-hf](https://huggingface.co/meta-llama/Llama-2-13b-hf), respectively. 
[gpt4life](https://github.com/gpt4life/alpagasus)'s alpaca_t45 dataset filtered by gpt-3.5-turbo-0301 was used.

For AlpaGasus2-QLoRA fine-tuning, Google Colab's single A100 40G GPU was used! 
In addition, we leveraged [QLoRA](https://arxiv.org/abs/2305.14314) to implement the large model with only one GPU.
To implement the model with QLoRA, HuggingFace's PEFT and the BitsAndBytes library were employed.
Further, the SFTTrainer of trl library was used to fine-tune the model.

To evaluate AlpaGasus2-QLoRA, we endeavored to align our evaluation metric as closely as possible with the original AlpaGasus.
We utilized the gpt-3.5-turbo as the evaluator model and [Alpaca2-LoRA](https://huggingface.co/Abe13/Llama-2-13b-hf-SFT_Lora_Alpaca-juniper-v2) as the comparison model.



## Dataset
AlpaGasus carefully selected higher-quality data through filtering on the original Alpaca instruction dataset to show improved performance than the original Alpaca.
For data filtering, gpt-3.5-turbo was used, as a result, the dataset was filtered from 52K to 9K.
Please check more specific data filtering processes in the [AlpaGasus paper](https://arxiv.org/abs/2307.08701), and [gpt4life](https://github.com/gpt4life/alpagasus)'s gpt-3.5-turbo filtered dataset, 'alpaca_t45.json' was used for fine-tuning AlpaGasus2-QLoRA.
Configuration of the dataset is as follows:

```
{
    'instruction': Give the instruction describing the question.
    'input': Occasionally present, detailed instructions accompany the question if available.
    'output': Give answers to questions.
}
.
.
.
```

## Requirements
If you want to run finetune.py, install some libraries specified in 'requirements.txt'.

```
pip install -r requirements.txt
```

## Fine-tuning
We fine-tuned our model using the SFTTrainer of the trl library and referred to [Stanford Alpaca](https://github.com/tatsu-lab/stanford_alpaca).
AlpaGasus2-QLoRA was fine-tuned with LLaMA2-7B and LLaMA2-13B with following parameters:

|Hyperparameters|LLaMA2-7B|LLaMA2-13B|
|---|---|---|
|Batch size|128|128|
|learning rate|2e-5|1e-5|
|Epochs|3|5|
|Max Length|256|256|
|weight decay|0|0|

In addition, we also used QLoRA to save memory and speed up the fine-tuning of LLMs.
QLoRA Configuration is as follows:

|Hyperparameters|QLoRA|
|---|---|
|Quantization bit|4bit|
|Quantization type|NF4|
|LoRA rank|8|
|LoRA alpha|32|
|LoRA dropout|0.05|
|target modules|q_proj, v_proj|


- For the instruction-finetuning of LLaMA-2-7B:
```
python AlpaGasus2-QLoRA/training/finetune.py \
    --base_model 'meta-llama/Llama-2-7b-hf' \
    --data_path 'AlpaGasus2-QLoRA/dataset/alpaca_t45.json' \
    --data_type 'json' \
    --output_dir './results' \
    --hub_path 'Hub path to upload the model'
    --auth_token 'your HuggingFace Authorization code' \
    --num_epochs 3 \
    --learning_rate 2e-5 \
    --val_set_size 0
```

- For the instruction-finetuning of LLaMA-2-13B:
```
python AlpaGasus2-QLoRA/training/finetune.py \
    --base_model 'meta-llama/Llama-2-13b-hf' \
    --data_path 'AlpaGasus2-QLoRA/dataset/alpaca_t45.json' \
    --data_type 'json' \
    --output_dir './results' \
    --hub_path 'Hub path to upload the model'
    --auth_token 'your HuggingFace authorization key'
    --num_epochs 5 \
    --learning_rate 1e-5
    --val_set_size 0
```

You can modify the arguments according to your taste!
```
python AlpaGasus2-QLoRA/training/finetune.py \
    --base_model 'your model' \
    --data_path 'your data' \
    --data_type 'your data's type' \
    --hub_path 'Hub path to upload the model'
    --auth_token 'your HuggingFace authorization key'
    --output_dir './results' \
    --batch_size 128 \
    --micro_batch_size 4 \
    --num_epochs 3 \
    --learning_rate 2e-5 \
    --cutoff_len 512 \
    --val_set_size 0 \
    --load_in_4bit True \
    --bnb_4bit_quant_type 'nf4' \
    --bnb_4bit_double_quant True \
    --lora_r 8 \
    --lora_alpha 32 \
    --lora_dropout 0.05 \
    --lora_target_modules '[q_proj,v_proj]' \
```

## Generation
For generating the output of the AlpaGasus2-QLoRA model, please follow the following code! 
We only provide the usage of a 13B model, but the use of the 7B model is the same!

**AlpaGasus2-QLoRA-13b**
```python
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

config = PeftConfig.from_pretrained("StudentLLM/Alpagasus-2-13B-QLoRA")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-13b-hf", use_auth_token="yotu_HuggingFace_token").to(device)
model = PeftModel.from_pretrained(model, "StudentLLM/Alpagasus-2-13B-QLoRA")

tokenizer = AutoTokenizer.from_pretrained("StudentLLM/Alpagasus-2-13B-QLoRA")
tokenizer.pad_token = tokenizer.eos_token

input_data = "Please tell me 3 ways to relieve stress."   # You can enter any questions!!

model_inputs = tokenizer(input_data, return_tensors='pt').to(device)
model_output = model.generate(**model_inputs, max_length=256)
model_output = tokenizer.decode(model_output[0], skip_special_tokens=True)
model_output
```

## AlpaGasus2-QLoRA Evaluation
### 1. AlpaGasus Evaluation

We tried to follow the evaluation metric introduced by the AlpaGasus paper. 
During the process, we consulted the code by [gpt4life](https://github.com/gpt4life/alpagasus).
We used the gpt-3.5-turbo as the evaluator model, and [Alpaca2-LoRA-13B](https://huggingface.co/Abe13/Llama-2-13b-hf-SFT_Lora_Alpaca-juniper-v2) as the comparison model. For more detailed information, please refer to the [AlpaGasus-Evaluation](https://github.com/gauss5930/AlpaGasus2-QLoRA/tree/main/evaluation/AlpaGasus-Evaluation) file.

The evaluation result of AlpaGasus2-QLoRA is as follows: 

![results](https://github.com/gauss5930/AlpaGasus2-QLoRA/assets/80087878/1dbc56ac-5cb0-4821-95ed-267e79acfd3f)

A result graph presented that AlpaGasus2 outperforms Alpaca2 overwhelmingly. 
In the AlphaGasus paper, they also claimed that AlphaGasus outperforms Alpaca. 
However, the results in the paper do not exhibit a substantial difference in performance.
We believe that these experimental results to the following reasons.

- While AlphaGasus2 was directly fine-tuned using the LLaMA2 model by us, the resource constraints prevented separate fine-tuning of Alpaca2. Consequently, we employed a pre-existing model deemed suitable. However, due to the inability to access precise learning specifics, we cannot ascertain the adequacy of the training process, thereby hindering a detailed analysis of the underlying reasons for the obtained results. Nevertheless, it is our conjecture that the substantial variance in performance stems from potential imperfections in the fine-tuning of the Alpaca2 model obtained from the HuggingFace Hub.
- Nonetheless, as evident from the outcomes reported in the AlphaGasus paper, AlphaGasus2 demonstrates superior performance when compared to Alpaca2. This result reaffirms that data quality plays an important role than data quantity during the fine-tuning process.

### 2. Open LLM Leaderboard Evaluation
[AlpaGauss2-QLoRA](https://huggingface.co/StudentLLM/Alpagasus-2-13B-QLoRA-merged) performance was uploaded on HuggingFace's [Open LLM Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard).
The AlpaGauss2-QLoRA was evaluated on the tasks specified in HF's Open LLM Leaderboard(ARC, HellaSwag, MMLU, TruthfulQA).
The table below shows the performance of AlpaGasus2-QLoRA on the aforementioned tasks.


|Benchmarks|13B|
|---|---|
|ARC|58.28|
|HellaSwag|80.98|
|MMLU|54.14|
|TruthfulQA|34.21|

## References
- [Llama2](https://arxiv.org/abs/2307.09288)
- [Self-Instruct](https://arxiv.org/abs/2212.10560)
- [Stanford Alpaca](https://github.com/tatsu-lab/stanford_alpaca/tree/main)
- [Vicuna](https://lmsys.org/blog/2023-03-30-vicuna/)
- [Koala](https://bair.berkeley.edu/blog/2023/04/03/koala/)
- [QLoRA](https://arxiv.org/abs/2305.14314)
- [AlpaGasus](https://arxiv.org/abs/2307.08701)
- [gpt4life/alpagasus](https://github.com/gpt4life/alpagasus)

## Citation
If you find it is a useful repository, please cite the paper:
```
@article{chen2023alpagasus,
  title={AlpaGasus: Training a Better Alpaca with Fewer Data},
  author={Lichang Chen, Shiyang Li, Jun Yan, Hai Wang, Kalpa Gunaratna, Vikas Yadav, Zheng Tang, Vijay Srinivasan, Tianyi Zhou, Heng Huang, Hongxia Jin},
  journal={arXiv preprint arXiv:2307.08701},
  year={2023}
}
```
