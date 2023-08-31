# AlpaGasus Evaluation

We tried to follow the evaluation metric introduced by AlpaGasus paper.
During the process, we consulted the code by [gpt4life](https://github.com/gpt4life/alpagasus/blob/main/evaluation/eval.py), an unofficial implementation of AlpaGasus.
Due to resource constraints, we have replaced the evaluator model from GPT-4 to gpt-3.5-turbo.
For the same reason, the WizardLM Evaluation dataset was excluded.
We exclusively evaluated AlpaGasus2-QLoRA using 'koala', 'self-instruct', and 'vicuna' test sets.

The following models were used for evaluation.

- Evaluator Model: gpt-3.5-turbo-16k-0613
- Base Model: [AlpaGasus2-QLoRA-13B](https://huggingface.co/StudentLLM/Alpagasus-2-13B-QLoRA)
- Comparison Model: [Alpaca2-LoRA-13B](https://huggingface.co/Abe13/Llama-2-13b-hf-SFT_Lora_Alpaca-juniper-v2)

## Running evaluation.py

The provided code below is for the running of evaluation.py. When executing the code, please ensure to input your own OpenAI API key.

```python
%cd AlpaGasus2-QLoRA/evaluation/AlpaGasus-Evaluation
for eval_file in 'koala_seed_0.json', 'sinstruct_seed_0.json', 'vicuna_seed_0.json':
    python evaluation.py --API_KEY your_own_API_KEY --model your_model -qa AlpaGasus2-QLoRA/evaluation/AlpaGasus-Evaluation/response_data/results/${eval_file} -k1 alpaca2 -k2 alpagasus2 --max_tokens 256 --output_dir AlpaGasus2-QLoRA/evaluation/AlpaGasus-Evaluation/rating_data/
    python evaluation.py --API_KEY your_own_API_KEY --model your_model -qa AlpaGasus2-QLoRA/evaluation/AlpaGasus-Evaluation/response_data/results/${eval_file} -k1 alpagasus2 -k2 alpaca2 --max_tokens 256 --output_dir AlpaGasus2-QLoRA/evaluation/AlpaGasus-Evaluation/rating_data/ 
```

## Result processing

We utilized the obtained result file(koala_result.json, sinstruct_result.json, vicuna_result.json) from running evaluation.py to generate and display the results graph.
In the case of the evaluation of AlpaGasus, evaluation was processed twice times to avoid the positional bias problem that chronic problem of model-based evaluation.
Hence, a judgment rule like the one below described in the AlpaGasus paper is required.

- Win: AlpaGasus wins twice, or wins once and draws once.
- Tie: AlpaGasus draws twice, or wins once and loses once.
- Lose: AlpaGasus loses twice, or loses once and draws once.

The code to generate a result graph using the aforementioned judgment rule and result graph are as follows:

```python
python result_graph.py --file_path AlpaGasus2-QLoRA/evaluation/AlpaGasus-Evaluation/evaluation_score/ --output_dir your_path
```

![results](https://github.com/gauss5930/AlpaGasus2-QLoRA/assets/80087878/8742bcc4-1bbc-449f-8bcf-660c08fcc10d)

A result graph presented that AlpaGasus2 outperforms Alpaca2 overwhelmingly. 
In the AlphaGasus paper, they also claimed that AlphaGasus outperforms Alpaca. 
However, the results in the paper do not exhibit a substantial difference in performance.
We believe that these experimental results to the following reasons.

- While AlphaGasus2 was directly fine-tuned using the LLaMA2 model by us, the resource constraints prevented separate fine-tuning of Alpaca2. Consequently, we employed a pre-existing model deemed suitable. However, due to the inability to access precise learning specifics, we cannot ascertain the adequacy of the training process, thereby hindering a detailed analysis of the underlying reasons for the obtained results. Nevertheless, it is my conjecture that the substantial variance in performance stems from potential imperfections in the fine-tuning of the Alpaca2 model obtained from the HuggingFace Hub.
- Nonetheless, as evident from the outcomes reported in the AlphaGasus paper, AlphaGasus2 demonstrates superior performance when compared to Alpaca2. This result reaffirms that data quality plays an important role than data quantity during the fine-tuning process.
