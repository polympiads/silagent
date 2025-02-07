
import docker.models.containers

from typing import List
from silagent.container.base import BaseContainer, Result

class DockerContainer(BaseContainer):
    def __init__(self, name: str, container: docker.models.containers.Container):
        super().__init__(name)

        self.__container = container
    def exec(self, cmd: List[str]) -> Result:
        exec_result = self.__container.exec_run( cmd )

        return Result( exec_result.exit_code, exec_result.output.decode("utf-8") )
