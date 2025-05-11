from typing import Type
from src.reader.reader import LocalFileReader, AbstractFileReader, Callable
from src.file_system.file_system import LocalFileSystem, AbstractFileSystem
from hashlib import sha1


class Config:

    file_reader_class: Type[AbstractFileReader] = LocalFileReader
    file_reader_hash_function: Callable = sha1

    file_system_class: Type[AbstractFileSystem] = LocalFileSystem

    sync_interval_seconds = 5
