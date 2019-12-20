from functools import reduce
import base64
import base62
import json
import pytun
import client.dns_client
import server.dns_server
from threading import Thread
import time
import os

config = {}

def encode_domain(data: bytes) -> str:
    """
    assert len(data) <= 100, "data is longer than 100 bytes"
    f = filter(lambda it: len(it) > 0, [data[0:25], data[25:50], data[50:75], data[75:100]])
    m = map(lambda it: it.hex(), list(f))
    return "x" + (".x".join(list(m)))"""
    return base62.encodebytes(data)


def decode_domain(data: str) -> bytes:
    """
    s = data.split(".")
    m = map(lambda it: bytes.fromhex(it[1:]), s)
    return reduce(lambda a, b: a + b, list(m), b'')"""
    return base62.decodebytes(data)


def encode_txt(data: bytes) -> str:
    # assert len(data) <= 100, "data is longer than 100 bytes"
    return base64.b64encode(data).decode()


def decode_txt(data: str) -> bytes:
    return base64.b64decode(data)

def load_config():
    global config
    with open("../config/config.json", "r") as config_file:
        config = json.loads( "".join(config_file.readlines()) )

def get_config():
    return config

load_config()

def get_tun_if(role="clients"):
    tun_config = get_config()["tun"][role]
    print("TUN: Init. Param: ", tun_config)
    tun = pytun.TunTapDevice(name=tun_config["ifname"], flags=pytun.IFF_TUN | pytun.IFF_NO_PI)
    tun.addr = tun_config["ip_addr"]
    tun.netmask = tun_config["netmask"]
    tun.mtu = tun_config["mtu"]
    tun.up()
    return tun

class DNSnode:
    def __init__(self, role="client"):
        self.tun = get_tun_if(role)
        dns_config = get_config()["dns"]
        misc_config = get_config()["misc"][role]

        if role == "client":
            self.node = client.dns_client.DNSClient(dns_config["own_domain"], dns_config["public_dns"], misc_config["poll_delay"], misc_config["buffer_flush_delay"])
        elif role == "server":
            self.node = server.dns_server.DNSServer(dns_config["own_domain"])
        self.node.start()

        self.rx_thread = Thread(target=self.read)
        self.rx_thread.setDaemon(True)
        self.rx_thread.start()

        self.tx_thread = Thread(target=self.write)
        self.tx_thread.setDaemon(True)
        self.tx_thread.start()


    def read(self):
        while True:
            to_send: bytes = self.tun.read(self.tun.mtu)
            self.node.send.put(to_send)
            # print("will send " + str(len(to_send)))

    def write(self):
        while True:
            to_receive: bytes = self.node.receive.get()
            self.tun.write(to_receive)
            # print("receive " + str(len(to_receive)))
    
    def loop_forever(self):
        while True:
            try:
                print("TUN:")
                os.system("ifconfig {} | grep packets".format(self.tun.name))
                print("DNS: RX packets: {} TX packets: {}".format(self.node.rx_count, self.node.tx_count))
                time.sleep(2)
            except KeyboardInterrupt:
                print("KeyboardInterrupt, exit")
                self.node.close()
                break

if __name__ == '__main__':
    data = b'1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    encode = encode_domain(data)
    print(encode)
    decode = decode_domain(encode)
    print(decode)
    assert data == decode

    encode = encode_txt(data)
    print(encode)
    decode = decode_txt(encode)
    print(decode)
    assert data == decode
