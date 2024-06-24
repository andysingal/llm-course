FROM pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime AS runtime

WORKDIR /usr/src

# Update and install dependencies
RUN apt-get update && \
    apt-get install -y \
    ca-certificates \
    nginx \
    curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip==23.2.1 && \
    python3 -m pip install "infinity-emb[all]" && \
    rm -rf /root/.cache/pip

EXPOSE 7997

# Adaptation for SAP AI Core
COPY run.sh /usr/src/run.sh

RUN mkdir -p /nonexistent/ && \
    mkdir -p /hf-home/ && \ 
    chown -R nobody:nogroup /nonexistent /hf-home/ && \
    chmod -R 770 /nonexistent/ /hf-home/ && \
    chmod +x /usr/src/run.sh

ENV HF_HOME=/hf-home
    # Note: Uncomment this ENV with MODEL_NAME & URL_PREFIX if you're running Docker locally. Don't forget about the backslash \
    # MODEL_NAME="nreimers/MiniLM-L6-H384-uncased"
    # URL_PREFIX="/v1"

ENTRYPOINT [ "/usr/src/run.sh" ]