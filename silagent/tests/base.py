
from typing import List
from silagent.container.base import BaseContainer

class BaseCommand:
    def __init__(self, __name: str, **kwargs):
        self.__name = __name
    @property
    def name (self):
        return self.__name
    
    def execute (self, container: BaseContainer, args: List[str]):
        raise NotImplementedError()
