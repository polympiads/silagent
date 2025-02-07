
from typing import Any, List, Tuple
from silagent.core.fs import FileSystem

class BaseImage:
    @property
    def name (self) -> str:
        raise NotImplementedError()

class BaseImageBuilder:
    @property
    def name (self) -> str:
        raise NotImplementedError()
    
    def __init__(self, fs: FileSystem, *args, **kwargs):
        pass
    def build (self, *args, **kwargs) -> BaseImage:
        raise NotImplementedError()

class BaseBuilderProcess:
    def __init__(self, image_builders: List[BaseImageBuilder]):
        self.__image_builders = image_builders

    def build (self) -> List[BaseImage]:
        images = []
        
        for image_builder in self.__image_builders:
            images.append( image_builder.build() )
        
        return images
