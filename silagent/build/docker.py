
from silagent.build.base import BaseImage, BaseImageBuilder
from silagent.core.error import LoadError
from silagent.core.fs import FileSystem

import docker
import docker.models.images

class DockerImage(BaseImage):
    def __init__(self, name: str, image: docker.models.images.Image):
        self.__name  = name
        self.__image = image
    @property
    def name (self):
        return self.__name

class DockerImageBuilder (BaseImageBuilder):
    __fs: FileSystem
    __folder: str
    __name  : str
    
    @property
    def name (self):
        return self.__name

    def __init__(self, fs, *args, **kwargs):
        self.__fs = fs

        if "name" not in kwargs:
            raise LoadError("docker.image", "Could not find the name of the image to build")
        self.__name = kwargs["name"]
        if not isinstance(self.__name, str):
            raise LoadError("docker.image", "The name should be a string")

        if "folder" not in kwargs:
            raise LoadError(f"docker.image[{self.__name}]", "Missing folder in the arguments to build the docker image")
        self.__folder = kwargs["folder"]
        if not isinstance(self.__folder, str):
            raise LoadError(f"docker.image[{self.__name}]", "The folder argument should be a string")

        super().__init__(fs, *args, **kwargs)
    def build(self, *args, **kwargs):
        print(f"  Building image {self.name}... ", end = "")
        path = self.__fs.subdir(self.__folder).abspath

        client   = docker.from_env()
        image, _ = client.images.build( path = path, tag = self.__name, rm = True )
        print("OK")

        return DockerImage(self.__name, image)
