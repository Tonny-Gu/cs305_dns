#!/bin/bash

echo "******************************"
echo "Project DNS"
echo "Backup default route"
echo ""
echo "Author: Tonny-Gu"
echo "Version: Alpha.1211"
echo "******************************"

CONFIG_DIR=$(pwd)/../config/private
DEFAULT_GW=$(route | grep default | awk '{print $2}')

echo $DEFAULT_GW > $CONFIG_DIR/DEFAULT_GW

echo "Done"