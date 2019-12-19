import socket
from queue import Queue
from threading import Thread

import dns.message
import dns.rdata
import dns.rdataclass
import dns.rdatatype

import dns_util


class DNSServer:
    def __init__(self, domain):
        self.domain = domain
        self.receive: Queue[bytes] = Queue()
        self.send: Queue[bytes] = Queue()
        self.isClosed: bool = False
        self.thread: Thread or None = None

        self.sock: socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 53))
        self.sock.settimeout(1)

    def start(self):
        if self.thread is None:
            self.thread = Thread(target=self.run)
            self.thread.start()

    def run(self):
        while not self.isClosed:
            try:
                print("listen")
                data, addr = self.sock.recvfrom(1024)
                print("receive")
                result = self.handle(data)
                self.sock.sendto(result, addr)
            except socket.timeout:
                pass

    def close(self):
        self.isClosed = True

    def handle(self, receive: bytes) -> bytes:
        request: dns.message.Message = dns.message.from_wire(receive)

        respond = dns.message.Message(request.id)
        respond.flags = dns.flags.QR
        if len(request.question) > 0:
            respond.question.append(request.question[0])
            qname = str(request.question[0].name)
            req_data = qname[:qname.rindex("." + self.domain)]
            rep_data = self.handle_request(req_data)
            respond.answer.append(dns.rrset.from_text(qname, 0, dns.rdataclass.IN, dns.rdatatype.TXT, rep_data))
        return respond.to_wire()

    def handle_request(self, req_data: str) -> str:
        label_pos = req_data.rindex(".")
        label = req_data[label_pos + 1:]
        data = req_data[:label_pos]
        if label == "msg":
            self.receive.put(dns_util.decode_domain(data))

        if self.send.empty():
            return ".0"
        else:
            return dns_util.encode_txt(self.send.get()) + "." + str( self.send.qsize() )


if __name__ == '__main__':
    # create
    server = DNSServer("group-25.cs305.fun")
    # start
    server.start()
    # close
    server.close()
