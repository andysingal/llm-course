# FiddleCube - Generate ideal question-answers for testing RAG

FiddleCube generates an ideal question-answer dataset for testing your LLM. Run tests on this dataset before pushing any prompt or RAG upgrades.

## Quickstart

### Install FiddleCube

```bash
pip3 install fiddlecube
```

### API Key

Get the API key [here](https://dashboard.fiddlecube.ai/api-key).

### Usage

```python
from fiddlecube import FiddleCube

fc = FiddleCube(api_key="<api-key>")
dataset = fc.generate(
    [
        "Wheat is mainly grown in the midlands and highlands of Ethiopia.",
        "Wheat covers most of the country's agricultural land next to teff, corn and sorghum and in the 2009/10 crop season 1.69 million hectares were covered by wheat crops",
        "46.42 million quintals of production was obtained and the average yield was 26.75 quintals per hectare.",
        "Bread wheat (Triticum aestivum L) and durum wheat (Triticum turgidum var durum L) are the types of wheat that are mainly produced in our country, and durum wheat is one of the native wheat crops.",
        "Ethiopia is known to be the primary source of durum wheat and a source of its biodiversity.",
        "Durum wheat is grown in high and medium altitude areas and clay and light soils, and its industrial demand is increasing from time to time.",
    ],
    3,
)
dataset
```

```json
{
    "results": [
        {
            "query": "Where is wheat primarily cultivated in Ethiopia?",
            "contexts": [
                "Wheat is mainly grown in the midlands and highlands of Ethiopia."
            ],
            "answer": "\"Wheat is primarily cultivated in the midlands and highlands of Ethiopia.\"",
            "score": 0.8,
            "question_type": "SIMPLE"
        },
        {
            "query": "If wheat, teff, corn and sorghum are the main crops, what was the coverage of wheat crops in the 2009/10 season?",
            "contexts": [
                "Wheat covers most of the country's agricultural land next to teff, corn and sorghum and in the 2009/10 crop season 1.69 million hectares were covered by wheat crops"
            ],
            "answer": "1.69 million hectares",
            "score": 0.8,
            "question_type": "CONDITIONAL"
        },
        {
            "query": "What was the total production obtained as mentioned in the context? A) 46.42 million quintals B) 26.75 million quintals C) 26.75 quintals D) 46.42 quintals per hectare",
            "contexts": [
                "46.42 million quintals of production was obtained and the average yield was 26.75 quintals per hectare."
            ],
            "answer": "Answer: A) 46.42 million quintals\n\nExplanation: The context information clearly states that \"46.42 million quintals of production was obtained,\" which directly corresponds to option A. The other options do not accurately reflect the total production mentioned in the context. Option B incorrectly combines the average yield figure with \"million quintals,\" option C provides only the average yield per hectare without the \"million\" scale, and option D incorrectly suggests that the production figure is a rate per hectare, rather than a total quantity.",
            "score": 0.8,
            "question_type": "MCQ"
        }
  ],
  "status": "COMPLETED",
  "num_tokens_generated": 44,
  "rate_limited": false
}
```

## Ideal QnA datasets for testing, eval and training LLMs

Testing, evaluation or training LLMs requires an ideal QnA dataset aka the golden dataset.

This dataset needs to be diverse, covering a wide range of queries with accurate responses.

Creating such a dataset takes significant manual effort.

As the prompt or RAG contexts are updated, which is nearly all the time for early applications, the dataset needs to be updated to match.

## FiddleCube generates ideal QnA from vector embeddings

- The questions cover the entire RAG knowledge corpus.
- Complex reasoning, safety alignment and 5 other question types are generated.
- Filtered for correctness, context relevance and style.
- Auto-updated with prompt and RAG updates.

## Roadmap

- [x] Question-answers, complex reasoning from RAG
- [ ] Multi-turn conversations
- [ ] Evaluation Setup - Integrate metrics
- [ ] CI setup - Run as part of CI/CD pipeline
- [ ] Diagnose failures - step-by-step analysis of failed queries

## More Questions?

[Book a demo](https://cal.com/kaushiks/fc)  
Contact us at [founders@fiddlecube.ai](mailto:founders@fiddlecube.ai) for any feature requests, feedback or questions.
