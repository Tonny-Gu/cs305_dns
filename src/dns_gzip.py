import zlib
from dns_model import *

class DNS_GZIP_ENC(DNS_PIPE):
    def __init__(self, config: dict = {}):
        self.level = config["level"]
        super().__init__(config)

    def invoke(self, data: bytes) -> bytes:
        ret = b''
        try:
            ret = zlib.compress(data, self.level)
        except Exception as e:
            self.log.error(e)
        return ret
    
    def terminate(self): pass

class DNS_GZIP_DEC(DNS_PIPE):
    def __init__(self, config: dict = {}):
        super().__init__(config)
    
    def invoke(self, data: bytes) -> bytes:
        ret = b''
        try:
            ret = zlib.decompress(data)
        except Exception as e:
            self.log.error(e)
        return ret
    
    def terminate(self): pass

class DNS_GZIP_FACTORY(DNS_FACTORY):
    def get_component(self, config: dict = {}) -> DNS_PIPE:
        if config["mode"] == "encode":
            return DNS_GZIP_ENC(config)
        elif config["mode"] == "decode":
            return DNS_GZIP_DEC(config)
