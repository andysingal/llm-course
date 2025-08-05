- Cognitive scaffolding: Cognitive scaffolding is a teaching method where an expert provides temporary support to help a learner develop a new skill or concept. This support is gradually reduced as the learner becomes more competent, ultimately enabling them to perform the task independently.
- Inference: It is the process of generating tokens in response to a particular input.

- Model: A machine-learning (ML) model is a mathematical representation or algorithm that learns patterns from data to make predictions, decisions, or inferences without being explicitly programmed for the task.

- Model data: A model’s data includes its weights, bias, and configuration. Weights and bias are what the model learns during training, and the model configuration holds the metadata to run the model, such as its embeddings and label classes (for classification models), its max_batch_size property (for batch inference), and its input and output tensors.
- Model architecture: Architecture refers to the structure and design of an ML model. It defines how the model is organized, including the types and number of layers, the connections between layers, and the operations the model performs. The architecture determines how the model processes input data to produce output predictions or decisions.
- Model execution code: A model’s execution code is what the model runs. It generally initializes the architecture in the model serving framework, loads weights, and runs predictions (or other outputs).
- Model serving: Deploying an ML model in a production environment, where it can process new data and generate predictions
- Observability in this context means the ability to monitor these models to detect anomalies, errors, or malicious behavior early on.
- Key-value caching is a technique that helps speed up the model inference process by remembering important information (such as attention) from previous steps. Instead of recomputing everything from scratch, the model reuses what it has already calculated, making text generation much faster and more efficient.


- When the model sees the input prompt, it calculates and stores it as key-value pairs in the cache.

- When generating new tokens, instead of starting over to recalculate KV cache from the very beginning, the model retrieves the stored KV cache instead.

- With the KV cache, the model now can calculate attention efficiently by aligning the cached keys and values with the new query (Q) to compute the new token.

- The model appends the newly generated token to the existing sequence and repeats the process from step 2 until it is finished generating.


- A model runtime is a specialized software framework designed to execute ML models efficiently on different hardware platforms. It serves as the intermediary layer between the trained model and the device’s hardware, optimizing the inference process to maximize speed, efficiency, and resource utilization.
- Ambient Agents: Ambient agents are AI systems designed to operate continuously in the background, monitoring data streams and automatically taking actions based on predefined rules and user intent, without requiring direct human prompts.


## Resources
[Demystifying essential AI buzzwords](https://blogs.oracle.com/fusioninsider/post/demystifying-essential-ai-buzzwords)
