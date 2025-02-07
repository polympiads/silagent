
from silagent.build.base import BaseImageBuilder
from silagent.build.docker import DockerImageBuilder

from typing import Type

from silagent.core.error import LoadError
from silagent.core.fs import FileSystem

class ImageBuilderFactory:
    @classmethod
    def find_image_builder (cls, engine: str) -> Type[BaseImageBuilder]:
        if engine == "Docker":
            return DockerImageBuilder

        raise LoadError("build.factory", f"Could not find the engine {engine}")

    @classmethod
    def create_image_builder (cls, fs: FileSystem, *args, **kwargs) -> BaseImageBuilder:
        if "engine" not in kwargs:
            raise LoadError("build.factory", "Could not find the engine parameter to determine the way to build the container")
        
        return cls.find_image_builder( kwargs["engine"] )(fs, *args, **kwargs)
