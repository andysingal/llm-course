Llama3.1-60B-Instruct: Removing 10B parameters (15%) with minimal performance loss and no retraining.

Using nyuntam - A New Open-Source Toolkit for Model Compression and Adaptation dropped in Github

Applying FLAP (Fluctuation-based Adaptive Structured Pruning) to compress and accelerate the Llama3.1-70b-instruct model.

FLAP allows for significant reduction in model size and computational requirements without sacrificing performance.

Unlike traditional pruning techniques, FLAP requires no retraining and adapts the pruning ratio across different modules and layers, offering an efficient and effective approach for deploying large language models in resource-constrained environments.

<img width="570" alt="Screenshot 2024-09-01 at 9 10 45 PM" src="https://github.com/user-attachments/assets/b62d8773-14b2-4ca6-ad79-4ea3a186ed75">
