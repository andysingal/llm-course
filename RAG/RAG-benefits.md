RAG consists of augmenting LLMs with specific data and requiring the model to use and source this data 
in its answer rather than replying on what it may or may not have memorized in its memorized weights

1. Reducing hallucinations by limiting the LLM to answer based on existing chosen data
2. Helping with explainability, error checking, and copyright issues by clearly referencing
its sources for each comment

3. Giving private/specific or more up-to-date data to the LLM
4. Not relying too much on black box LLM training/fine-tuning for what the models know and have
memorized

Another way to increase LLM performance is through good prompting. Some prompting techniques:

1. "Chain of Thought" prompting involves asking the model to think througha problem step by step
before coming with a final answer. The key idea is that each token in a language model has a limited "processing bandwidth" or "thinking capacity".
The LLMs need these token to figure things out

2. "Few-Shot Prompting" is when we show the model examples of the answers we seek based on some given questions similar to those we the model to reive

3. " Self Consistency" involves asking the same question to multiple versions of the model and then choosing the answer that comes up most often.

If you want to add specialized knowledge quickly and more efficiently, RAG is a better first step. With RAG,you have more control over the information the model uses to generate responses,making the phase quicker, more transparent, and easier to manage.
<img width="1228" alt="Screenshot 2024-11-24 at 9 00 23 AM" src="https://github.com/user-attachments/assets/1f4c2ab3-4d3f-4189-9d0c-24560be3f062">

## What are LLMs
LLMs interpret and create human-like text that captures the nuances of natural language, including syntax(arrangement of words) and semantic(meaning of words)

The text generation process in Large Language Models is autoregressive, meaning they generate the next tokens based on the sequence of tokens already generated. The attention mechanism is a vital component in this process; it establishes word connections and ensures the text is coherent and contextually appropriate.

This learning process involves predicting the next token in a sequence using either classical statistical methods or novel deep learning techniques.

In practice, models work with tokens, not complete words. This approach allows for more accurate predictions and text generation by more effectively capturing the complexity of human language.

## Tokenization
It is the initial phase of interacting with LLMs. It involves breaking down the input text into smaller pieces know as tokens. Tokens can range from single characters to entire words, and the size of these tokens can greatly influence the model's performance.

## Embeddings
The next step after tokenization is to turn these tokens into something the computer can understand and work with - this is where embeddings come into play. Embeddings are way to translate the tokens, which are words or pieces of words, into a language of numbers that the computers can grasp.

An embedding gives each token a unique numerical ID that captures its meaning.This numerical form helps the computer see how similar tokens are, like knowing that "happy" and "joyful" are close in meaning, even though they are different words.

This step is essential because it helps the models make sense of language in a numerical way, bridging the gap between human language and machine processing.

## Training/Fine-Tuning 

- LLMS are trained on a large corpus of text with the objective of correctly predicting the next token of a sequence. The goal is to adjust the model's parameters to maximize the probability of a correct prediction based on a huge purpose dataset of text.

<img width="588" alt="Screenshot 2024-11-24 at 9 50 52 AM" src="https://github.com/user-attachments/assets/e5f793d5-0039-4c82-bf7d-d187db2e8b23">

## Context Size

The context size or window is a crucial aspect of LLMs. It referes to the maximum number of tokens the model can process in a single request. Context size influences the length of text the model can handle at any one time, directlt affecting the model's performance and the outcome it produces.

## Scaling Laws
The following elements determine a language models performance:
1. The number of parameters (N) denotes the model's ability to learn from data. A greater number of parameters enables the detection of more complicated patterns in data.

2. The size of Training Dataset and number of tokens, ranging from small text chunks to single characters are counted

3. FLOPS(Floating Point Operations Per Second) estimate the computational resources used during training

<img width="589" alt="Screenshot 2024-11-24 at 10 00 01 AM" src="https://github.com/user-attachments/assets/d8a8f469-fc56-476b-8281-60560cf316dc">

## Prompts
The text we provide to LLMs as instructions is commonly called prompts. Prompts are instructions given to AI systems like OpenAI's GPT-3 and GPT-4, providing context to generate human-like text -- the more detailed the prompt, the better the model's output

Prompting tips:
<img width="1146" alt="Screenshot 2024-11-24 at 10 06 48 AM" src="https://github.com/user-attachments/assets/24398662-d769-4861-9552-97d7c7a1abc3">

## Hallucinations and Biases in LLMs

In LLMs, hallucinations occur when the model creates outputs that do not corrspond to real-world facts or context. This can lead to the spread of diinformation, especially in crucial industries where information accuracy is critical.
Bias in LLMs can also result in outcomes that favor particular perspectives over others , possibly reinforcing harmful stereotypes and discimination.

## Example
```py
from dotenv import load_dotenv
load_dotenv
import os
import openai

## English text to translate
english_text = "Hello, how are you?"

response = openai.ChatCompletion.create(
           model="gpt-3.5-turbo",
           messsages=[
             {"role": "system", "content":"You are aa helpful assistant"},
             {"role": "user", "content": f""Translate the following English text to French: "{engligh_text}"""}],)

print(response['choice'][0]['message']['content'])

```

Introduction of LLMs proved that scaling model size and data can unlock emergent skills that outperform their smaller counterparts. Through in-context learning, these LLMs can handle more complex tasks.

##Factors leading to Emergent Abilities 

- Multistep reasoning involves instructing a model to perform a series of intermediate steps before providing the final result. This approach, know as chain-of-thought prompting, becomes more effective than standard prompting only when applied to sufficiently large models

- Another strategy is fine-tunin a model on various tasks presented as Instruction Following. This method shows improved performance only with models of a certain size, underlining the significance of scale in achieving advanced capabilities


## Expanding the Context Window

-- The importance of Context Length: Context window in Language models represents the number of inputs tokens the model can process simultaneously

-- Context length primarily enables the model to process and comprehend larger datasets simultaneously, offering a deeper understanding of the context. This feature is beneficial when inputting a substantial amount of specific data into a language model and posing questions related to this data.
For examples.. when analyzing a lengthy document about a particular company or issue, a larger context window allows the language model to review and remember more of this unique information, ressulting in more accurate and tailored responses.

<img width="1019" alt="Screenshot 2024-11-24 at 10 35 27 AM" src="https://github.com/user-attachments/assets/b7913249-bc3e-45f0-8132-ef087bf2c1db">

<img width="1008" alt="Screenshot 2024-11-24 at 10 36 22 AM" src="https://github.com/user-attachments/assets/b164e768-48ae-4d30-b974-c621565914fa">


<img width="1021" alt="Screenshot 2024-11-24 at 10 36 09 AM" src="https://github.com/user-attachments/assets/a197dd92-17bf-4a35-b139-4e48ce0d8118">





