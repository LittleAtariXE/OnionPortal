import requests
import json

from threading import Thread
from typing import Union


class Scout:
    def __init__(self, onion_callback: object):
        self.onion = onion_callback
        self.socks_port = self.onion.config["SOCKS_PORT"]
        self.socks = self.getTorSocks()
        self._ip = None
        self._workFLAG = False
        
    
    def getTorSocks(self) -> object:
        socks = requests.session()
        socks.proxies = {
            "http" : f"socks5h://127.0.0.1:{self.socks_port}",
            "https" : f"socks5h://127.0.0.1:{self.socks_port}"
        }
        return socks
    
    def get_ip(self) -> Union[str, None]:
        # if self._ip:
        #     return self._ip
        self._workFLAG = True
        ip = self.get_IpIffy()
        if ip:
            return self.get_ip_done(ip)
        ip = self.get_HttpBinOrg()
        if ip:
            return self.get_ip_done(ip)
        self._workFLAG = False
        return None

    def get_ip_done(self, ip: str) -> str:
        self._workFLAG = False
        self._ip = ip
        return ip
    
    def get_HttpBinOrg(self) -> str:
        try:
            ip = self.socks.get("http://httpbin.org/ip")
        except:
            return None
        try:
            ip = ip.json()
            ip = ip["origin"]
        except:
            return None
        self.onion.log(f"Exit Node: {ip}")
        return ip

    
    def get_IpIffy(self) -> Union[str, None]:
        try:
            ip = self.socks.get("https://api.ipify.org?format=json")
        except Exception as e:
            print("ERROR: ", e)
            return None
        try:
            ip = ip.json()
            ip = ip["ip"]
        except:
            return None
        self.onion.log(f"Exit Node: {ip}")
        return ip
    
    def obtainIP(self) -> None:
        if not self._workFLAG:
            self._th_ip = Thread(target=self.get_ip, daemon=True)
            self._th_ip.start()
    
    