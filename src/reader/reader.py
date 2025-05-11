import os
from pathlib import Path
from abc import ABC, abstractmethod
from typing import TypeVar, Callable, Dict


class AbstractFileReader(ABC):

    @abstractmethod
    def read(self, root: Path) -> Dict[str, str]:
        pass


TReader = TypeVar('TReader', bound=AbstractFileReader)


class LocalFileReader(AbstractFileReader):

    BUFFER_SIZE = 64 * 1024

    def __init__(self, hashing_function: Callable):
        self._hashing_function = hashing_function

    def read(self, root: Path):
        hashes = {}

        for folder, _, files in os.walk(root):
            for file in files:
                path = Path(folder, file)
                file_hash = self._hash_file(path)
                hashes[file_hash] = path

        return hashes

    def _hash_file(self, file_path: Path) -> str:
        file_hash = self._hashing_function()

        with open(file_path, 'rb') as f:
            chunk = f.read(LocalFileReader.BUFFER_SIZE)
            while chunk:
                file_hash.update(chunk)
                chunk = f.read(LocalFileReader.BUFFER_SIZE)

        return file_hash.hexdigest()
