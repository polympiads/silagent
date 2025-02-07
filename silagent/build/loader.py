
from silagent.build.base import BaseBuilderProcess
from silagent.build.factory import ImageBuilderFactory
from silagent.core.error import LoadError
from silagent.core.fs import FileSystem

class BuildLoader:
    @classmethod
    def load (self, fs: FileSystem, yaml) -> BaseBuilderProcess:
        if "build" not in yaml:
            raise LoadError('build.loader', 'Could not find the "build" process')
        
        build_process = yaml["build"]
        if not isinstance(build_process, list):
            raise LoadError('build.loader', 'The "build" process should be an array of images to build')

        image_builders = []
        for index, build_image in enumerate(build_process):
            if not isinstance( build_image, dict ):
                raise LoadError(f'build.loader[{index}]', "The build images should be a dictionary of parameters")
            
            try:
                image_builder = ImageBuilderFactory.create_image_builder( fs, **build_image )

                image_builders.append(image_builder)
            except LoadError as error:
                raise LoadError(f'build.loader[{index}]', "An error occured when creating the image builder", error)

        return BaseBuilderProcess( image_builders )
