
1. ```ollama run llama3```
2. ```mkdir ollama-webui```
3. ```cd ollama-webui```
4. Stop and Remove Existing Containers
If you have any Docker containers already running, you will need to stop and remove them before proceeding. To do this, run the following command:
```py
docker stop $(docker ps -q)
docker rm $(docker ps -q -a)
```
5. Docker Compose
```
version: '3.8'

services:
  ollama:
    image: ollama/ollama
    container_name: ollama
    volumes:
      - ollama:/root/.ollama
    ports:
      - "11434:11434"
    restart: unless-stopped
    # GPUを使用する場合、以下の行のコメントを外してください
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - capabilities: [gpu]

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    ports:
      - "3000:8080"
    volumes:
      - open-webui:/app/backend/data
    extra_hosts:
      - "host.docker.internal:host-gateway"
    restart: always

volumes:
  ollama:
  open-webui:
```
6. ```docker-compose up -d```
7. Open WebUI
```
http://localhost:3000/

```

<img width="1471" alt="Screenshot 2024-07-05 at 1 07 39 PM" src="https://github.com/andysingal/llm-course/assets/20493493/fa3444e9-5525-4005-962f-6f9470375f17">

<img width="1696" alt="Screenshot 2024-07-05 at 1 08 59 PM" src="https://github.com/andysingal/llm-course/assets/20493493/b558abc2-8489-4e64-ad55-1f627fa65e6a">

Resources:
[open-webui](https://github.com/open-webui/open-webui) 


