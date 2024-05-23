import os
import subprocess
import threading

from threading import Thread
from time import sleep
from typing import Union
from datetime import datetime

from .logger import Logger
from .controler import Controler
from .scout import Scout


class Onion(Thread):
    def __init__(self, onion_conf: dict, stop_event: object):
        super().__init__()
        self.name = onion_conf["NAME"]
        self.config = onion_conf
        self.stop_event = stop_event
        self.proc_pause = 1
        self.proc_TOR = None
        self.status = "Ready to Start"
        self.log = Logger(self, self.config["LOG_SYS_FILE"])
        self.ctrl = Controler(self)
        self._is_start = False
        self.scout = Scout(self)
    
    @property
    def status_TOR(self) -> bool:
        return self.ctrl.checkTORconn()
    
    @property
    def ip(self) -> str:
        ip = self.scout._ip
        if ip:
            return ip
        else:
            if self.scout._workFLAG:
                return "checking"
            else:
                return "unknown"
    
    @property
    def torLogs(self) -> str:
        if not os.path.exists(self.config["LOG_FILE"]):
            return "No logs"
        else:
            with open(self.config["LOG_FILE"], "r") as f:
                data = f.read()
            return data
    
    @property
    def info(self) -> dict:
        return self._info()

    
    def _info(self) -> dict:
        info = {
            "NAME" : self.name,
            "STATUS" : self.status,
            "SOCKS_PORT" : self.config["SOCKS_PORT"],
            "OUT_PORT" : self.config["CONNECTOR_PORT"],
            "INFO_TOR" : self.status_TOR,
            "EXIT_NODE" : self.ip,
        }
        return info
    
    def showLogs(self) -> str:
        return self.log.readLog()
    
    def torStart(self) -> None:
        self.stop_event.clear()
        cmd = ["tor", "-f", self.config["TORRC_PATH"]]
        self._is_start = True
        try:
            self.status = "working"
            self.log("Starting TOR ......")
            self.proc_TOR = subprocess.Popen(cmd, text=True, stdout=subprocess.PIPE)
            self.ctrl.work()
            self.checkStatusTOR()
            while not self.stop_event.is_set():
                sleep(self.proc_pause)
        except Exception as e:
            self.status = "ERROR"
            self.log(f"ERROR: {e}")
        finally:
            self.terminateTOR()
            self.log("Terminate TOR")
    
    def terminateTOR(self) -> None:
        self.status = "terminate"
        try:
            self.ctrl.ctrl.close()
        except:
            pass

        if self.proc_TOR:
            try:
                self.proc_TOR.terminate()
            except:
                try:
                    self.proc_TOR.kill()
                except:
                    pass
        else:
            self.log("No TOR Process")
    
    def checkStatusTOR(self) -> None:
        while not self.stop_event.is_set():
            if self.status_TOR:
                self.log("Connected to TOR")
                break
            sleep(self.proc_pause)
    
    def newCircuit(self) -> None:
        circuit = Thread(target=self.ctrl.newCircuit)
        circuit.start()
     
    
    def stop(self) -> None:
        self.stop_event.set()
    
    def run(self) -> None:
        self.torStart()
    
    def START(self) -> None:
        if not self._is_start:
            self.start()
    
