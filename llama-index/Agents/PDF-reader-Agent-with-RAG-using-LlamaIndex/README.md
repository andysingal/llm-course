# PDF-reader-Agent-with-RAG-using-LlamaIndex


This is a tutorial for building an advanced AI agent that uses multiple LLMs (Large Language Models) locally on your computer. The agent will be able to read and understand code written in Python and then generate new code based on the existing code.

Here are the tools and technologies used:
* LlamaIndex: An open-source framework for building LLM applications. It helps with loading data, passing data to different LLMs, and parsing outputs.
* OLama: A tool that allows you to run open-source LLMs locally on your computer.
* Llama Parse: A tool from LlamaIndex that helps with parsing the outputs from different LLMs.

Here are the steps involved in building the AI agent:
1. Install the required dependencies: LlamaIndex, OLama, and other necessary libraries.
2. Set up Llama Index and configure it to use the local OLama models.
3. Define the data directory containing the code files that the agent will read from.
4. Write Python code to load the data using LlamaIndex's directory reader.
5. Create a vector store index to store the vector embeddings of the code files.
6. Use a query engine to process the code files and extract the relevant information.
7. Define multiple tools for the AI agent, including one for reading API documentation (using a PDF reader) and another for reading Python code.
8. Implement the logic for the AI agent to take a prompt from the user and decide which tool(s) to use.
9. Use the outputs from the chosen tools to generate new code.
10. Save the generated code to a file.
 
 
The agent is given a prompt to read a Python file and write a simple unit test for the API. The agent successfully generates some Python code that performs the unit test.

Note that the accuracy of the generated code may not be perfect because the local models have limited capabilities. However, this provides a good introduction to building advanced AI agents that can process and generate code using multiple LLMs.

Referance:  https://www.youtube.com/watch?v=JLmI0GJuGlY
