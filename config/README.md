# Data in Naked DNS - Configuration

#### 目录结构

- `本目录` 保存项目相关的全局配置参数

- `private` 保存用户备份参数



## CLIENT_WAN_IFNAME

指定客户端的网络出口

#### 内容

Linux udev的网络接口名称，例如：`eth0`



## SERVER_WAN_IFNAME

指定服务端网络出口

#### 内容

Linux udev的网络接口名称，例如：`eth0`



## PUBLIC_DNS_SERVER_ADDR

指定公共DNS服务器地址

#### 内容

IPv4地址



## TUN_CLIENT_IP_ADDR

指定客户端的TUN虚拟网卡的IP地址

#### 内容

IPv4地址



## TUN_SERVER_IP_ADDR

指定服务端的TUN虚拟网卡的IP地址

#### 内容

IPv4地址