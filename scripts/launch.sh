#!/bin/bash

echo "******************************"
echo "Project DNS"
echo "Launcher"
echo ""
echo "Author: Tonny-Gu & Gogo"
echo "Version: v2.20200410"
echo "******************************"

PYTHON_EXEC="python3"
SCRIPT_DIR=$(dirname "$0")
SRC_DIR="$SCRIPT_DIR/../src/"

cd $SRC_DIR

export PYTHONPATH=$PYTHONPATH:$SRC_DIR

$PYTHON_EXEC "$SRC_DIR/dns_main.py" $@

