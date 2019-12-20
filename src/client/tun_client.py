import dns_util

if __name__ == '__main__':
    client = dns_util.DNSnode("client")
    client.loop_forever()
