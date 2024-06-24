#!/bin/bash

# Set default Host to 0.0.0.0 if not already set
HOST="${HOST:-0.0.0.0}"
OPT+=" --host ${HOST}"

# Add port to options if PORT is set and --port is not already in ARG
if [ ! -z "${PORT}" ] && [[ ! "${ARG}" =~ --port ]]; then
	OPT+=" --port ${PORT}"
fi

# Echo the SERVE_FILES_PATH and the options to be used
echo ${MODEL_NAME}
echo ${URL_PREFIX}

# Use set -x to print commands and their arguments as they are executed.
set -x

# Run the service with the model and the prepared options
infinity_emb --url-prefix "${URL_PREFIX}" --model-name-or-path "${MODEL_NAME}"