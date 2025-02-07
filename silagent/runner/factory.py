
from silagent.core.error import LoadError
from silagent.core.yaml import load_yaml
from silagent.core.fs import FileSystem
from silagent.runner.compose import DockerComposeEngine


class RunnerEngineFactory:
    @classmethod
    def find_runner_engine (cls, name: str, fs: "FileSystem"):
        with fs.open("runner.yaml", "r") as file:
            yaml = load_yaml(file.read())
        
        if "engine" not in yaml:
            raise LoadError("runner.factory", f'Could not find "engine" field in "{name}" runner')
        engine = yaml["engine"]
        if engine == "Docker Compose":
            return (DockerComposeEngine( fs ), yaml)
        raise LoadError("runner.factory", f'Invalid "engine" field in "{name}" runner, "{engine}" not found')
