TYPES OF EMBEDDING MODEL IN MULTIMODAL RAG SYSTEM

As we move into more multimodal knowledge retrieval systems, it's crucial to understand the types of embedding models we need to use.

In text-based systems, the embedding model is quite straightforward: we provide text as input and get a vector as output. However, in Retrieval-Augmented Generation (RAG) systems, which comprise both images and text as data, the scenario becomes more complex.

RAG systems can utilize different types of embedding models to handle multimodal data effectively:

1. Early Fusion Models - These models combine text and image data at the input level, allowing the model to learn joint representations from the start. This can capture interactions between modalities but requires careful preprocessing.

Advantages:
- The model can learn joint representations from the combined data.
- May capture interactions between different modalities more effectively.

Disadvantages:
- Handling different modalities together can be challenging, especially if they have different dimensions or formats.
- Requires significant preprocessing to align the data from different sources.

Example: Meta Imagebind, Google MagicLens, OpenAI Clip

2. Mid Fusion Models -  In these models, text and image data are processed separately initially, and the features extracted are combined at an intermediate stage. This approach balances the need for separate feature extraction and joint learning but increases the model's complexity.

Advantages:
- Allows for separate processing and feature extraction from each modality.
- The model can learn modality-specific features before combining them.

Disadvantages:
- Requires careful design to determine the optimal point and method for fusing the modalities.
- Complexity increases due to the need for multiple sub-networks.

Example: Salesforce BLIP models

3. Late Fusion Models: These models process text and image data separately through their own sub-networks, and the outputs are combined at the final stage. This method is simple and flexible, allowing for independent processing, but it might not fully capture the interactions between modalities.

Advantages:
- Simple to implement as each modality can be processed independently.
- Flexibility to use different models tailored to each modality.
- Reduces the complexity of combining different modalities.

Disadvantages:
- Might not capture interactions between modalities as effectively as early fusion.
- The fusion of final predictions might not leverage the full potential of joint learning.
<img width="563" alt="Screenshot 2024-07-21 at 9 27 14 PM" src="https://github.com/user-attachments/assets/bbfe72e3-2378-42cc-961a-999d96e9e44f">


