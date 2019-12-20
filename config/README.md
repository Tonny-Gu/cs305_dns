# Data in Naked DNS - Configuration

本目录保存项目相关的全局配置参数

## config.json

### tun

此处保存和TUN网卡相关的设置

- server
    - ifname: 服务器TUN网卡名
    - ip_addr: 服务器TUN网卡IP地址
    - netmask: 服务器TUN网卡子网掩码
    - mtu: 服务器TUN网卡MTU值
- client
    - ifname: 客户端TUN网卡名
    - ip_addr: 客户端TUN网卡IP地址
    - netmask: 客户端TUN网卡子网掩码
    - mtu: 客户端TUN网卡MTU值

### dns

此处保存和Project DNS相关的重要设置

- own_domain: 私有域名
- public_dns: 公共DNS服务器IP地址
- socks5_port: Socks5服务端监听端口

### misc

此处保存杂项设置

- client
    - poll_delay: 轮询延迟（单位：s）
    - buffer_flush_delay: 发送队列刷新延迟（单位：s）
    - py_exec_cmd：客户端Python启动命令
    - pip_exec_cmd: 客户端pip启动命令
- server
    - py_exec_cmd：服务端Python启动命令
    - pip_exec_cmd: 服务端pip启动命令