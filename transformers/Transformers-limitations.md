Limitations
At this point, you might wonder what the issues are with transformers. Let’s briefly go over some of the limitations:

1. Transformers are very large. Research has consistently shown that larger models perform better. Although that’s quite exciting, it also brings concerns. First, some of the most powerful models require dozens of millions of U.S. dollars to train - just in computing power! That means that only a small set of institutions can train very large base models, limiting the kind of research that institutions without those resources can do. Second, using such amounts of computing power can also have ecological implications - those millions of GPU hours are, of course, powered by lots of electricity! Third, even if some of these models are open-sourced, running them might require many GPUs! Chapter 5 will explore some techniques to use these LLMs even if you don’t have multiple GPUs at home. Even then, deploying them in resource-constrained environments is a frequent challenge.

2. Sequential processing: If you recall the decoder section, we had to process all the previous tokens for each new token. That means generating the token 10,000 in a sequence will be much slower than generating the first. In computer science terms, transformers have quadratic time complexity with respect to the input length, making it challenging to scale them to very long documents or use these models in some real-time scenarios.

3. Fixed input size: Transformer models can handle a maximum number of tokens, which depends on the base model. Some transformers can only handle 512 tokens, while new techniques allow to scale to a hundred thousand tokens. This is an essential thing to look into when picking a pre-trained model! You cannot simply pass entire books to transformers, expecting they will be able to summarize them.

Limited interpretability: Transformers are often criticized for their lack of interpretability.
