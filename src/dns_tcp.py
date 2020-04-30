from threading import Thread
import socket
import time

from dns_model import *

class DNS_TCP_CLIENT(DNS_PUMP):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.settimeout(2.0)
        self.connect()

        self.thread = Thread(target=self.thread_main)
        self.thread.setDaemon(True)
        self.thread.start()
    
    def connect(self):
        while not self.isTerminated:
            try:
                self.sock.connect((self.config["remote_addr"], self.config["remote_port"]))
            except Exception as e:
                self.log.error(e)
                time.sleep(3)
            else:
                break
    
    def thread_main(self):
        while not self.isTerminated:
            try:
                data: bytes = self.sock.recv(65535)
                if data: self.forward(data)
                else: raise(socket.error)
            except socket.timeout as e:
                pass
            except socket.error as e:
                self.log.error(e)
                self.connect()
            except Exception as e:
                self.log.error(e)
        # self.log.info("Terminated")
    
    def invoke(self, data: bytes) -> bytes:
        if not self.terminate: self.sock.send(data)
        return data
    
    def terminate(self):
        super().terminate()
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

class DNS_TCP_SERVER(DNS_PUMP):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((config["listen_addr"], config["listen_port"]))
        self.sock.listen(1)
        # self.sock.settimeout(2.0)

        self.thread = Thread(target=self.thread_main)
        self.thread.setDaemon(True)
        self.thread.start()

    def thread_main(self):
        while not self.isTerminated:
            try:
                conn, addr = self.sock.accept()
                self.log.info("Accepted " + str(addr))
                thread = Thread(target=self.client_handler, args=(conn, addr))
                thread.setDaemon(True)
                thread.start()
            except socket.timeout as e:
                pass
            except Exception as e:
                self.log.error(e)
        # self.log.info("Terminated")
    
    def client_handler(self, conn:socket, addr):
        self.conn, self.addr = conn, addr
        while not self.isTerminated:
            try:
                data: bytes = conn.recv(65535)
                if not data: break
                self.forward(data)
            except Exception as e:
                self.log.error(e)
        # self.log.info("Terminated")
    
    def invoke(self, data: bytes) -> bytes:
        if self.conn and not self.terminate: self.conn.send(data)
        return data
    
    def terminate(self):
        super().terminate()
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

class DNS_TCP_FACTORY(DNS_FACTORY):
    def get_component(self, config: dict = {}) -> DNS_PUMP:
        if config["mode"] == "client":
            return DNS_TCP_CLIENT(config)
        elif config["mode"] == "server":
            return DNS_TCP_SERVER(config)