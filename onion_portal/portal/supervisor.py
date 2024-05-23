from threading import Thread, Event
from time import sleep

from .onion import Onion

class SuperVisor(Thread):
    def __init__(self, onion_portal_callback: object):
        super().__init__(daemon=True)
        self.name = "SuperVisor"
        self.op = onion_portal_callback
        self.proc_pause = 2
        self.log = self.op.log
    
    def _reloadOnion(self, name: str) -> None:
        old = self.op.onions.get(name)
        conf = old.config.copy()
        stop = Event()
        self.op.stop_events[name] = stop
        self.op.onions[name] = Onion(conf, stop)
        self.log(f"< {name} > Reloaded. Ready to start.")
    
    def reloadOnion(self) -> None:
        for onion in self.op.onions.values():
            if onion.status == "terminate":
                self._reloadOnion(onion.name)
    
    def checkIP(self) -> None:
        for onion in self.op.onions.values():
            if onion.status == "terminate" or onion.status == "Ready to Start":
                continue
            if onion.ip == "unknown":
                onion.scout.obtainIP()
    
    def work(self) -> None:
        while True:
            sleep(self.proc_pause)
            self.reloadOnion()
            self.checkIP()
    
    def run(self) -> None:
        self.work()

