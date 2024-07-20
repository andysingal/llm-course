Let’s examine each building block, starting from the encoding part:

- Input embedding->those are the vector representation of tokenized input text;
- Positional encoding-> as the Transformer does not have an inherent sense of word order (unlike RNNs with their sequential nature),positional encodings are added to the input embeddings. These encodings provide information about the positions of words in the input sequence, allowing the model to understand the order of tokens;
- Multi-head attention layer-> a mechanism in which multiple self-attention mechanisms operate in parallel on different parts of the input data, producing multiple representations. This allows the Transformer model to attend to different parts of the input data in parallel and aggregate information from multiple perspectives.
- Add and Norm layer-> it combines element-wise addition and layer normalization. It adds the output of a layer to the original input and then applies layer normalization to stabilize and accelerate training. This technique helps mitigate gradient-related issues and improves the model's performance on sequential data;
Feed-forward layer-> it is responsible for transforming the normalized output of attention layers into a suitable representation for the final output, using non-linear activation function such as the ReLU.
The decoding part of the Transformer starts with a similar process as the encoding part, where the target sequence (output sequence) undergoes input embedding and positional encoding.

- Output embedding (shifted right)-> For the decoder, the target sequence is "shifted right" by one position. This means that at each position, the model tries to predict the token that comes after the token in the original target sequence. This is achieved by removing the last token from the target sequence and padding it with a special start-of-sequence token (start symbol). This way, the decoder learns to generate the correct token based on the preceding context during autoregressive decoding.

Decoders layers->similarly to the encoder block, also here we have positional encoding, multi-head attention, Add&Norm, and feed-forward layers, whose role is the same as above;

- Linear and SoftMax->those layers apply, respectively, a linear and non-linear transformation to the output vector. The non-linear transformation (softmax) convey the output vector into a probability distribution, corresponding to a set of candidate word. The word corresponding to the greatest element of the probability vector will be the output of the whole process.
-
- <img width="448" alt="Screenshot 2024-04-15 at 10 46 11 AM" src="https://github.com/andysingal/llm-course/assets/20493493/4080d8e4-1f3f-462d-b4b5-ec76d162c439">

## Training a Large Language Model
By definition, Large Language Models are huge, from a double point of view:

1. Number of parameters: It is a measure of the complexity of the LLM architecture and represents the number of connections among neurons. Complex architectures have tons of layers, each one having multiple neurons, meaning that among layers we will have several connections with associated parameters (or weights).
2. Training set: It refers to the unlabeled text corpus on which the LLM learns and train its parameter. To give an idea of how big can be such a text corpus for an LLM, let’s consider the OpenAI’s GPT-3 training set:
<img width="603" alt="Screenshot 2024-04-15 at 10 57 50 AM" src="https://github.com/andysingal/llm-course/assets/20493493/cdbe28b0-afe0-4f31-93e9-a48d06eee800">

The training process involves numerous iterations over the dataset, fine-tuning the model's parameters using optimization algorithms backpropagation. Through this process, transformer-based language models acquire a deep understanding of language patterns, semantics, and context, enabling them to excel in a wide range of natural language processing tasks, from text generation to sentiment analysis and machine translation.Below the main steps involved in the training process of a Large Language Model:

1. Data collection. This is the process of gathering a large amount of text data from various sources, such as the open web, books, news articles, social media, etc. The data should be diverse, high-quality, and representative of the natural language that the LLM will encounter.
2. Data preprocessing. This is the process of cleaning, filtering, and formatting the data for training. This may include removing duplicates, noise, or sensitive information, splitting the data into sentences or paragraphs, tokenizing the text into subwords or characters, etc.
3. Model architecture. This is the process of designing the structure and parameters of the LLM. This may include choosing the type of neural network (such as transformer) and its structure (such as decoder only, encoder only or encoder-decoder), the number and size of layers, the attention mechanism, the activation function etc.
Model initialization. This is the process of assigning initial values to the weights and biases of the LLM. This may be done randomly or by using pre-trained weights from another model.
4. Model training. This is the process of updating the weights and biases of the LLM by feeding it batches of data and computing the loss function. The loss function measures how well the LLM predicts the next token given the previous tokens. The LLM tries to minimize the loss by using an optimization algorithm (such as gradient descent, Adam, etc.) that adjusts the weights and biases in the direction that reduces the loss with the backpropagation mechanism. The model training may take several epochs (iterations over the entire data set) until it converges to a low loss value.

## Model evaluation
Evaluating traditional AI models was, in some ways, pretty intuitive. For example, let’s think about an image classification model that have to determines whether the input image represents a dog or a cat. So we train our model on a training dataset with a set of labelled images and, once the model is trained, we test it on unlabeled images. The evaluation metric is simply the percentage of correctly classified images over the total number of images within the test set.When it comes to Large Language Models, the story is a bit different. As those models are trained on unlabeled text and are not task-specific, but rather generic and adaptable given a user’s prompt, traditional evaluation metrics were not suitable anymore. Evaluating an LLM means, among other things, measuring its language fluency, its coherence, its ability to emulate different styles depending on user’s request.Henceforth, a new set of evaluation frameworks urged to be introduced. The following are the most popular frameworks used to evaluate LLMs:

1. GLUE (General Language Understanding Evaluation) and SuperGLUE-> this benchmark is used to measure the performance of LLMs on various natural language understanding tasks, such as sentiment analysis, natural language inference, question answering, etc. The higher the score on the GLUE benchmark, the better the LLM is at generalizing across different tasks and domains.
It recently evolved into a new benchmark styled after GLUE and called SuperGLUE, that comes with more diffucult tasks. It consists of eight challenging tasks that require more advanced reasoning skills than GLUE, such as natural language inference, question answering, coreference resolution, etc., a broad coverage diagnostic set that tests models on various linguistic capabilities and failure modes, and a leaderboard that ranks models based on their average score across all tasks.

The difference between the GLUE and the SuperGLUE benchmark is that the SuperGLUE benchmark is more challenging and realistic than the GLUE benchmark, as it covers more complex tasks and phenomena, requires models to handle multiple domains and formats, and has higher human performance baselines. The SuperGLUE benchmark is designed to drive research in the development of more general and robust natural language understanding systems.

3. MMLU (Massive Multitask Language Understanding) ->it is a benchmark that measure the knowledge of an LLM using zero-shot and few-shot settings.

Definition

The concept of zero-shot evaluation is a method of evaluating a language model without any labeled data or fine-tuning. It measures how well the language model can perform a new task by using natural language instructions or examples as prompts, and computing the likelihood of the correct output given the input. It the probability that a trained model will produce a particular set of tokens without needing any labeled training data.

<img width="623" alt="Screenshot 2024-07-20 at 11 14 00 PM" src="https://github.com/user-attachments/assets/fedc8455-8131-484b-ac1b-f0fb7657ceaf">
