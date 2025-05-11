import os
import shutil
from pathlib import Path
from abc import ABC, abstractmethod
from typing import TypeVar


class AbstractFileSystem(ABC):

    @abstractmethod
    def copy(self, src: Path, dest: Path):
        raise NotImplementedError

    @abstractmethod
    def move(self, src: Path, dest: Path):
        raise NotImplementedError

    @abstractmethod
    def remove(self, src: Path):
        raise NotImplementedError


TFileSystem = TypeVar('TFileSystem', bound=AbstractFileSystem)


class LocalFileSystem(AbstractFileSystem):

    def copy(self, src: Path, dest: Path):
        shutil.copy(src, dest)

    def move(self, src: Path, dest: Path):
        shutil.move(src, dest)

    def remove(self, src: Path):
        os.remove(src)
