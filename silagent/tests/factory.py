
from silagent.core.error import LoadError
from silagent.tests.python import PythonCommand


class CommandFactory:
    @classmethod
    def create_command (cls, __name: str, **kwargs):
        if "engine" not in kwargs:
            raise LoadError("command.factory", f'Could not find "engine" field in command "{__name}"')
        engine = kwargs["engine"]

        if engine == "Python":
            return PythonCommand( __name, **kwargs )
        raise LoadError("command.factory", f'Could not find engine "{engine}" for command "{__name}"')