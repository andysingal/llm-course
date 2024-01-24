"""
Created on Tue Jan 23 2024

This script contains functions for implementing open source Retrieval Augmented Generation (RAG).

Author: Ibrahim Alabi
Email: ibrahimolalekana@u.boisestate.edu
Institution: Boise State University
"""


import os
import sys
import warnings
import transformers
from dotenv import load_dotenv

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate 
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline

load_dotenv() # take environment variables from .env.
api_key = os.getenv("Huggingface_API_key")
model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1" # the model id on 🤗

warnings.filterwarnings('ignore')
transformers.utils.logging.set_verbosity(40)
transformers.utils.logging.disable_progress_bar()



class NaiveRAG:

    def __init__(self, model=None, tokenizer=None):

        if tokenizer is None:
            self.tokenizer = self.do_tokenizer()
        else:
            self.tokenizer = tokenizer
        
        if model is None:
            self.model = self.do_model()
        else:
            self.model = model


    def do_tokenizer(self):
        tokenizer_ = transformers.AutoTokenizer.from_pretrained(
            model_id,
            token=api_key,
            padding_side='left'
        )
        return tokenizer_
    
    def do_model(self):

        model_config = transformers.AutoConfig.from_pretrained(
            model_id,
            token=api_key
        )

        model = transformers.AutoModelForCausalLM.from_pretrained(
            model_id,
            trust_remote_code=True,
            config=model_config,
            device_map='auto',
            token=api_key,
            load_in_4bit=True
        )

        hf_pipeline = transformers.pipeline(
            model=model.eval(), 
            tokenizer=self.tokenizer,
            return_full_text=True,  
            task='text-generation',
            framework="pt",
            temperature=0.1,
            max_new_tokens=512,  
            repetition_penalty=1.1, 
            do_sample=True, 
        )

        local_llm =HuggingFacePipeline(
            pipeline=hf_pipeline,
        )
        return local_llm
    
    def text_to_mixtral_template(self, instruction: str, safety_mode: bool = True) -> str:

        if safety_mode:
            safety_prompt = (
                "Always assist with care, respect, and truth. Respond with utmost utility yet securely. "
                "Avoid harmful,unethical, prejudiced, or negative content. Ensure replies promote fairness and positivity."
            )
            
            instruction = f"{safety_prompt} {instruction}"
        
        chat = [
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I'm doing great. How can I help you today?"},
            {"role": "user", "content": instruction}
        ]

        hf_output = self.tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=False)

        return hf_output
    
    def text_with_context_to_mixtral_template(self, instruction: str, context: str, safety_mode: bool = True) -> str:

        context_instruction = f"Answer the following question using the provided context. \n\ncontext: {context}"

        if safety_mode:
            safety_prompt = (
                "Always assist with care, respect, and truth. Respond with utmost utility yet securely. "
                "Avoid harmful,unethical, prejudiced, or negative content. Ensure replies promote fairness and positivity."
            )
            
            instruction = f"{safety_prompt}\n\n{context_instruction} \n\nquestion:{instruction}"

        else:
            instruction = f"{context_instruction} \n\nquestion:{instruction}"
        
        chat = [
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I'm doing great. How can I help you today?"},
            {"role": "user", "content": instruction}
        ]

        return self.tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=False)
    
    
    def qa_with_context(self, question: str, context: str, model_template=None, safety_mode: bool = True) -> str:
        input_text="{question}"
        input_context="{context}"

        if model_template is None:
            template = self.text_with_context_to_mixtral_template(instruction=input_text, context=input_context, safety_mode=safety_mode)

        else:
            template = model_template

        prompt_template = PromptTemplate(template=template, input_variables=["question", "context"])
        llm_chain = LLMChain(prompt=prompt_template, llm=self.model)
        result=llm_chain.invoke({"question": question, "context": context})
        return result['text'].strip()
    
    def qa(self, question: str, model_template=None, safety_mode: bool = True) -> str:
        input_text="{question}"

        if model_template is None:
            template = self.text_to_mixtral_template(instruction=input_text, safety_mode=safety_mode)
        
        else:
            template = model_template

        prompt_template = PromptTemplate(template=template, input_variables=["question"])
        llm_chain = LLMChain(prompt=prompt_template, llm=self.model)
        result=llm_chain.invoke(question)
        return result['text'].strip()
    
if __name__ == "__main__":

    # Running the script on a command-line only supports question without contex.

    rag = NaiveRAG()
    query = None

    if len(sys.argv) > 1:
        query = sys.argv[1]

    print(">> Bot: How can I help you today?")
    while True:
        if query is None:
            query = input(">> User: ")

            if query in ["exit", "quit", "q", "q()"]:
                print(">> Bot: Goodbye!")
                sys.exit(0)
        response = rag.qa(question=query)
        print(response)
        query = None
