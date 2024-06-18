install:
	@echo "Installing dependencies"
	curl -sSL https://install.python-poetry.org | python3 -
	poetry install

run-llm:
	poetry run python src/models.py \
		--input "Create a plot with Python of the number of games won by the Golden State Warriors in each of the last 2 NBA seasons." \
		--model_name gpt-3.5-turbo \
		--model_provider openai

run-agent:
	poetry run python src/agent.py \
		--input "Create a plot of the number of games won by the golden state warriors in each of the last 2 seasons. Save the plot as a png file under plots/warriors_victories.png" \
		--model_name command-r-plus \
		--model_provider cohere
lint:
	@echo "Fixing linting issues"
	poetry run ruff check --fix .

format:
	echo "Formatting Python code"
	poetry run ruff format .