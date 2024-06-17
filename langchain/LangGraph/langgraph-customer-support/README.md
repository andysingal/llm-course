

# Advanced Customer Support control flow with LangGraph🦜🕸

Implementation of a customer support agent that collects user information, validates it, and only then assists the user.
The state is persisted to allow continuation and provide a more advanced user experience.



![Logo](https://github.com/emarco177/langgraph-customer-support/blob/main/static/logo.png)



## Features

- **Human In the Loop**: Continuously gather input from the user until the agent has all required information.
- **Persistent Storage**: Checkpoint LangGraph state after each node execution to an SQLite database.
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`PYTHONPATH=/{YOUR_PATH_TO_PROJECT}/langgraph-customer-support`

`MISTRALAI_API_KEY`

`LANGCHAIN_API_KEY`

`LANGCHAIN_TRACING_V2=true`

`LANGCHAIN_PROJECT`

## Run Locally

Clone the project

```bash
  git clone https://github.com/emarco177/langgraph-customer-support.git
```

Go to the project directory

```bash
  cd langgraph-customer-support
```

Install dependencies

```bash
  poetry install
```

Start the flask server

```bash
  poetry run app.py
```


## Running Tests

To run tests, run the following command

```bash
  poetry run pytest . -s -v
```

## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://www.udemy.com/course/langgraph/?referralCode=FEA50E8CBA24ECD48212)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/eden-marco/)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://www.udemy.com/user/eden-marco/)