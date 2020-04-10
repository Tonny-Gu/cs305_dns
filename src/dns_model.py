from abc import ABCMeta, abstractmethod
from typing import List

class DNS_PIPE(metaclass=ABCMeta):
    @abstractmethod
    def invoke(self, data: bytes) -> bytes:
        pass

class DNS_PUMP(DNS_PIPE):
    pipes: List[DNS_PIPE] = []
    
    def attach(self, pipe:DNS_PIPE):
        self.pipes.append(pipe)
    
    def transfer(self, data:bytes):
        data_in = data
        for pipe in self.pipes:
            data_out: bytes = pipe.invoke(data_in)
            data_in = data_out

class DNS_FACTORY(metaclass=ABCMeta):
    @abstractmethod
    def get_component(self, config: dict = {}) -> DNS_PIPE:
        pass
