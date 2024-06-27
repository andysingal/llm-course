from fiddlecube import FiddleCube

fc = FiddleCube(api_key="<api-key>")
dataset = fc.generate(
    [
        "The cat did not want to be petted.",
        "The cat was not happy with the owner's behavior.",
    ],
    2,
)
print("==dataset==", dataset)

debug = [
    {
        "query": "What is the capital of France?",
        "answer": "Paris",
        "prompt": "You are an expert at answering hard questions.",
        "context": ["Paris is the capital of France."],
    }
]
diagnosis = fc.diagnose(debug)
print("==diagnosis==", diagnosis)
