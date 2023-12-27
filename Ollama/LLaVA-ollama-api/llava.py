import subprocess
import argparse
import requests
import base64
import time
import json
import sys

# note: including the start server code in this script for demo purposes. You might want to seperately start the server so that you're not starting the server every time you make the call. 
def start_ollama_server():
    try:
        subprocess.Popen(["ollama", "run", "llava"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Starting Ollama server with LLaVa...")
        time.sleep(5)  # Wait a bit for the server to start
    except FileNotFoundError:
        print("Error: Ollama is not installed or not in the PATH.")
        sys.exit(1)

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def analyze_image(image_path, custom_prompt):
    url = "http://localhost:11434/api/generate"
    image_base64 = encode_image_to_base64(image_path)

    payload = {
        "model": "llava",
        "prompt": custom_prompt,
        "images": [image_base64]
    }

    response = requests.post(url, json=payload)

    try:
        # Split the response text into separate lines
        response_lines = response.text.strip().split('\n')

        # Extract and concatenate the 'response' part from each line
        full_response = ''.join(json.loads(line)['response'] for line in response_lines if 'response' in json.loads(line))

        return full_response
    except Exception as e:
        return f"Error: {e}"

def parse_arguments():
    parser = argparse.ArgumentParser(description='LLaVA Image Analysis')
    parser.add_argument('-i', '--image', required=True, help='Path to the image file')
    parser.add_argument('-p', '--prompt', default='Describe this image in detail', help='Custom prompt for image analysis')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    start_ollama_server()
    result = analyze_image(args.image, args.prompt)
    print(" Response:", result)
