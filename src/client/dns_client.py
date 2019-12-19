import socket
import string
import time
from queue import Queue
from threading import Thread

import dns.rdatatype
import dns.resolver
import random

import dns_encode


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

        self.remain_pkg_num = 0

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        if self.send_thread is None:
            self.send_thread = Thread(target=self.run)
            self.send_thread.start()
        if self.recv_thread is None:
            self.recv_thread = Thread(target=self.recv)
            self.recv_thread.start()

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

            self.remain_pkg_num = int(label)

            if len(data) > 0:
                self.receive.put(dns_encode.decode_txt(data))

    def run(self):
        while not self.isClosed:
            for i in range(self.remain_pkg_num + 1):
                self.sock.sendto(self.make_request(), ("120.78.166.34", 53))
            time.sleep(0.1)

    def make_request(self) -> bytes:
        domain: str
        if self.send.empty():
            domain = "x" + random_string(31) + ".fetch." + self.server
        else:
            domain = dns_encode.encode_domain(self.send.get()) + ".msg." + self.server
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
