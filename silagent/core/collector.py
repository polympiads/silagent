
from typing import List, Set, Tuple
from silagent.core.error import LoadError
from silagent.core.fs import FileSystem

import shutil
import os

class Collector:
    __fs: "List[Tuple[str, FileSystem]]"
    __names: Set[str]
    
    def __init__(self):
        self.__fs = []
        self.__names = set()

    def add_to_collection (self, fs: FileSystem, service: str):
        listdir = fs.listsubfs()

        for dir in listdir:
            name = dir.basename

            if name in self.__names:
                raise LoadError(f"collector.{service}", f"Duplicated item '{name}'")

            self.__fs.append((name, dir))
    def collect (self, target: "FileSystem"):
        for index in range(len(self.__fs)):
            name, fs = self.__fs[index]
            newfs = target.subdir(name)
            shutil.copytree( fs.abspath, newfs.abspath )
            self.__fs[index] = name, newfs

    @property
    def collected (self):
        return self.__fs
