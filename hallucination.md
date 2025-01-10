## Hallucination Detection 
Hallucination in LLMs occur when a model generates text that is incorrect and not grounded in reality.Several factors contribute to hallucination:
- LLMs might be trained on datasets lacking the necesaary knowledge to answer specific questions
- These models often lack mechanisms to verify the factual accuracy of their outputs , leading to potentially convincing yet incorrect responses
- Hallucinations can also arise from this discrepancy because the primary aim of a language model is to learn a language's word distribution patterns , not to differentate between true and false statements

## Improving LLM Accuracy
- Tuning the Text Generation parameters : Parameters such as temperature, frequency penalty, presence penalty and top-p significantly influence LLM output- a lower temperature value results in more predictable and reproducible results
- Leveraging External documents with Retrievers Architectures: .. LLM accuracy can be improved by incorporating domain-specific knowledge through external documents...LLM uses the top-ranked retrieved texts as contexts to provide the final response. This method makes the model less prone to hallucinations by guiding it to produce accurate and contextually appropriate responses

## Reducing Bias in LLMs: Constitutional AI

Constitutional AI is a framework developed by Anthropic researchers to align Ai systems with  human values, focusing on making them beneficial, safe and trustworthy

## Evaluating LLM Performance: Objective functions and evaluation metrics are critical components of machine learning models

- The cross-entropy is the commonly used objective function for LLMs. In casual anguage modeling, where the model predicts the subsequent token from a predetermined list
- Evaluation metrics are tools to measure the model's performance in terms that are understandable to humans.
- Intrinsic metrics which are directly related to the training objective--perplexity... first step... measure perplexity is calculating the probability of a sentence. This is done by multiplying the probabilities assigned to each word

![Screenshot 2024-12-05 090547](https://github.com/user-attachments/assets/3f277db8-f59e-4d73-ac22-5fca54da5744)

[RAG Hallucination Detection Techniques](https://machinelearningmastery.com/rag-hallucination-detection-techniques/)



<img width="767" alt="Screenshot 2024-10-06 at 9 55 16 PM" src="https://github.com/user-attachments/assets/4ca9510c-d83d-475a-ab37-5257e4b9853f">

Resource:
- [Awesome-Hallucination-detector](https://github.com/EdinburghNLP/awesome-hallucination-detection)
