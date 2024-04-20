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

Examples:
These are just some of the massive explosion of instruct-tuned models. Flan-T5 is a fine-tuned T5 model using the FLAN dataset. Alpaca is an LLaMA fine-tune on an instruction dataset generated by InstructGPT. WizardLM is a LLaMA instruct-tune on the Evol-Instruct dataset. ChatGLM2 is a fine-tuned bilingual model trained on English and Chinese instructions. Dolly 2 is a Pythia instruct-tuned on the Dolly dataset. 

[Instruction datasets](https://github.com/jianzhnie/awesome-instruction-datasets)

[More Reading](https://lightning.ai/pages/community/tutorial/optimizing-llms-from-a-dataset-perspective/) 

[Self-Instruct](https://github.com/yizhongw/self-instruct)

<img width="712" alt="Screenshot 2024-04-20 at 9 08 21 AM" src="https://github.com/andysingal/llm-course/assets/20493493/94c9b032-50f1-4c21-a662-f963c50ed515">


### When should you use fine-tuning vs. instruct-tuning vs. prompt engineering?
Once again, it depends on the task, available resources desired experimentation speed, and more. Usually, fine-tuned models specific to a task or domain will perform better. On the other hand, it won’t allow you to tackle tasks out of the box. Instruct-tune is more versatile, but defining the dataset and structure requires additional work. Prompt engineering is the most flexible approach for quick experimentation, as it won’t require you to train a model out of the box.

#### introduction to adapters
Let’s now dive into the fourth approach: adapters. So far, we’ve explored fine-tuning DistilBERT for text classification and GPT-2 to generate text in our specific style. In both cases, all weights of the model were modified during fine-tuning. Fine-tuning is much more efficient than pre-training as we don’t need too much data or compute power. However, as the trend of larger models keeps growing, doing traditional fine-tuning becomes infeasible on consumer hardware. Additionally, if we want to fine-tune an encoder model for different tasks, we’ll end up with multiple models.

Welcome: PEFT! Parameter-efficient fine-tuning, called PEFT, is a group of techniques that enables adapting the pre-trained models without fine-tuning all the model parameters. Typically, we add a small number of extra parameters, called adapters, and then fine-tune them while freezing the original pre-trained model. What effects does this have?

1. Faster training and lower hardware requirements: When doing traditional fine-tuning, we update many parameters. With PEFT, we only update the adapter, which has a small percentage of parameters compared to the base model. Hence, training is completed much faster and can be done with smaller GPUs.

2. Lower storage costs: After fine-tuning the model, we only need to store the adapter instead of the whole model for each fine-tuning. When some models can take over 100Gb to store, it won’t scale well if each downstream model requires saving all the parameters again. An adapter could be 1% of the size of the original model. If we have 100 fine-tunes of a 100Gb model, traditional fine-tuning would take 10,000Gb of storage while PEFT would take 200Gb (the original model and 100 adapters of 1Gb each).

3. Comparable performance: The performance of the PEFT models tends to be comparable to the performance of fully fine-tuned models

4. No latency hit: As we’ll see soon, after training, the adapter can be merged into the pre-trained model, meaning the final size and inference latency will be the same.

Amongst the most popular ones are prefix tuning, prompt tuning, and low-rank adaptation (LoRA). LoRA represents the weight updates with two smaller matrices called update matrices using low-rank decomposition. Although this can be applied to all blocks in the transformers models, we usually apply them only to attention blocks. 

How does it work under the hood? When you fine-tune a base model, you’re updating the layers. Computing the update matrices can be memory intensive, so LoRA tries to approximate these update matrices with smaller matrices. For example, let’s assume there’s a single update matrix with 10,000 rows and 20,000 columns. That means that the update matrix has 200 million values. With LoRA, we represent the update matrix with two smaller matrices with a a rank +r+. Assuming a rank 8, the first matrix, A, would have 10,000 rows and 8 columns, while matrix B would have 8 rows and 20,000 columnms (to ensure same input and output sizes). A has 80,000 values and B has 160,000. We went from 200 million values to 240,000 values. That’s 800 times smaller! LoRA assumes that these matrices can approximate well enough the weight update matrice

<img width="970" alt="Screenshot 2024-04-20 at 9 25 25 AM" src="https://github.com/andysingal/llm-course/assets/20493493/f8dd6c6f-9682-49db-a709-5acfa8227970">

### An introduction to Quantization

PEFT allows us to fine-tune models with less compute and disk space. The size of the model during inference is not decreased. If you’re doing inference of a model with 30 billion parameters, you will still need a powerful GPU to run it. For example, a 176B model such as Bloom would require 8 A100 GPUs, which are pretty powerful and expensive (each one costs over $15k!). In this section, we’ll discuss some techniques that will allow us to run the models with smaller GPUs in a way that does not degrade their performance.

Let’s say we have a model of 7 billion parameters. Each of those parameters has a data type or precision. For example, the float32 (FP32, also called full precision) type stores a float number with 32 bits. 7 billion parameters are 224 billion bits corresponding to 28 Gigabytes14. FP32 allows the representation of a wide range of numbers with high precision, which is important for pre-training models.

In many cases, though, such a wide range is not required. In those cases, we can use float16 (or FP16, also called half-precision). FP16 has less precision and a lower range of numbers (the largest number possible is 64,000), which introduces new risks: a model can overflow (if a number is not within the range of representable numbers).

A third data type is Brain Floating-Point, or bfloat16. BF16 uses 16 bits just like FP16, but allocates those bits in a different way in order to gain more precision for smaller numbers (like those typically seen in neural network weights) while still covering the same total range as FP32.

Using full precision for training and inference usually leads to the best results, but it’s significantly slower. For training, people have found ways to do mixed-precision training, which offers a significant speedup. In mixed-precision training, the weights are maintained in full precision as reference, but the operations are done in half-precision. The half-precision updates are used to update the full-precision weights. The precision does not significantly impact inference, so we can load the model with half-precision. PyTorch loads all models in full precision by default, so we need to specify the type when loading a model by passing the torch_dtype if we want to use float16 or bfloat16.

<img width="1144" alt="Screenshot 2024-04-20 at 9 38 14 AM" src="https://github.com/andysingal/llm-course/assets/20493493/b46e5aa2-ee53-4d97-b752-767d670cdd6c">

<img width="726" alt="Screenshot 2024-04-20 at 9 40 15 AM" src="https://github.com/andysingal/llm-course/assets/20493493/97b8144e-52c1-47c4-93e7-0d391f3e85af">


### All together
Let’s review PEFT and quantization.

PEFT allows us to fine-tune models using much less compute by adding adapters and freezing the base model weights. This accelerates training, given only a few weights are updatable.

Quantization allows us to load a model using fewer bits than those used for storage. This reduces the GPU requirements to load and run inference with a model.
