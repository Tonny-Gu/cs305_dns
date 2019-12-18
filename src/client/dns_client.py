import string
import time
from queue import Queue
from threading import Thread
from typing import Tuple

import dns.rdatatype
import dns.resolver
import random

import dns_encode
from time_limits import time_limited, TimeoutException


def random_string(string_length=10) -> str:
    alphabat = string.ascii_letters + string.octdigits
    return ''.join(random.choice(alphabat) for _ in range(string_length))


class DNSClient:
    def __init__(self, server):
        self.server = server
        self.receive: Queue[bytes] = Queue()
        self.send: Queue[bytes] = Queue()
        self.isClosed: bool = False
        self.thread: Thread or None = None

        self.noDataReceive = False

    def start(self):
        if self.thread is None:
            self.thread = Thread(target=self.run)
            self.thread.start()

    def run(self):

        @time_limited(3)
        def to_run():
            res, res_data = self.make_request()
            self.noDataReceive = res_data == "--NODATA--"
            if res_data != "--NODATA--":
                self.receive.put(dns_encode.decode_txt(res_data))
            if self.noDataReceive and self.send.empty():
                time.sleep(0.5)

        while not self.isClosed:
            try:
                to_run()
            except TimeoutException:
                print("timeout")

    def close(self):
        self.isClosed = True

    def make_request(self) -> Tuple[dns.message.Message, str]:
        domain: str
        if self.send.empty():
            domain = "x" + random_string(31) + ".fetch." + self.server
        else:
            domain = dns_encode.encode_domain(self.send.get()) + ".msg." + self.server
        request = dns.message.make_query(domain, dns.rdatatype.TXT)
        print("send " + domain)
        res = dns.query.udp(request, "120.78.166.34")
        return res, res.answer[0].items[0].strings[0].decode()


if __name__ == '__main__':
    # create
    client = DNSClient("group-25.cs305.fun")
    # start
    client.start()
    # close
    client.close()