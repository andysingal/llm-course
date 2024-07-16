from transformers import TFAutoModelForSeq2SeqLM, AutoTokenizer
from huggingface_hub import HfApi, HfFolder

# Load your model and tokenizer
model_checkpoint = "Helsinki-NLP/opus-mt-en-hi"
model = TFAutoModelForSeq2SeqLM.from_pretrained("model/")
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

tokenizer.save_pretrained("tokenizer/")

# Define your repository name
repo_name = "shinigami-srikar/langgpt-pretrained"

# Create the repository if it doesn't exist
api = HfApi()
api.create_repo(repo_name)

# Push model and tokenizer to the hub
model.push_to_hub(repo_name)
tokenizer.push_to_hub(repo_name)
