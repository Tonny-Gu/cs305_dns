#!/bin/bash

echo "******************************"
echo "Project DNS"
echo "Install Dependency for Client"
echo ""
echo "Author: Tonny-Gu"
echo "Version: Alpha.1211"
echo "******************************"

PIP_EXEC_CMD=$(cat ../../config/config.json | python -c "import sys, json; print(json.load(sys.stdin)['misc']['client']['pip_exec_cmd'])")

$PIP_EXEC_CMD install -r ../../src/requirements.txt

modprobe tun
if [ $? -ne 0 ]
then
    echo "Please check TUN/TAP is enabled."
    exit 1
fi
echo "TUN/TAP module loaded."