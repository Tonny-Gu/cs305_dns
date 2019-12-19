import pytun
import server.dns_server
from threading import Thread

if __name__ == '__main__':
    tun = pytun.TunTapDevice(name='stun0', flags=pytun.IFF_TUN | pytun.IFF_NO_PI)
    tun.addr = '10.101.0.1'
    tun.dstaddr = '10.100.0.1'
    tun.netmask = '255.255.255.0'
    tun.mtu = 100
    tun.up()

    server = server.dns_server.DNSServer("group-25.cs305.fun")
    server.start()


    def read():
        while True:
            to_send: bytes = tun.read(tun.mtu)
            server.send.put(to_send)
            print("will send " + str(len(to_send)))


    tun_thread = Thread(target=read)
    tun_thread.setDaemon(True)
    tun_thread.start()

    while True:
        try:
            to_receive: bytes = server.receive.get()
            tun.write(to_receive)
            print("receive " + str(len(to_receive)))
        except KeyboardInterrupt:
            print("KeyboardInterrupt, exit")
            server.close()
            break
