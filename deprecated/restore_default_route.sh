#!/bin/bash

echo "******************************"
echo "Project DNS"
echo "Restore default route"
echo ""
echo "Author: Tonny-Gu"
echo "Version: Alpha.1211"
echo "******************************"

CONFIG_DIR=$(pwd)/../config/private
DEFAULT_GW=$(cat $CONFIG_DIR/DEFAULT_GW)

route add default gw $DEFAULT_GW

echo "Done"