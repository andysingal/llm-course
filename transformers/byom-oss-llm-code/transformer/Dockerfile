ARG BASE_IMAGE=pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime
FROM ${BASE_IMAGE} AS runtime

WORKDIR /app
COPY app/* ./

ENV CUDA_HOME=/usr/local/cuda

RUN python3 -m pip install -r requirements.txt && \
    rm -rf /root/.cache/pip

# Adaptation for SAP AI Core
RUN mkdir -p /nonexistent && \
    mkdir -p /hf-home && \ 
    chown -R nobody:nogroup /nonexistent /hf-home /app && \
    chmod -R 770 /nonexistent /hf-home /app

ENV HF_HOME=/hf-home

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
#ENTRYPOINT [ "/app/run.sh" ]