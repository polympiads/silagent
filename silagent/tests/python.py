
from typing import List
from silagent.core.error import LoadError
from silagent.tests.base import BaseCommand


class PythonCommand(BaseCommand):
    __path: List[str]

    def __init__(self, __name, **kwargs):
        super().__init__(__name, **kwargs)

        self.__path = kwargs.get( "path", [] )
        if not isinstance(self.__path, list):
            raise LoadError("python.command", 'The "path" field of a python engine should be an array of paths')

    def execute(self, container, args):
        PYTHONPATH = ":".join( self.__path )

        script = [
            f"export PYTHONPATH={PYTHONPATH}",
            f"python3 /silagent/{self.name}/main.py " + (" ".join(args))
        ]
        
        return container.exec_script( "\n".join(script) )
