import os
import sys
import re
import traceback
import time
from io import StringIO
from openai import OpenAI

llama_api = OpenAI(
    api_key="api_key",  # Change if needed
    base_url="https://your.api.provider/v1/" # Change if needed
)

model_a_id = "meta-llama/Meta-Llama-3.1-8B-Instruct" # Change if needed
model_b_id = "Qwen/Qwen2.5-Coder-32B-Instruct"       # Change if needed

def query_llama(model, messages, stream=False):
    chat_completion = llama_api.chat.completions.create(
        model=model,
        messages=messages,
        stream=stream,
    )
    if stream:
        response = ""
        for chunk in chat_completion:
            content = chunk.choices[0].delta.content
            if content is not None:
                response += content
                sys.stdout.write(content)
                sys.stdout.flush()
        return response
    else:
        return chat_completion.choices[0].message.content.strip()

def chat_model(messages, stream=False):
    global model_a_id
    return query_llama(model_a_id, messages, stream)

def coder_model(messages, stream=False):
    return query_llama(model_b_id, messages, stream)

def run_code(code):
    print("\n\n--- running code")
    old_stdout = sys.stdout
    captured_output = StringIO()
    sys.stdout = captured_output
    try:
        exec(code)
    except Exception as e:
        sys.stdout = old_stdout
        return traceback.format_exc()
    sys.stdout = old_stdout
    print("--- finished running code")
    return captured_output.getvalue()

def main():
    print(f"{os.getcwd()}> python3 explore.py")
    print("LLMs activated!")

    model_a = chat_model
    model_b = coder_model

    conversation = [
        # You can edit the system prompt to let the LLMs do what you want!
        {"role": "system", "content": "You are an LLM inside a folder. You are allowed to run whatever Python code you'd like and do whatever fun things you want to.\n\nThe way you can run code is by saying like this:\n\nRUN-CODE\n```\nprint('Hello World')\n```\n\nHowever, please note that code using input() or internet features like requests won't work. You can also run system commands with the os library. Try to interact with the environment like creating files and checking the current directory, as well as reading files in the current folder. Please note that you MUST say RUN-CODE followed by the code if you want it to run."}
    ]

    while True:
        print(f"\n{model_a_id}:")
        chat_response = model_a(conversation, stream=True)
        conversation.append({"role": "assistant", "name": model_a_id, "content": chat_response})
        time.sleep(3)

        # Check for RUN-CODE
        code_match = re.search(r'RUN-CODE\n```(?:python)?\n(.*?)\n```', chat_response, re.DOTALL)
        if code_match:
            code = code_match.group(1).strip()
            print("\n[code detected]")
            output = run_code(code)
            time.sleep(3)  # Wait 3 seconds after code execution
            content = "The code has been run, and here is the output:\n" + output
            print(f"\n{model_a_id}:\n{content}")
            conversation.append({"role": "assistant", "name": model_a_id, "content": content})
        else:
            print("\nNo code detected, moving on\n\n")
            time.sleep(3)

        # Get Coder response
        print(f"\n{model_b_id}:")
        b_response = model_b(conversation, stream=True)
        conversation.append({"role": "assistant", "name": model_b_id, "content": b_response})
        time.sleep(3)

        # Check for RUN-CODE
        code_match = re.search(r'RUN-CODE\n```\n(.*?)\n```', b_response, re.DOTALL)
        if code_match:
            code = code_match.group(1).strip()
            print("\n[code detected]")
            output = run_code(code)
            time.sleep(3)  # Wait 3 seconds after code execution
            content = "The code has been run, and here is the output:\n" + output
            print(f"\n{model_b_id}:\n{content}")
            conversation.append({"role": "assistant", "name": model_b_id, "content": content})
        else:
            print("\nNo code detected, moving on\n\n")
            time.sleep(3)

if __name__ == "__main__":
    main()
