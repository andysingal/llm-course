# Technology

* PydanticAI
* Tavily - Search
* OpenAI - GPT 4o-mini
* Markdown

# Workflow

* Agent
    * Search for appsec news from the last week - based on today's date
    * Write it in a particular format - markdown. each story is going to have header and a brief explanation
    * Save it in a file

## Steps to run

* Clone the repo

* Install dependencies

```bash
uv sync
```

* Run the agent

```bash
uv run research_agent.py
```