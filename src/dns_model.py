from abc import ABCMeta, abstractmethod
from typing import List
import logging

class DNS_PIPE(metaclass=ABCMeta):
    def __init__(self, config: dict):
        self.config = config
        self.log = logging.getLogger()
        self.log.info("Module %s Init." % self.__class__.__name__)

    @abstractmethod
    def invoke(self, data: bytes) -> bytes:
        pass

class DNS_PUMP(DNS_PIPE):
    def __init__(self, config: dict):
        super().__init__(config)
        self.pipes: List[DNS_PIPE] = []
    
    def attach(self, pipe:DNS_PIPE):
        self.pipes.append(pipe)
    
    def forward(self, data:bytes):
        data_in = data
        for pipe in self.pipes:
            data_out: bytes = pipe.invoke(data_in)
            if not data_out: break
            data_in = data_out

class DNS_FACTORY(metaclass=ABCMeta):
    @abstractmethod
    def get_component(self, config: dict = {}) -> DNS_PIPE:
        pass
