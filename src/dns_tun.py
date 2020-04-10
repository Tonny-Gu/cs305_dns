from threading import Thread
import pytun
import time
import os

from dns_model import *

class DNS_TUN(DNS_PUMP):
    def __init__(self, config: dict = {}):
        self.tun = pytun.TunTapDevice(name=config["ifname"], flags=pytun.IFF_TUN | pytun.IFF_NO_PI)
        self.tun.addr = config["ip_addr"]
        self.tun.netmask = config["netmask"]
        self.tun.mtu = config["mtu"]
        self.tun.up()

        self.thread = Thread(target=self.thread_main)
        self.thread.setDaemon(True)
        self.thread.start()

    def thread_main(self):
        while True:
            try:
                data: bytes = self.tun.read(self.tun.mtu)
                self.transfer(data)
            except Exception as e:
                print(e)
    
    def invoke(self, data: bytes) -> bytes:
        self.tun.write(data)

class DNS_TUN_FACTORY(DNS_FACTORY):
    def get_component(self, config: dict = {}) -> DNS_PUMP:
        return DNS_TUN(config)