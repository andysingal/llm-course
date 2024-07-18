```py
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

def select_model():
    models = ("GPT-3.5", "GPT-4", "Claude 3.5 Sonnet", "Gemini 1.5 Pro")
    model = st.sidebar.radio("Choose a model:", models)
    if model == "GPT-3.5":
        return ChatOpenAI(model_name="gpt-3.5-turbo")
    elif model == "GPT-4":
        return ChatOpenAI(model_name="gpt-4")
    elif model == "Claude 3.5 Sonnet":
        return ChatAnthropic(model_name="claude-3-5-sonnet-20240620")
    elif model == "Gemini 1.5 Pro":
        return ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")

# モデルの選択と使用
llm = select_model()
response = llm.invoke("AIの未来について教えてください。")
print(response)
```
