from threading import Thread
import socket
import time

from dns_model import *

class DNS_UDP(DNS_PUMP):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((config["listen_addr"], config["listen_port"]))
        # self.sock.settimeout(2.0)
        
        self.thread = Thread(target=self.thread_main)
        self.thread.setDaemon(True)
        self.thread.start()

    def thread_main(self):
        while not self.isTerminated:
            try:
                data, addr = self.sock.recvfrom(65535)
                self.log.info("Received from " + str(addr))
                if data: self.forward(data)
            except socket.timeout as e:
                pass
            except Exception as e:
                self.log.error(e)
        self.log.info("Terminated")
    
    def invoke(self, data: bytes) -> bytes:
        config = self.config
        if not self.terminate: self.sock.sendto(data, (config["remote_addr"], config["remote_port"]))
        return data
    
    def terminate(self):
        super().terminate()
        self.sock.close()

class DNS_UDP_FACTORY(DNS_FACTORY):
    def get_component(self, config: dict = {}) -> DNS_PUMP:
        return DNS_UDP(config)