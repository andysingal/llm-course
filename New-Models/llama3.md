1. ```py
   pip install -U "huggingface_hub[cli]"
   ```
 2. Log in to your Hugging Face account: ```py  huggingface-cli login ```
 3. Download the model ```py huggingface-cli download meta-llama/Meta-Llama-3-8B-Instruct --exclude "original/*" --local-dir meta-llama/Meta-Llama-3-8B-Instruct ```
 4. ```py pip install accelerate transformers bitsandbytes```
 5. 
  ```py  import torch
import transformers

class Llama3:
    def __init__(self, model_path):
        self.model_id = model_path
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=self.model_id,
            model_kwargs={
                "torch_dtype": torch.float16,
                "quantization_config": {"load_in_4bit": True},
                "low_cpu_mem_usage": True,
            },
        )
        self.terminators = [
            self.pipeline.tokenizer.eos_token_id,
            self.pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
        ]
  
    def get_response(
          self, query, message_history=[], max_tokens=4096, temperature=0.6, top_p=0.9
      ):
        user_prompt = message_history + [{"role": "user", "content": query}]
        prompt = self.pipeline.tokenizer.apply_chat_template(
            user_prompt, tokenize=False, add_generation_prompt=True
        )
        outputs = self.pipeline(
            prompt,
            max_new_tokens=max_tokens,
            eos_token_id=self.terminators,
            do_sample=True,
            temperature=temperature,
            top_p=top_p,
        )
        response = outputs[0]["generated_text"][len(prompt):]
        return response, user_prompt + [{"role": "assistant", "content": response}]
    
    def chatbot(self, system_instructions=""):
        conversation = [{"role": "system", "content": system_instructions}]
        while True:
            user_input = input("User: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting the chatbot. Goodbye!")
                break
            response, conversation = self.get_response(user_input, conversation)
            print(f"Assistant: {response}")
  
if __name__ == "__main__":
    bot = Llama3("/workspace/meta-llama/Meta-Llama-3-8B-Instruct")
    bot.chatbot()
    ```
    
