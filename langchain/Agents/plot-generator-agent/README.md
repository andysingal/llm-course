# Let's build our first LLM agent


## Table of Contents
- [What is this repo about?](#)
- [How to run the code](#features)
- [Wanna get more hands-on content like this?](#)

## What is this repo about?
In this repository you will find a Python implementation of an LLM agent that can generate visualisations using public data available on the Internet.

### What is an LLM agent?
An agent is essentially a wrapper around your LLM, that provides extra functionality like

- Tool usage. The LLM is able to select and use tools, like internet search, to fetch relevant information it might need to accomplish the task.

- Multi-step reasoning. The LLM can generate a plan, execute it, and adjust it based on the partial outcomes obtained.

The LLM acts as a reasoning machine, that helps the agent choose the sequence of actions to take to solve the task.

Let me show you how to build a ReAct (Reason and Act) agent in Python that can generate the plot we want.


## Run the whole thing in 3 minutes

1. Create Python virtual environment and install all dependencies using Python Poetry
    ```
    $ make install
    ```

2. Set API keys for Tavily and Cohere in an `.env` file
    ```
    $ cp .env.sample .env
    ```
    and replace placeholders with your keys.

3. Ask the agent to generate a plot example
    ```
    $ make run-agent
    ```

## Wanna get more hands-on content like this?

Jon 15k+ builders to the the Real-World ML Newsletter, and learn to build real-world ML products.

-> [Click to join for FREE](https://www.realworldml.net/subscribe)