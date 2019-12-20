#!/bin/bash

echo "******************************"
echo "Project DNS"
echo "Client Startup"
echo ""
echo "Author: Tonny-Gu & Gogo"
echo "Version: Alpha.1211"
echo "******************************"

PYTHON_EXEC=$(cat ../config/config.json | python -c "import sys, json; print(json.load(sys.stdin)['misc']['client']['py_exec_cmd'])")

export PYTHONPATH=$PYTHONPATH:$(pwd)

$PYTHON_EXEC "$(pwd)/client/tun_client.py"

