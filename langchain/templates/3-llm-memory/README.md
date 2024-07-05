# AI for Web Devs 3: Custom Offline LLM Chat Memory

## First time setup

### Project

- `cp .env.example .env`

#### DB / SQLAlchemy

```sh
docker exec -it chat_web flask db init
docker exec -it chat_web flask db migrate -m "Initial migration"
docker exec -it chat_web flask db upgrade
docker exec -it chat_web flask db_seed

# One liner wipe and reset DB
docker exec -it chat_db psql -U app -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"; rm -rf app/migrations; docker exec -it chat_web flask db init; docker exec -it chat_web flask db migrate -m "Initial migration"; docker exec -it chat_web flask db upgrade; docker exec -it chat_web flask db_seed
```

### Ollama

_https://ollama.com/library_

- `docker exec -it chat_ollama ollama run {MODEL NAME}`
- `docker exec -it chat_ollama ollama run tinydolphin`

### Svelte

- `cd components/chat`
- `npm i`

### Link build output to Flask static

- force the output to not include hash (vite config)
- add command to build and watch (package json)
- symlink component output from flask static dir
  - `cd app/static`
  - `mkdir components`
  - `cd components`
  - `ln -s ./../../components/chat/dist/assets ./chat`

## Start the stack

- `docker compose up --build`

## Resources

- [OpenAI Chat API Docs](https://platform.openai.com/docs/api-reference/chat/create)
- [Ollama Chat API Docs](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-chat-completion)
- [Postgres](https://www.postgresql.org)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/)
- [Flask-Migrate](https://github.com/miguelgrinberg/flask-migrate)
- [SQLAlchemy-serializer](https://github.com/n0nSmoker/SQLAlchemy-serializer)
