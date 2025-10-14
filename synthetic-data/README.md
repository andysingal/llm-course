[Synthetic Data Generator](https://huggingface.co/spaces/argilla/synthetic-data-generator)


[docker support](https://buff.ly/49IDSmd)

[Synthetic Data Generation sdv](https://github.com/Zhenna/synthetic_data_generation_tabular_experiments/blob/main/sdv_notebook.ipynb)

[Synthetic-sdv](https://colab.research.google.com/drive/1L6i-JhJK9ROG-KFcyzT9G-8FC3L8y8Lc#scrollTo=eO3bqE0dOf6a)



### Videos

[Genkit + NodeJS + Gemini](https://www.youtube.com/watch?v=AY6HY6Wofnc)

Articles

[Think Inside the JSON: A Reinforcement Strategy for Strict LLM Schema Adherence](https://www.mastercontrol.com/gxp-lifeline/thinkjson-ai-solution-for-life-science-manufacturing/)

[Synthetic Data in the Era of LLMs](https://synth-data-acl.github.io/)

[How to Evaluate Your RAG Pipeline with Synthetic Data?](https://www.marktechpost.com/2025/10/13/how-to-evaluate-your-rag-pipeline-with-synthetic-data/)

```py
from deepeval.synthesizer import Synthesizer

synthesizer = Synthesizer(model="gpt-4.1-nano")

# Generate synthetic goldens from your document
synthesizer.generate_goldens_from_docs(
    document_paths=["example.txt"],
    include_expected_output=True
)

# Print generated results
for golden in synthesizer.synthetic_goldens[:3]:  
    print(golden, "\n")
```
