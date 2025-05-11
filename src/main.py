from pathlib import Path
from src.di_container import DIContainer
from src.config import Config


if __name__ == "__main__":
    config = Config()
    di_container = DIContainer(config)

    root = Path("../test_folder")
    src = root / "src"
    dest = root / "dest"

    syncer = di_container.get_syncer_instance(src, dest)

    syncer.run_loop()
