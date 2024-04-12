import os
import openai
import asyncio

from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.core.llama_pack import download_llama_pack
from llama_index.core.llama_dataset import LabelledRagDataset
from main import load_query_engine, load_index

openai.api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("MODEL", "gpt-4-0125-preview")
print(f"model = {model}")
Settings.model = OpenAI(model=model)


async def evaluate():
    rag_dataset = LabelledRagDataset.from_json("./data/rag_dataset.json")
    print("Rag dataset loaded")
    index = load_index()
    print("Index loaded")
    query_engine = load_query_engine(index)
    print("Query engine loaded")
    RagEvaluatorPack = download_llama_pack("RagEvaluatorPack", "./rag_evaluator_pack")
    print("RagEvaluatorPack downloaded")
    rag_evaluator_pack = RagEvaluatorPack(
        rag_dataset=rag_dataset, query_engine=query_engine
    )
    print("RagEvaluatorPack created")
    ############################################################################
    # NOTE: If have a lower tier subscription for OpenAI API like Usage Tier 1 #
    # then you'll need to use different batch_size and sleep_time_in_seconds.  #
    # For Usage Tier 1, settings that seemed to work well were batch_size=5,   #
    # and sleep_time_in_seconds=15 (as of December 2023.)                      #
    ############################################################################
    benchmark_df = await rag_evaluator_pack.arun(
        batch_size=20,  # batches the number of openai api calls to make
        sleep_time_in_seconds=1,  # seconds to sleep before making an api call
    )
    print("Benchmarking complete")
    benchmark_df.to_csv("benchmark.csv", index=True)


if __name__ == "__main__":
    asyncio.run(evaluate())
