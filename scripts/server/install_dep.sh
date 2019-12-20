#!/bin/bash

echo "******************************"
echo "Project DNS"
echo "Install Dependency for Server"
echo ""
echo "Author: Tonny-Gu"
echo "Version: Alpha.1211"
echo "******************************"

SOCKS_PORT=$(cat ../../config/config.json | python -c "import sys, json; print(json.load(sys.stdin)['dns']['socks5_port'])")
SERVER_IP_ADDR=$(cat ../../config/config.json | python -c "import sys, json; print(json.load(sys.stdin)['tun']['server']['ip_addr'])")
PIP_EXEC_CMD=$(cat ../../config/config.json | python -c "import sys, json; print(json.load(sys.stdin)['misc']['server']['pip_exec_cmd'])")

$PIP_EXEC_CMD install -r ../../src/requirements.txt

modprobe tun
if [ $? -ne 0 ]
then
    echo "Please check TUN/TAP is enabled."
    exit 1
fi
echo "TUN/TAP module loaded."

wget https://install.direct/go.sh
bash go.sh
rm go.sh

cp socks_config.json /etc/v2ray/config.json
sed -i "s/#SOCKS_PORT#/$SOCKS_PORT/g" /etc/v2ray/config.json
service v2ray start
service v2ray status

echo "V2Ray installed."
echo "Socks5 Proxy Address: $SERVER_IP_ADDR:$SOCKS_PORT"