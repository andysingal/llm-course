## The key Insights of Transformers

1. The first insight is the usage of the attention mechanism. Previous NLP methods, such as recurrent neural networks, struggled to handle long sentences. Attention mechanisms allow the transformers model to attend to long sequences and learn long-range relationships. In other words, transformers can estimate how relevant some tokens are to other tokens.

2. The second key aspect is their ability to scale. The transformer architecture has an implementation optimized for parallelization, and research has shown that these models can scale to handle high-complexity and high-scale datasets. Although initially designed for text data, the transformer architecture can be flexible enough to support different data types and handle irregular inputs.

3. The third key insight is the ability to do pre-training and fine-tuning. Traditional approaches to a task, such as movie review classification, were limited by the availability of labeled data. A model would be trained from scratch on a large corpus of labeled examples, attempting to predict the label from the input text directly. This approach is often referred to as supervised learning. However, it has a significant drawback: it requires a large amount of labeled data to train effectively. This is a problem because labeled data is expensive to obtain and time-consuming to label. There might not even be any available data in many domains!

To address this, researchers began looking for a way to pre-train models on existing data that could then be fine-tuned (or adjusted) for a specific task. This approach is known as transfer learning and is the foundation of modern ML in many fields, such as Natural Language Processing and Computer Vision. Initial works in NLP focused on finding domain-specific corpora for the language model pre-training phase, but papers such as ULMFiT9 showed that even pre-training on generic text such as Wikipedia could yield impressive results when the models were fine-tuned on downstream tasks. This set the stage for the rise of transformers, which turned out to be highly well-suited to learning rich representations of language.

The idea of pre-training is to train a model on a large unlabeled dataset and then fine-tune it to a new target task, for which one would require much less labeled data. Before graduating to NLP, transfer learning had already been very successful with the Convolutional Neural Networks that form the backbone of modern Computer Vision. In this scenario, one first trains a large model with a massive amount of labeled images in a classification task. Through this process, the model learns common features that can be leveraged on a different but related problem. For example, we can pre-train a model on thousands of classes and then fine-tune it to classify whether a picture is of a hot dog.


This embedding can then be leveraged by adding a small, simple network on top of the encoder and fine-tuning the model for the specific task. As a concrete example, we can add a simple linear layer on top of the BERT encoder output to predict the sentiment of a document. We can take this approach to tackle a wide range of tasks:

a. Token classification. Identify each entity in a sentence, such as a person, location, or organization.

b. Extractive question answering. Given a paragraph, answer a specific question and extract the answer from the input.

c. Semantic search. The features generated by the encoder can be handy to build a search system. Given a database of a hundred documents, we can compute the embeddings for each. Then, we can compare the input embeddings with the documents’ ones at inference time, hence identifying the most similar document in the database.10

And many others, including text similarity, anomaly detection, named entity linking, recommendation systems, and document classification.
