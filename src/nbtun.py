import queue
from threading import Thread
import pytun
import json
import subprocess
import os

class nbtun:
    def __init__(self, role="client"):
        self.callbacks = {}
        with open("./config/config.json", "r") as config_file:
            self.config = json.loads( "".join(config_file.readlines()) )
        
    
    def get_config(self):
        return self.config

    def reg_callback(self, event: str, cb_func):
        self.callbacks[event] = cb_func

if __name__ == "__main__":
    tun = nbtun()