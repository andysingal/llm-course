## Define Which Model Type to Use
We can use three types of transformers depending on which type of task we’re trying to solve:

1. Encoder Models: They are great at obtaining rich representations from sequences. They output embeddings, which contain semantic information about the input. We can then add a small network on top of these embeddings and train it for a new specific task that relies on the semantic information (such as identifying entities in the text or classifying the sequence).

2. Decoder Models: They are ideal for generating new text.

3. Encoder-Decoder Models: They are ideal for tasks that require generating new sentences based on a given input.


##### EXAMPLE
Now, considering the task of topic classification for short news article abstracts, we have two main approaches:

1. Text Generation Model: Fine-tune a text generation model to generate the label (e.g., "business“) given an input news article. The first approach is similar to what a model called T5 does - it solves many different tasks by formulating them as text generation problems, ending with a single model that can solve many tasks.

2. Encoder Model with Classification Head: Fine-tune an encoder model by adding a simple classification network (called head) to the embeddings. This approach provides a specialized and efficient model tailored to our use case, making it a favorable choice for our topic classification task.


#### Pick a Good Base Model
Our requirements are:

- An encoder-based model architecture.

- A small model that we can fine-tune in a few minutes.

- A pretrained model with solid results.

- A model that can process a small number of tokens.


n fine-tuning, choosing the right base model is an essential decision. Several factors come into play; let’s explore some of them:

1. Model Size: Deploying a model with 60 billion parameters locally on your computer won’t be practical. The choice of model size depends on factors like expected inference, hardware capacity, and deployment requirements. Later in this chapter, we’ll delve into techniques that enable running models with more parameters using the same computing resources.

2. Training data: The performance of your fine-tuned model correlates with how closely the training data of the base model aligns with your inference data. For instance, fine-tuning a model to generate code in your codebase style is more effective when starting with a model pre-trained specifically on code. Consider the specificity of data sources, especially if not all models disclose their training data. Similarly, you will want to use something other than a predominantly English-based model for Korean text generation. Not all models disclose which were the data sources, which can make it challenging to identify this.

3. Context length: Different models have different context length limits. The context length is the maximum number of tokens the model can use when making predictions. For example, if the context length is 1024, the model can use the last 1024 tokens to make predictions. To generate long-form text, you will need a model with a large context length.

4. License: The licensing aspect is crucial when selecting a base model. Consider whether the model aligns with your usage requirements. Models may have commercial or non-commercial licenses, and there’s a distinction between open-source and open-access licenses. Understanding these licenses is essential to ensure compliance with legal and usage restrictions. For example, although some models may permit commercial use, they can specify permissive use cases and scenarios where the model should not be used.


Benchmarks such as ARC for science questions, HellaSwag for common sense inference, and others serve as proxies for different capabilities. Hugging Face Open LLM Leaderboard collects benchmark results for thousands of models and allows filtering according to model size and type. 




#### Define evaluation metrics
Besides monitoring the loss, defining some downstream metrics that will allow us to monitor the training is usually a good idea. We’ll leverage the evaluate library, a handy tool with a standardized interface for various metrics. The choice of metrics depends on the task. For sequence classification, suitable candidates can be:

1. Accuracy: Represents the proportion of correct predictions, providing a high-level view of overall model performance.

2. Precision: The ratio of correctly labeled positive examples to all instances labeled as positive. It guides us in understanding the accuracy of positive predictions.

3. Recall: The proportion of actual positive examples predicted correctly by the model. It helps uncover the model’s ability to capture all positive instances, hence being lower if false negatives exist.

4. F1 Score: The harmonic mean of precision and recall, offering a balanced measure that considers both false positives and false negatives.


Finally, we need to define the training arguments. In this example, we modify a couple to showcase that TrainingArguments provides a lot of control and flexibility. Let’s take a closer look at a couple of key parameters, showcasing the significant influence they can have on model training:

<img width="660" alt="Screenshot 2024-04-20 at 8 51 33 AM" src="https://github.com/andysingal/llm-course/assets/20493493/86820f00-615d-4a5a-9cff-81724b66280c">


### Instructions 
Benefits, limitations, and uses of different approaches:

1. Fine-tuning multiple models: We can pick and fine-tune a base model for each task to build a specialized model. All the model weights are updated during fine-tuning, which implies that if we want to solve five different tasks, we’ll end up with five model fine-tunes.

2. Adapters: We can freeze the base model and train a small auxiliary model called an adapter rather than modifying all the model weights. We would still need a different adapter for every new task, but they are significantly smaller, meaning we can easily have multiple without adding overhead. 

3. Prompting: We can use a robust pretrained model’s zero-shot and few-shot capabilities to solve different tasks. With zero-shot, we write a prompt that explains a task in detail. With a few-shot approach, we add examples of solving the task and improving the model’s performance. The performance of these capabilities hinges on the strength of the base model. A very strong model such as GPT-4 may yield impressive zero-shot results, which is great for tackling all kinds of tasks, such as writing those long emails or summarizing a book chapter.

4. Instruct-tuning: Instruct-tuning is an alternative and simple way to improve the zero-shot performance of LLMs. Instruct tuning formulates tasks as instructions such as "Is the topic of this post business or sports?" or "Translate '`how are you' to Spanish`”. This approach mainly involves constructing a dataset of instructions for many tasks and then fine-tuning a pretrained language model with this mixture of instruction datasets. Creating datasets for instruct-tuning is a task of manageable complexity; for instance, one could utilize AG News and structure the inputs and labels as instructions by building a prompt .

By building a large enough dataset of diverse instructions, we can end up with a general instruct-tuned model that can solve many tasks, even unseen ones, thanks to cross-task generalization. This idea is the foundation behind Flan, a model that can solve 62 tasks out of the box.


### When should you use fine-tuning vs. instruct-tuning vs. prompt engineering?
Once again, it depends on the task, available resources desired experimentation speed, and more. Usually, fine-tuned models specific to a task or domain will perform better. On the other hand, it won’t allow you to tackle tasks out of the box. Instruct-tune is more versatile, but defining the dataset and structure requires additional work. Prompt engineering is the most flexible approach for quick experimentation, as it won’t require you to train a model out of the box.






