import queue
from threading import Thread
# import pytun
import json

class nbtun:
    def __init__(self, role="client"):
        with open("../config/config.json", "r") as config_file:
            self.config = json.loads( config_file.readlines() )
        print(self.config)

if __name__ == "__main__":
    tun = nbtun()