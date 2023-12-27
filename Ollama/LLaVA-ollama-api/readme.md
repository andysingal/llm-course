# Hot Dog Not Hotdog Demo with LLaVa API on Ollama

## Introduction
Welcome to the demo app for the "Hot Dog or Not Hot Dog" application, inspired by the classic Silicon Valley show. This app utilizes the LLaVa model, capable of processing both text and images, and runs through the Ollama tool. This README accompanies a video tutorial demonstrating how to use the Ollama tool to run a LLaVa API server. Full code for this demo is available in this folder ( llava.py)

### What is LLaVa?
LLaVa (Multimodal Large Language Model) is an advanced model that understands both images and text, enabling versatile AI applications.

### What is Ollama?
Ollama is a tool that facilitates the easy and efficient running of local Large Language Models (LLMs), as previously discussed in another video.

## Installation and Setup

1. **Install Ollama App:**
   Make sure to have the Ollama app installed, which includes the Ollama CLI.

2. **Run Python Script:**
   Use the provided Python script for image analysis.


### Notes
- The script can also call a remote server hosting your LLaVa model.

## How to Call the Script

After setting up the environment and ensuring that the Ollama server is running, you can call the script from the command line by providing the necessary arguments.

### Usage

Navigate to the directory containing the script and use the following command:

```bash
python llava.py -i <path_to_image> -p "<custom_prompt>"
