import socket
import string
import time
from queue import Queue
from threading import Thread

import dns.rdatatype
import dns.resolver
import random

import dns_util


def random_string(string_length=10) -> str:
    alphabat = string.ascii_letters + string.octdigits
    return ''.join(random.choice(alphabat) for _ in range(string_length))


class DNSClient:
    def __init__(self, server):
        self.server = server
        self.receive: Queue[bytes] = Queue()
        self.send: Queue[bytes] = Queue()
        self.isClosed: bool = False
        self.send_thread: Thread or None = None
        self.recv_thread: Thread or None = None
        self.reload_thread: Thread or None = None

        self.remain_pkg_num = 0
        self.remain_pkg_num_reload = 0

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def reload(self):
        while not self.isClosed:
            self.remain_pkg_num = self.remain_pkg_num_reload + 1
            time.sleep(0.1)
        
    def start(self):
        if self.send_thread is None:
            self.send_thread = Thread(target=self.batch_send)
            self.send_thread.start()
        if self.recv_thread is None:
            self.recv_thread = Thread(target=self.recv)
            self.recv_thread.start()
        if self.reload_thread is None:
            self.reload_thread = Thread(target=self.reload)
            self.reload_thread.start()

    def recv(self):
        while not self.isClosed:
            data, addr = self.sock.recvfrom(1024)
            res: dns.message.Message = dns.message.from_wire(data)

            try:
                res_data: str = res.answer[0].items[0].strings[0].decode()
            except IndexError:
                print("mistake data receive")
                continue

            label_pos = res_data.rindex(".")
            label = res_data[label_pos + 1:]
            data = res_data[:label_pos]

            remain_pkg_num = int(label)
            if remain_pkg_num > self.remain_pkg_num_reload:
                self.remain_pkg_num_reload = remain_pkg_num
                self.remain_pkg_num        = remain_pkg_num
            else: self.remain_pkg_num_reload = remain_pkg_num

            if len(data) > 0:
                self.receive.put(dns_util.decode_txt(data))

    def batch_send(self):
        while not self.isClosed:
            while max(self.remain_pkg_num, self.send.qsize())>0:
                self.sock.sendto(self.make_request(), ("120.78.166.34", 53))
                if self.remain_pkg_num>0: self.remain_pkg_num -= 1
            time.sleep(0.005)

    def make_request(self) -> bytes:
        domain: str
        if self.send.empty():
            domain = "x" + random_string(31) + ".fetch." + self.server
        else:
            domain = dns_util.encode_domain(self.send.get()) + ".msg." + self.server
        print("send " + domain)
        request = dns.message.make_query(domain, dns.rdatatype.TXT)
        return request.to_wire()

    def close(self):
        self.isClosed = True


if __name__ == '__main__':
    # create
    client = DNSClient("group-25.cs305.fun")
    # start
    client.start()
    # close
    client.close()
