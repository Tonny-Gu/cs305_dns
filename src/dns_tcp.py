from threading import Thread
import socket

from dns_model import *

class DNS_TCP_CLIENT(DNS_PUMP):
    def __init__(self, config: dict = {}):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((config["remote_addr"], config["remote_port"]))
        self.sock.settimeout(2.0)

        self.thread = Thread(target=self.thread_main)
        self.thread.setDaemon(True)
        self.thread.start()
    
    def thread_main(self):
        while True:
            try:
                data: bytes = self.sock.recv(65535)
                self.transfer(data)
            except socket.timeout as e:
                pass
            except Exception as e:
                print(e)
    
    def invoke(self, data: bytes) -> bytes:
        self.sock.send(data)

class DNS_TCP_SERVER(DNS_PUMP):
    def __init__(self, config: dict = {}):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((config["listen_addr"], config["listen_port"]))
        self.sock.listen(1)
        self.sock.settimeout(2.0)

        self.thread = Thread(target=self.thread_main)
        self.thread.setDaemon(True)
        self.thread.start()

    def thread_main(self):
        while True:
            try:
                conn, addr = self.sock.accept()
                self.conn, self.addr = conn, addr
                while True:
                    data: bytes = conn.recv(65535)
                    if not data: break
                    self.transfer(data)
            except socket.timeout as e:
                pass
            except Exception as e:
                print(e)
    
    def invoke(self, data: bytes) -> bytes:
        if self.conn: self.conn.send(data)

class DNS_TCP_FACTORY(DNS_FACTORY):
    def get_component(self, config: dict = {}) -> DNS_PUMP:
        if config["mode"] == "client":
            return DNS_TCP_CLIENT(config)
        elif config["mode"] == "server":
            return DNS_TCP_SERVER(config)