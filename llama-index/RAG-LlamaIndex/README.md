# RAG workflow. From basic to advanced.

This project focuses on enhancing the GPT Documents chatbot by introducing several innovative features across different stages of development, aimed at improving user interaction, search accuracy, and response quality. 

![](https://github.com/felipearosr/GPT-Documents/blob/main/1.Streaming%20-%20Memory%20-%20Sources/images/RAG.gif)

## Project Overview:

1. **ChatBot with Streaming, Memory, and Sources**: The initial version introduces streaming for real-time response delivery, memory for contextual conversations, and source indication for transparency. Technologies like Llama-index and Chainlit are utilized to facilitate a more intuitive and informative chatbot experience.

2. **Vector DB Integration, Hybrid Retriever, and Advanced Ingestion**: Subsequent updates include Pinecone integration for efficient vector data handling, a hybrid retriever combining dense and sparse vector methods for improved search relevance, and advanced ingestion techniques for better document retrieval and processing.

3. **Reranker, Query Transformations, and Response Synthesis**: Further enhancements incorporate the Cohere reranker for semantic document reordering, multi-step query transformations for detailed query processing, and response synthesis methods for generating more accurate and comprehensive answers.

4. **Evaluation - Generation - Optimization:** This stage involves the systematic generation and evaluation of the RAG in the following metrics; correctness, relevancy, faithfulness and context similarity.

5. **Intent Detection Agent:** Integration of an agent for effective user intent detection, streamlining the query process and enabling more efficient and precise information retrieval by redirecting queries to a more compact and cost-efficient language model.

## Key Features and Improvements:

- **Real-time Interaction**: Implements streaming to deliver answers swiftly, enhancing user experience.
  
- **Conversational Memory**: Employs memory capabilities to provide context-aware responses based on previous interactions.
  
- **Source Transparency**: Indicates the origin of the chatbot's responses, building user trust.

- **Efficient Data Handling**: Utilizes Pinecone for optimized vector data management, enabling faster and more relevant search results.

- **Enhanced Search Accuracy**: Introduces a hybrid retriever that merges dense and sparse search methodologies, offering more precise results.

- **Improved Document Processing**: Incorporates advanced ingestion techniques for various document types, enhancing the chatbot's understanding and retrieval capabilities.

- **Semantic Reranking**: Integrates a reranker to adjust search results based on semantic relevance, ensuring responses align more closely with user queries.

- **Advanced Query Processing**: Applies multi-step query transformations to break down complex inquiries into manageable parts, ensuring thorough exploration of user intents.

- **Dynamic Response Generation**: Adopts multiple response synthesis methods, tailoring the chatbot's replies to user needs and ensuring comprehensive and detailed answers.

This project represents a comprehensive approach to developing a sophisticated chatbot capable of real-time interaction, contextual understanding, and accurate information retrieval, all while maintaining transparency and user trust.


## Roadmap

The order might change, and points might be added.

- [x] Chat Streaming
- [X] Memory
- [x] Sources
- [x] Pinecone Pod
- [ ] Pinecone Serverless
- [x] Implementing HybridSearch Retriever
- [x] Implementing better ingestion 
- [x] Add evaluation
- [x] Create set of documents and questions for evaluation
- [ ] Trying out agents
- [ ] Prompting
- [x] Trying out Query Transformations 
- [ ] Implementing a llm router
- [ ] Trying out GPT as a reranker and comparing it with others
- [ ] Adding Mistral and Llama examples
- [ ] Adding jupyter files to each subproject.
- [x] Intent Detection, using 3.5T for some easy tasks.
