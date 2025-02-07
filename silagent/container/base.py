
import base64
from typing import List

class Result:
    def __init__(self, exit_code: int, output: str):
        self.exit_code = exit_code
        self.output    = output

class BaseContainer:
    def __init__(self, name: str):
        self.__name = name
    
    @property
    def name (self):
        return self.__name

    def exec (self, cmd: List[str]) -> Result:
        raise NotImplementedError()
    def exec_script (self, script: str):
        b64 = "".join(base64.encodebytes( script.encode("utf-8") ).decode("utf-8").split("\n"))

        b64echo = f"echo {b64}"
        b64dec  = f"base64 -d"
        b64run  = f"sh"
        
        return self.exec( [ "sh", "-c", f"{b64echo} | {b64dec} | {b64run}" ] )
