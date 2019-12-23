###  packet IP datagram into DNS packet

```sequence
TUN0 -> DNS Client : read
Note over DNS Client : packet
DNS Client -> Public DNS : query
Public DNS -> DNS Server : recursive query
Note over DNS Server : unpacket
DNS Server -> TUN1 : write
TUN1 --> DNS Server : read
Note over DNS Server : packet
DNS Server --> Public DNS : response
Public DNS --> DNS Client : response
Note over DNS Client : unpacket
DNS Client --> TUN0 : write
```


### fragmentation and reassembly

```sequence
Note over Client App : open socket
Client App -> TCP/IP Stack : packet 1
Note over TCP/IP Stack : check forwarding table
Note over TCP/IP Stack : fragment by MTU
TCP/IP Stack -> TUN0 : IP packet 1.0
TCP/IP Stack -> TUN0 : IP packet 1.1
TCP/IP Stack -> TUN0 : IP packet 1.2
Note over TUN0 : wait for DNS
TUN0 -> TCP/IP Stack : IP packet 2.0
TUN0 -> TCP/IP Stack : IP packet 2.1
TUN0 -> TCP/IP Stack : IP packet 2.2
Note over TCP/IP Stack : reassembly
TCP/IP Stack -> Client App : packet 2
```

### NAT

```sequence
TUN1 -> Socks Proxy : 
Note over Socks Proxy : do NAT
Note over Socks Proxy : send to Internet
Socks Proxy -> TUN1 :
```

