What is 𝗖𝗼𝗻𝘁𝗲𝘅𝘁𝘂𝗮𝗹 𝗥𝗲𝘁𝗿𝗶𝗲𝘃𝗮𝗹 and why might it be important for your AI applications?

The idea of Contextual Retrieval was suggested by the Anthropic team late last year. It aims to improve accuracy and relevance of data that is retrieved in Retrieval Augmented Generation based AI systems.

There have been various methods suggested for improving the process before:

➡️ Overlapping chunking.
➡️ Hierarchical chunking.
➡️ …

I personally tried at least a few with different levels of success (they do help). 

However, I love the intuitiveness and simplicity of Contextual Retrieval. And it does provide better results.

𝘗𝘳𝘦𝘱𝘳𝘰𝘤𝘦𝘴𝘴𝘪𝘯𝘨:

𝟭. Split each of your documents into chunks via chosen chunking strategy. 
𝟮. For each chunk separately, add it to a prompt together with the whole document. 
𝟯. Include instructions to situate the chunk in the document and generate short context for it. Pass the prompt to a chosen LLM.
𝟰. Combine the context that was generated in the previous step and the chunk that the context was generated for.
𝟱. Pass the data through a TF-IDF embedder.
𝟲. Pass the data through a LLM based embedding model.
𝟳. Store the data generated in steps 5. and 6. in databases that support efficient search.

𝘙𝘦𝘵𝘳𝘪𝘦𝘷𝘢𝘭:

𝟴. Use user query for relevant context retrieval. ANN search for semantic and TF-IDF index for exact search.
𝟵. Use Rank Fusion techniques to combine and deduplicate the retrieved results and produce top N elements.
𝟭𝟬. Rerank the previous results and narrow down to top K elements.
𝟭𝟭. Pass the result of step 10. to a LLM together with the user query to produce the final answer.

❗️ Step 3. might sound extremely costly and it is, but with Prompt Caching, the costs can be significantly reduced.
✅ Prompt caching can be implemented in both proprietary and open source model cases (remember Cache Augmented Generation?).
