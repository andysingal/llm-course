import torch
from PIL import Image
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import List, Union, Dict, Optional
from transformers import AutoModelForCausalLM, AutoProcessor, BitsAndBytesConfig
import time
import os

app = FastAPI()
model_name = os.getenv('MODEL_NAME', 'microsoft/Phi-3-vision-128k-instruct')
print(f'model: {model_name}\n')

# Current resource plan(infer.s/m/l) of SAP AI Core has only one V100 GPU
device = 'cuda:0'

class ImageUrl(BaseModel):
    url: HttpUrl

class Content(BaseModel):
    type: str
    text: Union[str, None] = None
    image_url: Union[ImageUrl, None] = None

class Message(BaseModel):
    role: str
    content: Union[str, List[Content]]

class ChatCompletionRequest(BaseModel):
"""
Class implements an OpenAI-like chat completion request
"""
    messages: List[Message]
    model: str
    temperature: float = 0.7
    max_new_tokens: int = 2048
    do_sample: bool = True

class ResponseMessage(BaseModel):
    role: str
    content: str

class Choice(BaseModel):
    index: int
    message: ResponseMessage
    logprobs: Optional[Union[None, dict]] = None
    finish_reason: str

class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ChatCompletionResponse(BaseModel):
"""
Class implements an OpenAI-like chat completion response
"""
    id: str
    object: str
    created: int
    model: str
    system_fingerprint: str
    choices: List[Choice]
    usage: Usage

class ChatModel:
"""
A wrapper class of the inference engine of large language models with hugging face transformers library.
It holds a list of model and processor, no model swapping with current implmentation
-get_model(): download and load model
-generate_response(): inference the model with input request of ChatCompletionRequest and generate the responses of ChatCompletionResponse.
"""
    def __init__(self):
        self.models = {}
        self.get_model()

    def get_model(self, model_id=model_name):
        print('get_model: start to download the model')
        if model_id not in self.models:
            model = AutoModelForCausalLM.from_pretrained(
                model_id, 
                device_map=device,
                trust_remote_code=True, 
                torch_dtype=torch.bfloat16,
                _attn_implementation='eager',
                #_attn_implementation='flash_attention_2', # V100(resource plan infer.s/m/l) not supported yet. https://github.com/Dao-AILab/flash-attention/issues/535
                quantization_config=BitsAndBytesConfig(load_in_8bit=True),
            )

            processor = AutoProcessor.from_pretrained(model_id, 
                                                      trust_remote_code=True)
            self.models[model_id] = (model, processor)
        return self.models[model_id]

    async def generate_response(self, request: ChatCompletionRequest):
        print(f'Request>>>\n{request}')

        model_id = request.model
        messages = request.messages

        model, processor = self.get_model(model_id)

        # Preprocess the user message type with <|image_1|>\n
        messages_with_image_tag = []
        images = None
        
        # default_image_text = 'What is in the this image?'
        default_image_text = ''
        i = 1
        image_url = None
        for message in request.messages:
            if message.role == 'user':
                content = message.content
                if isinstance(content, list):
                    for item in content:
                        if item.type == 'image_url':
                            text_content = next((x.text for x in content if x.type == 'text'), default_image_text)
                            messages_with_image_tag.append({'role': 'user', 'content': f'<|image_{i}|>\n{text_content}'})
                            
                            # Important: phi3-vision can support only one single image as of June 14 2024
                            image_url = item.image_url.url

                            # Implementation for multiple images support.
                            # i = i +1
                            # image = Image.open(requests.get(item.image_url.url, stream=True).raw)
                            # if i == 1:
                            #     images=[]
                            # images.append([image])

                            break
                else:
                    # text only message
                    messages_with_image_tag.append(message)
            else:
                # system or assistant message
                messages_with_image_tag.append(message)
        print(f'messages_with_image_tag>>>\n{messages_with_image_tag}')

        prompt = processor.tokenizer.apply_chat_template(messages_with_image_tag, 
                                                         tokenize=False, 
                                                         add_generation_prompt=True)
        if prompt.endswith('<|endoftext|>'):
            prompt = prompt.rstrip('<|endoftext|>')

        print(f'propmt>>>\n{prompt}')
        
        if not image_url:
            print('No image_url found in the request. It is a text-only request.')
        else:
            image = Image.open(requests.get(image_url, stream=True).raw)
            images = [image]
        
        inputs = processor(prompt, 
                           images=images, 
                           return_tensors='pt').to("cuda:0")   
        prompt_tokens = inputs['input_ids'].shape[1]
        print(f"prompt_tokens: {prompt_tokens}\n")

        generation_args = {
            'max_new_tokens': request.max_new_tokens,
            'temperature': request.temperature,
            'do_sample': request.do_sample
        }

        print(f'\ngeneration_args>>>\n{generation_args}\n')
    
        generate_ids = model.generate(**inputs, 
                                      eos_token_id=processor.tokenizer.eos_token_id, 
                                      **generation_args)
        # Calculate total_tokens as the length of the combined input and output tokens
        total_tokens = generate_ids.shape[1]
        print(f"total_tokens: {total_tokens}\n")

        # Remove input tokens
        generate_ids = generate_ids[:, inputs['input_ids'].shape[1]:]

        # Calculate completion_tokens as the length of the combined input and output tokens
        completion_tokens = generate_ids.shape[1]
        print(f"completion_tokens: {completion_tokens}\n")
        
        response = processor.batch_decode(generate_ids, 
                                          skip_special_tokens=True, 
                                          clean_up_tokenization_spaces=False)[0]

        print(f'generated response>>>\n{response}')

        utc_time_epoch = int(time.time())
        chat_completion_resp = ChatCompletionResponse(
            id = f'{utc_time_epoch}',
            object = 'chat.completion',
            created = utc_time_epoch,
            model = model_id,
            system_fingerprint = 'fp_44709d6fcb',
            choices=[
                Choice(
                    index = 0,
                    message=ResponseMessage(
                        role = 'assistant',
                        content = response
                    ),
                    logprobs = None,
                    finish_reason = 'stop'
                )
            ],
            usage=Usage(
                prompt_tokens = prompt_tokens,
                completion_tokens = completion_tokens,
                total_tokens = total_tokens
            )
        )

        print(f'chat_completion_resp>>>\n{chat_completion_resp}')
        return chat_completion_resp

# Initialize an instance for ChatModel
chat_model = ChatModel()

# OpenAI-compatible chat completions endpoint
@app.post('/v1/chat/completions')
async def generate_response(request: ChatCompletionRequest):
    return await chat_model.generate_response(request)

# Running the app using uvicorn
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)