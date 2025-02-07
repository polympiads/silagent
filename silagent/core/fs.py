
import os
from typing import List

class FileSystem:
    def __init__ (self, path: str):
        self.__path = path

    def parent (self) -> "FileSystem":
        return FileSystem( os.path.dirname(self.__path) )
    def subdir (self, path: str):
        return FileSystem( os.path.join(self.__path, path) )
    
    def open (self, file: str, mode: str):
        return open( os.path.join(self.__path, file), mode )

    def is_file (self):
        return os.path.isfile(self.abspath)
    def is_dir (self):
        return os.path.isdir(self.abspath)

    def listdir (self) -> "List[str]":
        return os.listdir(self.abspath)
    def listsubfs (self) -> "List[FileSystem]":
        sub = self.listdir()

        lfs = []
        for s in sub:
            nfs = self.subdir(s)

            if nfs.is_dir():
                lfs.append(nfs)
        return lfs

    @property
    def abspath (self):
        return os.path.abspath( self.__path )
    @property
    def basename (self):
        return os.path.basename( self.abspath )

def get_silagent_root () -> FileSystem:
    return FileSystem(
        __file__
    ).parent().parent()
