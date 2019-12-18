import pytun
import client.dns_client
from threading import Thread

if __name__ == '__main__':
    tun = pytun.TunTapDevice(name='ctun0', flags=pytun.IFF_TUN | pytun.IFF_NO_PI)
    tun.addr = '10.100.0.1'
    tun.dstaddr = '10.101.0.1'
    tun.netmask = '255.255.255.0'
    tun.mtu = 100
    tun.up()

    client = client.dns_client.DNSClient("group-25.cs305.fun")
    client.start()


    def read():
        while True:
            to_send: bytes = tun.read(tun.mtu)
            client.send.put(to_send)
            print("will send " + str(len(to_send)))


    Thread(target=read).start()

    while True:
        to_receive: bytes = client.receive.get()
        tun.write(to_receive)
        print("receive " + str(len(to_receive)))
