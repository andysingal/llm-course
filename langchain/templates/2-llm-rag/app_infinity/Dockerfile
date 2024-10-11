ARG MODEL
ARG PORT

FROM michaelf34/infinity:0.0.63
# cache the model into the dockerfile
RUN /bin/sh -c infinity_emb v2 --port $PORT --model-id $MODEL --preload-only
# execute the model. Check all CLI arguments here: https://michaelfeil.eu/infinity/0.0.63/cli_v2/
ENTRYPOINT /bin/sh -c infinity_emb v2 --port $PORT --model-id $MODEL
