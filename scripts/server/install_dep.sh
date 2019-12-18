#!/bin/bash

echo "******************************"
echo "Project DNS"
echo "Install Dependency for Server"
echo ""
echo "Author: Tonny-Gu"
echo "Version: Alpha.1211"
echo "******************************"

SOCKS_PORT=$(cat ../../config/SOCKS_PORT)

wget https://install.direct/go.sh
bash go.sh
rm go.sh

cp socks_config.json /etc/v2ray/config.json
sed -i "s/#SOCKS_PORT#/$SOCKS_PORT/g" /etc/v2ray/config.json
service v2ray start
service v2ray status

echo "V2Ray installed."

