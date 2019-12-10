#!/bin/bash

echo "******************************"
echo "Project DNS"
echo "Setup TUN Interface for Server"
echo ""
echo "Author: Tonny-Gu"
echo "Version: Alpha.1211"
echo "******************************"

CONFIG_DIR=$(pwd)/../../config
TUN_IFNAME=$(cat $CONFIG_DIR/TUN_IFNAME)
TUN_IP=$(cat $CONFIG_DIR/TUN_SERVER_IP_ADDR)
TUN_MASK=$(cat $CONFIG_DIR/TUN_NETMASK)
WAN_IFNAME=$(cat $CONFIG_DIR/SERVER_WAN_IFNAME)

get_wan_ip(){
    WAN_IP=$( ip addr show dev $WAN_IFNAME | egrep -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | head -n 1 )
    [ -z ${WAN_IP} ] && echo "[Fatal] Failed to get WAN IP" && exit 1
    echo "[Info] Got WAN IP: ${WAN_IP}"
}


modprobe tun
if [ $? -ne 0 ]
then
    echo "[Fatal] Please check TUN/TAP is enabled."
    exit 1
fi
echo "[Info] Kernel module loaded."

tunctl -t $TUN_IFNAME -u root
ifconfig $TUN_IFNAME $TUN_IP netmask $TUN_MASK promisc
if [ $? -ne 0 ]
then
    echo "[Fatal] Creating TUN Interface failed."
    exit 1
fi
echo "[Info] TUN interface created."

echo 1 > /proc/sys/net/ipv4/ip_forward
echo "[Info] IPv4 IP Forwarding enabled."

get_wan_ip
iptables -t nat -A POSTROUTING -d $WAN_IP -j SNAT --to-source $TUN_IP
echo "[Info] NAT enabled."