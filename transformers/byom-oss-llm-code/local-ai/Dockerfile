# Specify the base layers (default dependencies) to use
ARG BASE_IMAGE=localai/localai:master-cublas-cuda11-core
FROM ${BASE_IMAGE}

###################Start of Adapation for SAP AI Core###################
COPY entrypoint.sh /build/

# Update and install dependencies
RUN apt-get update && \
    apt-get install -y \
    ca-certificates \
    nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configure nginx for reverse proxy
RUN echo "events { use epoll; worker_connections 128; } \
    http { \
    server { \
    listen 18080; \
    location /v1/ { \
    proxy_pass http://localhost:8080/; \
    proxy_set_header Host \$host; \
    proxy_set_header X-Real-IP \$remote_addr; \
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for; \
    proxy_set_header X-Forwarded-Proto \$scheme; \
    } \
    } \
    }" > /etc/nginx/nginx.conf && \
    chmod -R 777 /var/log/nginx /var/lib/nginx /run

EXPOSE 18080

RUN mkdir -p /nonexistent && \ 
    chown -R 65534:65534 /nonexistent /build
#RUN chmod -R 777 /nonexistent

# Enable Model Gallery for model management capability
ENV GALLERIES='[{"name":"model-gallery", "url":"github:go-skynet/model-gallery/index.yaml"}, {"url": "github:go-skynet/model-gallery/huggingface.yaml","name":"huggingface"}]'
ENV LD_LIBRARY_PATH=/usr/local/nvidia/lib:/usr/local/nvidia/lib64

# Add the "service nginx start" command at the end of the entrypoint script
#RUN echo "\nservice nginx start\n \
#            echo 'service nginx started'" >> /build/entrypoint.sh
#CMD service nginx start && /build/entrypoint.sh
ENTRYPOINT [ "/build/entrypoint.sh" ]

###################End of Adapation for SAP AI Core####################