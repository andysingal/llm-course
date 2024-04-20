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


#### Define evaluation metrics
Besides monitoring the loss, defining some downstream metrics that will allow us to monitor the training is usually a good idea. We’ll leverage the evaluate library, a handy tool with a standardized interface for various metrics. The choice of metrics depends on the task. For sequence classification, suitable candidates can be:

1. Accuracy: Represents the proportion of correct predictions, providing a high-level view of overall model performance.

2. Precision: The ratio of correctly labeled positive examples to all instances labeled as positive. It guides us in understanding the accuracy of positive predictions.

3. Recall: The proportion of actual positive examples predicted correctly by the model. It helps uncover the model’s ability to capture all positive instances, hence being lower if false negatives exist.

4. F1 Score: The harmonic mean of precision and recall, offering a balanced measure that considers both false positives and false negatives.
