
from typing import Any

from silagent.core.collector import Collector
from silagent.core.error import LoadError
from silagent.core.fs import FileSystem

class CommandsLoader:
    @classmethod
    def load (self, fs: FileSystem, yaml: Any) -> Collector:
        assert isinstance(yaml, list)
        
        commands_yaml = None

        for _yml in yaml:
            if isinstance(_yml, dict) and "commands" in _yml:
                if commands_yaml is not None:
                    raise LoadError("commands.loader", 'The "commands" parameter appears more than once.')
                commands_yaml = _yml["commands"]

        if commands_yaml is None:
            raise LoadError("commands.loader", 'The "commands" parameter does not appear.')
        if not isinstance(commands_yaml, list):
            raise LoadError("commands.loader", 'The "commands" parameter should be an array of folders')
        
        commands_collector = Collector()
        for command_folder in commands_yaml:
            commands_collector.add_to_collection( fs.subdir(command_folder), "commands" )

        return commands_collector
