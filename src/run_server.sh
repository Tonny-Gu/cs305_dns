#!/bin/bash

PYTHON_EXEC="python3.6"

export PYTHONPATH=$PYTHONPATH:$(pwd)

$PYTHON_EXEC "$(pwd)/server/tun_server.py"

