from time import sleep
from pathlib import Path
from typing import Generic

from src.reader.reader import TReader
from src.file_system.file_system import TFileSystem


class FolderSyncer(Generic[TReader]):

    COPY = "COPY"
    DELETE = "DELETE"
    MOVE = "MOVE"

    def __init__(self, src_root: Path, dest_root: Path, reader: TReader, file_system: TFileSystem, interval_seconds: int):
        self._src_root = src_root
        self._dest_root = dest_root
        self._reader = reader
        self._file_system = file_system
        self._interval_seconds = interval_seconds

        self._src_hashes = {}
        self._dest_hashes = {}

    def run_loop(self):
        try:
            while True:
                print("CHECKING...")
                self.run_once()
                print("SLEEPING...")
                sleep(self._interval_seconds)
        except KeyboardInterrupt:
            print("User interrupted")

    def run_once(self):
        self._read_paths_and_hashes()

        for (command, src, dest) in self._get_file_system_commands():
            if command == FolderSyncer.DELETE:
                self._file_system.remove(dest)
            elif command == FolderSyncer.COPY:
                self._file_system.copy(src, dest)
            elif command == FolderSyncer.MOVE:
                self._file_system.move(src, dest)

    def _read_paths_and_hashes(self):
        self._src_hashes = self._reader.read(self._src_root)
        self._dest_hashes = self._reader.read(self._dest_root)

    def _get_file_system_commands(self):
        for f_hash in self._dest_hashes:
            if f_hash not in self._src_hashes:
                yield FolderSyncer.DELETE, None, self._dest_hashes[f_hash]

        for f_hash in self._src_hashes:
            if f_hash not in self._dest_hashes:
                yield FolderSyncer.COPY, self._src_hashes[f_hash], self._dest_root
            elif self._dest_hashes[f_hash] != self._src_hashes[f_hash]:
                new_filename = self._src_hashes[f_hash].name
                new_dest_path = self._dest_root / new_filename
                yield FolderSyncer.MOVE, self._dest_hashes[f_hash], new_dest_path
