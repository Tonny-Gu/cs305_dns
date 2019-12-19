#!/bin/bash

PYTHON_EXEC="python3"

export PYTHONPATH=$PYTHONPATH:$(pwd)

$PYTHON_EXEC "$(pwd)/client/tun_client.py"

