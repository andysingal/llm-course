[Codestral Mamba](https://mer.vin/2024/07/codestral-mamba-code/)

[CodeAct](https://docs.all-hands.dev/modules/usage/agents)

[code2prompt](https://github.com/mufeedvh/code2prompt/)

[Fine-Tuning of Llama-2 7B Chat for Python Code Generation](https://www.marktechpost.com/2025/02/08/fine-tuning-of-llama-2-7b-chat-for-python-code-generation-using-qlora-sfttrainer-and-gradient-checkpointing-on-the-alpaca-14k-dataset/)


Examples
```py
from  transformers  import  GPT2LMHeadModel , GPT2Tokenizer , TextDataset , DataCollatorForLanguageModeling   
from  transformers  import  Trainer , TrainingArguments 
# Initialize tokenizer and model
tokenizer  =  GPT2Tokenizer . from_pretrained ( "gpt2" )
model  =  GPT2LMHeadModel . from_pretrained ( "gpt2" )
# Assume code_corpus.txt is your code data file
train_file  =  "code_corpus.txt"
# Use tokenizer to process the dataset
def  load_dataset ( file_path ) :
    with  open ( file_path , "r" ) as f :   
        text  =  f . read ( )
    tokenized_text  =  tokenizer . convert_tokens_to_ids ( tokenizer . tokenize ( text ) )
    return  [ tokenizer . build_inputs_with_special_tokens ( tokenized_text ) ]
dataset  =  load_dataset ( train_file )
# Dataset segmentation and processing
train_dataset  =  TextDataset ( dataset )
data_collator  =  DataCollatorForLanguageModeling ( tokenizer = tokenizer , mlm = False ) 
# Set training parameters
training_args  =  TrainingArguments (
    output_dir = "./results" ,
    overwrite_output_dir = True ,
    num_train_epochs = 1 , # More rounds should be set for actual training  
    per_device_train_batch_size = 4 ,
    save_steps = 10_000 ,
    save_total_limit = 2 ,
)
# Create Trainer and start training
trainer  =  Trainer (
    model = model ,
    args = training_args ,
    data_collator = data_collator ,
    train_dataset = train_dataset ,
)
trainer . train ( )
# Generate code example
input_prompt  =  "def add_numbers(a, b):"
input_ids  =  tokenizer . encode ( input_prompt , return_tensors = "pt" ) 
sample_outputs  =  model . generate ( input_ids , max_length = 50 , num_return_sequences = 1 , do_sample = True )   
generated_code  =  tokenizer . decode ( sample_outputs [ 0 ] , skip_special_tokens = True ) 
print ( generated_code )
```
