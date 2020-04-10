from dns_model import *

class DNS_GZIP_ENC(DNS_PIPE):
    def __init__(self, config: dict = {}):
        pass

    def invoke(self, data: bytes) -> bytes:
        return data

class DNS_GZIP_FACTORY(DNS_FACTORY):
    def get_component(self, config: dict = {}) -> DNS_PIPE:
        return DNS_GZIP_ENC(config)