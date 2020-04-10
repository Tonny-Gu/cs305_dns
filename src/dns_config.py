import json

class DNS_CONFIG:
    config = {}
    def __init__(self, json_path="config.json", preset=""):
        with open(json_path, "r") as fs: 
            config: dict = json.loads( "".join(fs.readlines()) )
        if not preset: self.config = config[ list(config.keys())[0] ]
        else: self.config = config[ preset ]
        if "__common" in config: self.config.update(config["__common"])

    def __getitem__(self, index):
        return self.config[index]
    
    def __iter__(self):
        return self.config.__iter__()
    
    def get_config(self) -> dict:
        return self.config
        