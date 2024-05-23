import os

from threading import Event

from .portal.logger import Logger
from .portal.onion import Onion
from .portal.supervisor import SuperVisor


class OnionPortal:
    def __init__(self, constructor_class: object):
        self.name = "OnionPortal"
        self.constructor = constructor_class()
        self.constructor.Start()
        self.serv_conf = self.constructor.server_conf
        self.onions = {}
        self.stop_events = {}
        self.extra_ports = list(self.conf["EXTRA_PORT"])
        self.log_file_path = os.path.join(self.constructor.conf["LOGS_DIR"], "onion_portal.log")
        self.log = Logger(self, self.log_file_path)
        self.log("Portal Start")
        self.supervisor = SuperVisor(self)
        self.supervisor.start()


    
    @property
    def conf(self) -> dict:
        return self.constructor.conf.copy()
    
    def showLogs(self) -> str:
        return self.log.readLog()
    
    def makeOnions(self) -> None:
        c = 0
        for oc in self.constructor.onion_cfg.values():
            stop = Event()
            onion = Onion(oc, stop)
            self.onions[onion.name] = onion
            self.stop_events[onion.name] = stop
            c += 1
        self.log(f"Making {c} portals")
    
    def addOnion(self, port_num: str) -> None:
        ports = []
        for p in port_num.split(", "):
            ports.append(int(p.strip("()")))
        port_num = tuple(ports)
        self.extra_ports.remove(port_num)
        c = len(self.onions) + 1
        bname = self.constructor.conf["ONION_NAME"]
        while f"{bname}{c}" in self.onions.keys():
            c += 1
        conf = self.constructor._prepareTor(c, port_num)
        stop = Event()
        new = Onion(conf, stop)
        self.onions[new.name] = new
        self.stop_events[new.name] = stop
        self.log(f"New portal added: {new.name}")

    def showOnions(self) -> list:
        onions = []
        for o in self.onions.values():
            onions.append(o.info)
        return onions
    
    def startPortals(self) -> None:
        for o in self.onions.values():
            o.START()
    
    def stopPortals(self) -> None:
        for o in self.onions.values():
            o.stop()
    
    def newCircuit(self) -> None:
        for o in self.onions.values():
            o.newCircuit()
    

