import os
import subprocess
from pathlib import Path
from configparser import ConfigParser
from typing import Union

class Constructor:
    def __init__(self):
        self.main_dir = Path(os.path.dirname(__file__)).parent
        self.config_ini = os.path.join(self.main_dir, "CONSTRUCTOR.ini")
        self.main_config = ConfigParser()
        self.main_config.read(self.config_ini)
        self.conf = self.getConfig()
        self.server_conf = self.getServerConfig()
        self.onion_cfg = {}
        
    
    def fixPort(self, port: str) -> tuple:
        return tuple(int(p) for p in port.split(":"))
    
    def getExtraPort(self, num_start: int, num_port: int) -> tuple:
        ports = []
        for x in range(num_port):
            ports.append((num_start + (x * 20), num_start + (x * 20)))
        return tuple(ports)
    
    def getConfig(self) -> dict:
        conf = self.main_config["CONFIG"]
        config = {
                    "MAIN_DIR" : str(self.main_dir),
                    "CONFIG_FILE_PATH" : self.config_ini,
                    "ONIONS_DIR" : os.path.join(self.main_dir, "ONIONS"),
                    "LOGS_DIR" : os.path.join(self.main_dir, "ONIONS", "Logs"),
                    "TORRC_DIR" : os.path.join(self.main_dir, "ONIONS", "Torrc"),
                    "TOR_FILE_DIR" : os.path.join(self.main_dir, "ONIONS", "TorFiles"),
                    "CONTROLS_DIR" : os.path.join(self.main_dir, "ONIONS", "_controls"),
                    "CONTROL_PORT" : self.fixPort(conf.get("CONTROL_PORT")),
                    "PORT_MAPPING" : tuple(map(self.fixPort, conf["PORT_MAPPING"].split(" "))),
                    "IMAGE_NAME" : conf.get("IMAGE_NAME"),
                    "ONION_NAME" : conf.get("PORTAL_NAME"),
                    "EXTRA_PORT" : self.getExtraPort(int(conf.get("EXTRA_PORT_START")), int(conf.get("EXTRA_PORT_NUM"))),
                    "CONTAINER_NAME" : conf.get("CONTAINER_NAME")
        }
        

        return config
    
    def getServerConfig(self) -> object:
        conf = self.main_config["SERVER"]
        class WebConf:
            DEBUG = conf.getboolean("DEBUG")
            SECRET_KEY = conf.get("SECRET_KEY")
            PORT = self.conf["CONTROL_PORT"][1]
            HOST = conf.get("HOST")
            

        return WebConf
    
    def makeDir(self) -> None:
        if not os.path.exists(self.conf["ONIONS_DIR"]):
            os.mkdir(self.conf["ONIONS_DIR"])
        if not os.path.exists(self.conf["LOGS_DIR"]):
            os.mkdir(self.conf["LOGS_DIR"])
        if not os.path.exists(self.conf["TORRC_DIR"]):
            os.mkdir(self.conf["TORRC_DIR"])
        if not os.path.exists(self.conf["TOR_FILE_DIR"]):
            os.mkdir(self.conf["TOR_FILE_DIR"])
        if not os.path.exists(self.conf["CONTROLS_DIR"]):
            os.mkdir(self.conf["CONTROLS_DIR"])
        else:
            for fd in os.listdir(self.conf["CONTROLS_DIR"]):
                try:
                    os.unlink(os.path.join(self.conf["CONTROLS_DIR"], fd))
                except:
                    pass
    
    def clearLogFiles(self) -> None:
        for lf in os.listdir(self.conf["LOGS_DIR"]):
            try:
                os.remove(os.path.join(self.conf["LOGS_DIR"], lf))
            except OSError:
                pass

    
    def _prepareTor(self, count: str, port: tuple) -> object:
        name = f"{self.conf['ONION_NAME']}{count}"
        dir_lib = os.path.join(self.conf["TOR_FILE_DIR"], name)
        if not os.path.exists(dir_lib):
            os.mkdir(dir_lib)
            check = subprocess.run(["chmod", "g+s,g-x", dir_lib], capture_output=True, check=True, text=True)
        conf = f"## Custom Config: {name}\n"
        conf += f"\n## Control Socket:\nControlSocket {os.path.join(self.conf['CONTROLS_DIR'], name)} GroupWritable RelaxDirModeCheck\nControlSocketsGroupWritable 1\n"
        conf += f"\n## Send all messages of level 'notice' or higher\nLog notice file {os.path.join(self.conf['LOGS_DIR'], name)}\n"
        conf += f"\n## TOR data in 'onions' directory\nDataDirectory {dir_lib}\n"
        conf += f"\n## Socks Port\nSocksPort 0.0.0.0:{port[1]}"
        with open(os.path.join(self.conf["TORRC_DIR"], name), "w") as f:
            f.write(conf)
        self.onion_cfg[name] = {
            "NAME" : name,
            "CONTROL_SOCKET" : os.path.join(self.conf['CONTROLS_DIR'], name),
            "LOG_FILE" : os.path.join(self.conf['LOGS_DIR'], name),
            "LOG_SYS_FILE" : os.path.join(self.conf['LOGS_DIR'], "onion_portal.log"),
            "TOR_LIB_FILES" : dir_lib,
            "TORRC_PATH" : os.path.join(self.conf["TORRC_DIR"], name),
            "SOCKS_PORT" : port[1],
            "CONNECTOR_PORT" : port[0]
        }
        return self.onion_cfg[name]
        
    def prepareTor(self) -> None:
        c = 0
        for tor in self.conf["PORT_MAPPING"]:
            c += 1
            self._prepareTor(c, tor)
        self.clearLogFiles()
    
    def Start(self) -> None:
        self.makeDir()
        self.prepareTor()

        
        
    



