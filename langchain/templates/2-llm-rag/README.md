# AI for Web Devs 2: Custom Offline LLM RAG with OpenSearch

## First time setup

### Project

- `cp .env.example .env`

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

- [Elastic: What is RAG](https://www.elastic.co/what-is/retrieval-augmented-generation)
- [Wiki: Bag of Words Model](https://en.wikipedia.org/wiki/Bag-of-words_model)
- [A Gentle Introduction to Bag Words Model](https://machinelearningmastery.com/gentle-introduction-bag-words-model/)
- [Wiki: BM25 Search Function](https://en.wikipedia.org/wiki/Okapi_BM25)
- [Vector vs Keyword search](https://about.xethub.com/blog/you-dont-need-a-vector-database)
- [ChromaDB](https://www.trychroma.com)
- [Elasticsearch](https://www.elastic.co)
- [OpenSearch](https://opensearch.org)
- [Infinity Embedding Server](https://github.com/michaelfeil/infinity)
- [LangChain](https://www.langchain.com)
- [Elastic Sparse Encoder Model](https://www.elastic.co/search-labs/blog/may-2023-launch-sparse-encoder-ai-model)
- [OpenSearch Sparse Encoding Models](https://opensearch.org/docs/2.13/ml-commons-plugin/pretrained-models/#sparse-encoding-models)
- [Elasticsearch Labs](https://github.com/elastic/elasticsearch-labs)
