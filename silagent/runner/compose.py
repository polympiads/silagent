
from typing import List
import docker
from silagent.container.docker import DockerContainer
from silagent.core.error import LoadError
from silagent.core.yaml import dump_yaml, load_yaml
from silagent.core.fs import FileSystem
from silagent.runner.engine import BaseRunnerEngine

import subprocess

import random
import string

def random_string (k: int):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=k))

class DockerComposeEngine (BaseRunnerEngine):
    def __init__(self, runner: "FileSystem"):
        super().__init__(runner)

        self.__uuid     = random_string(12)
        self.__services = []

        self.__volume_name = f"{self.__uuid}-volume"

    @property
    def names (self) -> List[str]:
        return list(map(lambda x: x[1], self.__services))
    def process_service (self, name: str, service_yaml):
        container_name = service_yaml["container_name"] = self.__uuid + "-cont-" + name
        
        if "volumes" not in service_yaml:
            service_yaml["volumes"] = []
        volumes = service_yaml["volumes"]
        if not isinstance(volumes, list):
            raise LoadError(f"runner.docker-compose[{name}]", 'The "volumes" field should be an array')
        volumes.append(f"{self.__volume_name}:/silagent")
        
        self.__services.append((container_name, name))

    def prepare(self, volume: "FileSystem", **kwargs):
        with self.runner.open( "docker-compose.yaml", "r" ) as file:
            yaml = load_yaml(file.read())

        if "services" not in yaml:
            raise LoadError ("runner.docker-compose", 'Missing "services" field in docker-compose.yaml')
        services = yaml["services"]
        if not isinstance(services, dict):
            raise LoadError ("runner.docker-compose", '"services" field in docker-compose.yaml should be a dictionary')

        for name in services.keys():
            self.process_service(name, services[name])
        
        if "volumes" not in yaml:
            yaml["volumes"] = {}
        volumes = yaml["volumes"]
        if not isinstance(volumes, dict):
            raise LoadError ("runner.docker-compose", '"volumes" field in docker-compose.yaml should be a dictionary')

        volumes[self.__volume_name] = {
            "driver": "local",
            "driver_opts": {
                "type": 'none',
                "o": 'bind',
                "device": volume.abspath
            }
        }
        
        with self.runner.open( "docker-compose.yaml", "w" ) as file:
            file.write(dump_yaml(yaml))

        return super().prepare(**kwargs)

    def run(self):
        result = subprocess.run(
            [ "docker", "compose", "up", "-d" ],
            cwd = self.runner.abspath,
            capture_output = True,
            text = True
        )

        client = docker.from_env()
        containers = client.containers.list()
        containers_dict = {}
        for container in containers:
            containers_dict[ container.name ] = container
        
        containers = []
        for container_name, service_name in self.__services:
            containers.append( DockerContainer( service_name, containers_dict[container_name] ) )
        
        return containers
    def close (self):
        result = subprocess.run(
            [ "docker", "compose", "down" ],
            cwd = self.runner.abspath,
            capture_output = True,
            text = True
        )