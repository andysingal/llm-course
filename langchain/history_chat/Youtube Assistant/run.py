#import agent
from agent import agent

import warnings, asyncio, os, uuid
warnings.filterwarnings('ignore')

# FastAPI related
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile

 
os.makedirs('temp', exist_ok=True)

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]

app = FastAPI(middleware=middleware, version='v0.1', title='AI Tutor',
                description="<b>Chatbot to answer user queries</b></br></br>")

#default API
@app.get("/")
def home():
    return {'type': 'Langchain based Chatbot'}


#API to chat with chatbot
@app.post('/chat')
async def chat(user_question, file: UploadFile=File(None)):  #takes user question and uploaded image file
    await asyncio.sleep(0.001)
    try:
        image_path = os.path.join('temp', uuid.uuid4().hex[:8]+'.'+str(file.filename).strip().split(".")[-1].strip())
        with open(image_path, mode="wb") as file_on_disk:
            file_contents = await file.read()
            file_on_disk.write(file_contents)
            suffix = image_path.split('.')[-1].strip().lower()
            if suffix not in ['png', 'jpg', 'jpeg']:
                try:
                    os.remove(image_path)
                except:
                    pass
                return {"Error": 'Upload only images with extensions JPG, PNG or JPEG'}
    except:
        image_path = ''
        
    response = agent.invoke({'user_question': user_question, 'image_path': image_path, 'human_input': ''})
    # print("Response: ", response['output'])
    try:
        os.remove(image_path)
    except:
        pass
    return response['output'].replace('{\"__arg1\": \"\"}\n','').strip()
        
 
    
