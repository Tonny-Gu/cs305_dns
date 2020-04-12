import base62
from dns_model import *

class DNS_BASE62_ENC(DNS_PIPE):
    def __init__(self, config: dict = {}):
        super().__init__(config)

    def invoke(self, data: bytes) -> bytes:
        ret = b''
        try:
            ret = base62.encodebytes(data)
        except Exception as e:
            self.log.error(e)
        return ret

class DNS_BASE62_DEC(DNS_PIPE):
    def __init__(self, config: dict = {}):
        super().__init__(config)
    
    def invoke(self, data: bytes) -> bytes:
        ret = b''
        try:
            ret = base62.decodebytes(data)
        except Exception as e:
            self.log.error(e)
        return ret

class DNS_BASE62_FACTORY(DNS_FACTORY):
    def get_component(self, config: dict = {}) -> DNS_PIPE:
        if config["mode"] == "encode":
            return DNS_BASE62_ENC(config)
        elif config["mode"] == "decode":
            return DNS_BASE62_DEC(config)
