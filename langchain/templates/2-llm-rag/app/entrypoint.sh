#!/bin/sh

# Handle docker volmue mapping for pip
if ! command -v pip &> /dev/null
then
    echo "pip could not be found. Reinstalling..."
    python3 -m ensurepip
    pip install -r requirements.txt
fi

exec "$@"
