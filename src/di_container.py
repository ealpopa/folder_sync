from pathlib import Path
from src.config import Config
from src.syncer.syncer import FolderSyncer


class DIContainer:

    def __init__(self, config: Config):
        self._config = config

        self._hash_function = self._config.file_reader_hash_function
        self._reader = self._config.file_reader_class(self._hash_function)
        self._file_system = self._config.file_system_class()
        self._interval_seconds = self._config.sync_interval_seconds

    def get_syncer_instance(self, src_root: Path, dest_root: Path) -> FolderSyncer:
        return FolderSyncer(src_root, dest_root, self._reader, self._file_system, self._interval_seconds)
