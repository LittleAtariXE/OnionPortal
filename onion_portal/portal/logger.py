import os
from datetime import datetime
from threading import Lock


class Logger:
    def __init__(self, onion_callback: object, file_log_path: str):
        self.onion = onion_callback
        self.lock = Lock()
        self.log_file = file_log_path
        self.makeLogFile()
    
    def time(self) -> str:
        _time = datetime.now()
        return _time.strftime('%d:%m:%Y  %H:%M')

    def makeLogFile(self) -> None:
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                f.write(f"{self.time()} -- START LOG FILE\n-----------------------------------------------------------------\n")
    
    def addLog(self, text: str) -> None:
        with self.lock:
            with open(self.log_file, "a+") as f:
                f.write(f"\n{self.time()} -- {self.onion.name} -- {text}")
    
    def readLog(self) -> str:
        with open(self.log_file, "r") as f:
            data = f.read()
        return data
    
    def __call__(self, text: str) -> None:
        self.addLog(text)

                