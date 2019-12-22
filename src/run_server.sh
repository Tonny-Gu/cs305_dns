#!/bin/bash

echo "******************************"
echo "Project DNS"
echo "Server Startup"
echo ""
echo "Author: Tonny-Gu & Gogo"
echo "Version: Alpha.1211"
echo "******************************"

SCRIPT_DIR=$(dirname "$0")

cd $SCRIPT_DIR

PYTHON_EXEC=$(cat ../config/config.json | python -c "import sys, json; print(json.load(sys.stdin)['misc']['server']['py_exec_cmd'])")

export PYTHONPATH=$PYTHONPATH:$(pwd)

$PYTHON_EXEC "$(pwd)/server/tun_server.py"

