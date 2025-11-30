In deep learning, we often use the terms embedding vectors, representations, and latent space. What do these concepts have in common, and how do they differ?

While these three terms are often used interchangeably, we can make subtle distinctions between them:

- Embedding vectors are representations of input data where similar items are close to each other. Alternatively, Embedding vectors, or embeddings for short, encode relatively high-dimensional data into relatively low-dimensional vectors.
Embeddings can have higher or lower numbers of dimensions than the original input. For instance, using embeddings methods for extreme expression, we can encode data into two-dimensional dense and continuous representations for visualization purposes and clustering analysis
<img width="692" alt="Screenshot 2024-04-21 at 8 57 35 PM" src="https://github.com/andysingal/llm-course/assets/20493493/d12de310-421f-4c38-bb14-32295e1db987">

- Latent space is typically used synonymously with embedding space, the space into which embedding vectors are mapped.

- Representations are encoded versions of the original input.

A representation is an encoded, typically intermediate form of an input. For instance, an embedding vector or vector in the latent space is a representation of the input, as previously discussed. However, representations can also be produced by simpler procedures. For example, one-hot encoded vectors are considered representations of an input.

The key idea is that the representation captures some essential features or characteristics of the original data to make it useful for further analysis or processing.

- Attention sink: An "attention sink" is a phenomenon in large language models where initial tokens, especially the very first one, consistently receive a disproportionate amount of attention across transformer layers. This happens because the softmax function allocates unused attention to a few tokens, and in auto-regressive models, the initial tokens are seen most frequently, leading to a concentration of attention
- Rotary Position Embedding: Most LLMs adopt Rotary Position Embedding
as their default positional encoding mechanism, which has become
the de facto standard in contemporary architectures.
RoPE encodes token positions by rotating each
query/key vector on a sequence of two-dimensional
planes. This formulation allows attention scores to
depend on relative positional offsets while preserving the simple dot-product structure.




## SELF-SUPERVISED LEARNING 
Self-supervised learning is a pretraining procedure that lets neural networks leverage large, unlabeled datasets in a supervised fashion.
Self-supervised learning is related to transfer learning, a technique in which a model pretrained on one task is reused as the starting point for a model on a second task. For example, suppose we are interested in training an image classifier to classify bird species. In transfer learning, we would pretrain a convolutional neural network on the ImageNet dataset, a large, labeled image dataset with many different categories, including various objects and animals. After pretraining on the general ImageNet dataset, we would take that pretrained model and train it on the smaller, more specific target dataset that contains the bird species of interest. 

<img width="733" alt="Screenshot 2024-04-24 at 12 32 03 PM" src="https://github.com/andysingal/llm-course/assets/20493493/5dce1a13-0fc7-4a5d-82ce-3da6d7383e84">


Self-supervised learning is an alternative approach to transfer learning in which the model is pretrained not on labeled data but on unlabeled data. We consider an unlabeled dataset for which we do not have label information, and then we find a way to obtain labels from the dataset’s structure to formulate a prediction task for the neural network
<img width="643" alt="Screenshot 2024-04-24 at 12 33 02 PM" src="https://github.com/andysingal/llm-course/assets/20493493/e95da500-9a93-46f7-9b41-f078c360f59f">

With self-supervised learning, we can leverage unlabeled data. Hence, self-supervised learning is likely to be useful when working with large neural networks and with a limited quantity of labeled training data.

Transformer-based architectures that form the basis of LLMs and vision transformers are known to require self-supervised learning for pretraining to perform well.

## Self-Prediction and Contrastive Self-Supervised Learning
There are two main categories of self-supervised learning: 
1. self-prediction
2. contrastive self-supervised learning.

Desc. with fig. : we typically change or hide parts of the input and train the model to reconstruct the original inputs, such as by using a perturbation mask that obfuscates certain pixels in an image.

<img width="500" alt="Screenshot 2024-04-24 at 12 40 45 PM" src="https://github.com/andysingal/llm-course/assets/20493493/17a132de-aba0-4c52-879e-be29d36b8946">

Example: A classic example is a denoising autoencoder that learns to remove noise from an input image. Alternatively, consider a masked autoencoder that reconstructs the missing parts of an image 

<img width="662" alt="Screenshot 2024-04-24 at 12 44 05 PM" src="https://github.com/andysingal/llm-course/assets/20493493/80f54f1b-7c79-4d0a-8e27-d535fcc75ac3">

In contrastive self-supervised learning, we train the neural network to learn an embedding space where similar inputs are close to each other and dissimilar inputs are far apart. In other words, we train the network to produce embeddings that minimize the distance between similar training inputs and maximize the distance between dissimilar training examples.

<img width="666" alt="Screenshot 2024-04-24 at 12 45 04 PM" src="https://github.com/andysingal/llm-course/assets/20493493/4c13af89-914f-4f69-8cb8-4539d833fcb3">

