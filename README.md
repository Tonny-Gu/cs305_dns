# Data in Naked DNS

#### SUSTech CS305 - Computer Networks - Final Project



## Introduction

借助DNS公共服务器递归查询的特性，让DNS服务器转发代理流量的实验性tunnel。



目录结构：

- `config` 全局配置文件
- `doc` 项目相关文档
- `scripts` 部署维护相关脚本
- `src` 项目相关源码


## Requirement

操作系统：`Ubuntu >= 16.04`

Python版本：`>= 3.6`

支持`TUN/TAP` （不可部署在`OpenVZ`的容器内）

需要`root`或管理员权限

## Installation

### Server

#### Step 1

进入`config`目录修改相关配置

#### Step 2

关闭所有占用`53`端口的程序

#### Step 3

运行`script/server`目录下的`install_dep.sh`脚本

```bash
cd script/server
sudo ./install_dep.sh
```

脚本运行结束后显示的IP地址为`Socks5`服务器地址

#### Step 4

运行`src`目录下的`run_server.sh`脚本

```bash
cd src
sudo ./run_server.sh
```

### Client

#### Step 1

进入`config`目录修改相关配置

#### Step 2

运行`script/client`目录下的`install_dep.sh`脚本

```bash
cd script/client
sudo ./install_dep.sh
```

#### Step 3

运行`src`目录下的`run_client.sh`脚本

```bash
cd src
sudo ./run_client.sh
```

#### Step 4

填入`Socks5`服务器地址

推荐Chrome配合SwitchyOmega食用

## Declaration

The idea for this project is based on an assignment from Prof. Rodrigo Fonseca for CS168, Computer Networks, from Brown university, with some changes. 

Note that gaining access to network resources you are not authorized to access may be illegal. We do not encourage you to do this, nor will be responsible for any consequences if you do this. 
