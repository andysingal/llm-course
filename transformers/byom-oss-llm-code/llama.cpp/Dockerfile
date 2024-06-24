ARG BASE_IMAGE=ghcr.io/ggerganov/llama.cpp:server-cuda
FROM ${BASE_IMAGE}
ENV LANG C.UTF-8

# Adaptation for SAP AI Core
# Update and install dependencies
RUN apt-get update && \
    apt-get install -y \
    ca-certificates \
    wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /nonexistent && \
    mkdir -p /models && \
    chown -R nobody:nogroup /nonexistent /models && \
    chmod -R 770 /nonexistent /models

EXPOSE 8080