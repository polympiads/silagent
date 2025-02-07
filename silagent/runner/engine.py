
from typing import List
from silagent.container.base import BaseContainer
from silagent.core.fs import FileSystem

class BaseRunnerEngine:
    def __init__ (self, runner: FileSystem):
        self.runner = runner
    def prepare (self, **kwargs):
        pass

    @property
    def names (self) -> List[str]:
        raise NotImplementedError()

    def run (self) -> "List[BaseContainer]":
        raise NotImplementedError()
    def close (self):
        raise NotImplementedError()
