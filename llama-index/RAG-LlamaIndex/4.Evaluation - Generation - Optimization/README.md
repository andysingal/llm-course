# Evaluation, generation and optimization

> [!IMPORTANT] 
> Optimization is untested and likely unfinished.

## Table of Contents

1. [Installation Instructions](#installation-instructions)
2. [Usage](#usage)
3. [Generation](#generation)
4. [Evaluation](#evaluation)
10. [Testing](#tested)

## Installation Instructions

Follow these steps to set up the GPT Documents chatbot on your local machine:

1. Create a conda environment:

   ```shell
   conda create -n rag python==3.11 -y && source activate rag
   ```

2. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

3. Load your documents into the vector store by: 
    - Create a folder named 'data'.
    - Place your documents inside the 'data' folder.
    - Execute the 'ingest.py' script to initiate the loading process.

## Usage

Once the setup is complete, launch the chainlit app using the following command:

```shell
chainlit run -w main.py
```

Feel free to explore the functionalities and contribute to the development of this project. Your feedback and contributions are highly appreciated!

## Generation

### Why is it important?

The creation of a dataset is crucial for developing and refining a RAG. These systems combine the capabilities of information retrieval and generative language models to provide answers that are both relevant and contextually accurate. By generating and using a labeled dataset, we can train, test, and improve the RAG models more effectively, ensuring that they provide high-quality, contextually relevant answers based on the information retrieved.

### What are we generating?

We are generating a `LabelledRagDataset`. This dataset is designed to train and test Retriever-Augmented Generation systems. You can generate this dataset by hand or with the help of a large language model (LLM), such as GPT-4. For the purposes of this example, we are generating it with `gpt-4`.

The dataset consists of the following structured data:

```json
{
   "query": "Query",
   "query_by": {
      "model_name": "gpt-4",
      "type": "ai"
   },
   "reference_contexts": [
      "context_1",
      "context_2"
   ],
   "reference_answer": "answer",
   "reference_answer_by": {
      "model_name": "gpt-4",
      "type": "ai"
   }
},
```

Each entry in the dataset includes:

- `query`: The question or prompt that the RAG system needs to respond to.
- `query_by`: Information about how or by whom the query was generated, it can be a model or a person.
- `reference_contexts`: An array of texts that provide relevant information or context to the query. These are the pieces of information that the retriever component is expected to fetch, which will aid the generator in crafting a coherent and contextually appropriate response.
- `reference_answer`: The correct or expected answer to the query, which will be used as the ground truth for evaluating the RAG system's performance.
- `reference_answer_by`: Information about how or by whom the reference answer was generated. This could be a human annotator or an AI model.

This structure allows for the comprehensive training and evaluation of RAG systems, ensuring they can effectively retrieve relevant information and generate appropriate responses. 

### How do we implement it?

The implementation is super easy thanks to LlamaIndex.

```python
dataset_generator = RagDatasetGenerator.from_documents(
   documents,
   llm=llm,
   num_questions_per_chunk=1,
   show_progress=True,
)

rag_dataset = dataset_generator.generate_dataset_from_nodes()
```

## Evaluation

### Why is evaluation important?

Evaluation is crucial for measuring the performance and guiding the improvement of Retriever-Augmented Generation (RAG) systems. It ensures that these systems produce accurate, relevant, and contextually appropriate responses. By evaluating various metrics, we can identify areas of strength and weakness, benchmark against other systems, and refine our approach for better outcomes.

We assess the following metrics:

- **Mean Correctness Score**: Accuracy of the generated answers.
- **Mean Relevancy Score**: Relevance of the retrieved documents to the query.
- **Mean Faithfulness Score**: Adherence of the responses to the retrieved information.
- **Mean Context Similarity Score**: Similarity of the responses to the query and document context.

These metrics collectively help ensure the RAG system meets quality standards and user needs.

### Notes

In the process of adjusting my pipeline within `main.py`, several modifications were necessary. Notably, due to the limitations of using a trial API key for Cohere, I was unable to perform evaluations as initially intended. This constraint has influenced the functionality of the RAG, rendering my current results less applicable. If you have access to a full API key and can conduct the evaluation, I encourage you to share your findings through a pull request.

Additionally, I disabled streaming functionality to accommodate these changes. This decision may affect the overall operation and efficiency of the system.

I acknowledge that my current implementation might not be optimal. I am planning to revisit and refine it to enhance performance and reliability. Your feedback and contributions are highly welcomed to help improve this project.

---

## Testing
| Tested       | Function        | Last Time Tested | Notes                      |
|:-------------|:----------------|:-----------------|:---------------------------|
| ✅           | Generation      | 2023-03-14       |                            |
| ✅           | Evaluation      | 2023-03-14       | Had to change some things in main.py, this is the [notes](#notes) above.                           |
| ❌           | Optimization    | Untested         |                            |