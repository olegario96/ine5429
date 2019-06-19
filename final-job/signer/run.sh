#!/bin/bash

if [ -d ".venv" ]; then
    source .venv/bin/activate;
fi

python3 -m signer;
exit;
