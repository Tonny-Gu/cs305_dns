import dns_util

if __name__ == '__main__':
    server = dns_util.DNSnode("server")
    server.loop_forever()
