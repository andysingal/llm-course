ARG BASE_IMAGE=vllm/vllm-openai:latest
FROM ${BASE_IMAGE}
ENV LANG C.UTF-8

# Adaptation for SAP AI Core
RUN mkdir -p /nonexistent/ &&\
    mkdir -p /hf-home/ && \ 
    chown -R nobody:nogroup /nonexistent /hf-home/ && \
    chmod -R 770 /nonexistent/ /hf-home/

ENV HF_HOME=/hf-home
# MODEL will be passed from serving template when pod is initiated. Here just set a default model
ENV MODEL="TheBloke/Mistral-7B-Instruct-v0.2-AWQ"

EXPOSE 8000

ENTRYPOINT ["python3", "-m", "vllm.entrypoints.openai.api_server", "--model", "TheBloke/Mistral-7B-Instruct-v0.2-AWQ", "--dtype","half", "--gpu-memory-utilization", "0.95"]