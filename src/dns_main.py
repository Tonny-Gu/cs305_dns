import argparse
import time
import signal
import logging
from dns_config import DNS_CONFIG
from dns_model import *

class DNS_KILLER:
    kill_now = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit)
        signal.signal(signal.SIGTERM, self.exit)
    
    def exit(self, signum, frame):
        self.kill_now = True

class DNS_NODE:
    def instantiate_components(self, config: dict) -> dict:
        ret = {}
        for key in config:
            module_name: str = config[key]["module"]
            factory_name = module_name.upper() + "_FACTORY"
            module_meta = __import__(module_name)
            factory_meta:DNS_FACTORY = getattr(module_meta, factory_name)
            component:DNS_PIPE = factory_meta().get_component(config[key]["config"])
            ret[key] = component
        return ret

    def __init__(self, config: dict):
        pumps = self.instantiate_components(config["pump"])
        pipes = self.instantiate_components(config["pipe"])
        components = {}
        components.update(pipes)
        components.update(pumps)
        for key in config["pump"]:
            pump: DNS_PUMP = pumps[key]
            for pipe in config["pump"][key]["attach"]:
                pump.attach( components[pipe] )

        self.config = config
        
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--preset", type=str, default="", help="select a predefined preset")
    parser.add_argument("-c", "--config-file", type=str, default="config.json", help="select the path to the config file. Default: ./config.json")
    parser.add_argument("-l", "--log-level", type=str, choices=["debug", "info", "warn", "error", "fatal"], default="info", help="set log level. Most verbose: debug. Default: info")
    args = parser.parse_args()

    config = DNS_CONFIG(json_path=args.config_file, preset=args.preset).get_config()

    loglevels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warn": logging.WARN,
        "error": logging.ERROR,
        "fatal": logging.FATAL
    }
    logging.basicConfig(level=loglevels[ args.log_level ],
        format="%(asctime)s [%(levelname)s] (%(threadName)s @ %(filename)s:%(lineno)d) %(message)s")
    log = logging.getLogger()
    log.info("Project DNS v2 Started.")

    node = DNS_NODE(config)

    killer = DNS_KILLER()
    while not killer.kill_now:
        time.sleep(1)
    log.info("Project DNS v2 Terminated.")