import socket
import os
import requests
import re

from threading import Thread
from typing import Union
from time import sleep

class Controler:
    def __init__(self, onion_callback: object):
        self.onion = onion_callback
        self.ctrl_socket_path = self.onion.config["CONTROL_SOCKET"]
        self.raw_len = 2048
        self.format = "utf-8"
        self.socket_timeout = 2
        self.log = self.onion.log
        self.stop_event = self.onion.stop_event
        self._is_conn = False
    

    def controlerConn(self) -> bool:
        try:
            self.ctrl = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.ctrl.connect(self.ctrl_socket_path)
            self.ctrl.settimeout(self.socket_timeout)
            self.log("Connected to Control Socket")
            self.sendMsg('AUTHENTICATE ""\r\n')
            msg = self.reciveMsg()
            if msg:
                self.log(f"Control Response: {msg}")
            return True
        except:
            return False
    
    def reciveMsg(self) -> Union[str, None]:
        msg = b""
        while not self.stop_event.is_set():
            try:
                recv = self.ctrl.recv(self.raw_len)
            except TimeoutError:
                self.log("ERROR: Socket Timeout")
                return None
            except (BrokenPipeError, ConnectionResetError, ConnectionError, ConnectionAbortedError) as e:
                self.log(f"ERROR Recive Message from Control Socket")
                return None
            if recv:
                if len(recv) < self.raw_len:
                    msg += recv
                    break
                else:
                    msg += recv
            else:
                return None
        return msg.decode(self.format)
    
    def sendMsg(self, msg: str) -> None:
        if not msg.endswith("\r\n"):
            msg += "\r\n"
        try:
            self.ctrl.sendall(msg.encode(self.format))
        except (BrokenPipeError, ConnectionResetError, ConnectionError, ConnectionAbortedError) as e:
            self.log(f"ERROR Control Socket send command: {e}")
    
    def checkTORconn(self) -> bool:
        if not self._is_conn:
            return False
        self.sendMsg("GETINFO status/bootstrap-phase\r\n")
        resp = self.reciveMsg()
        if not resp:
            return False
        buff = re.search(r"PROGRESS=(\d+)", resp)
        if buff:
            progress = buff.group(1)
            if progress == "100":
                return True
        return False
    
    def newCircuit(self) -> None:
        self.sendMsg("SIGNAL NEWNYM\r\n")
        resp = self.reciveMsg()
        if not resp:
            self.log("No response")
        else:
            self.log(f"Response: {resp}")
        self.onion.scout._ip = None
        


    def _work(self) -> None:
        while not self.stop_event.is_set():
            self._is_conn = self.controlerConn()
            if self._is_conn:
                break
            sleep(0.5)
    
    def work(self):
        work = Thread(target=self._work, daemon=True)
        work.start()
        while not self._is_conn:
            sleep(0.5)
        