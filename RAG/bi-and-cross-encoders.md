I finally understood why re-rankers are so powerful once I understood the difference between bi- and cross-encoders.

Bi-encoders (similar to vector search) process the query and documents separately.
1. Pre-compute document embeddings
2. At inference time, compute query embedding

This makes bi-encoders perfect for 1st-stage retrieval:
• fast
• scalable
• but might miss contextual nuances

Cross-encoders are a popular architecture for re-ranking models.
They process the query and documents together.
1. Concatenate query and each document  ([CLS] Query [SEP] Document [SEP])
2. Process together for full cross-attention

This makes cross-encoders perfect for 2nd-stage retrieval:
• contextually rich for more precise results
• but slow and computationally expensive at scale

<img width="407" alt="Screenshot 2024-09-17 at 10 02 10 PM" src="https://github.com/user-attachments/assets/8ac56abf-a0e5-4f6a-9e1a-b1ffabdb702d">
