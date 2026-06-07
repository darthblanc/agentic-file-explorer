from pathlib import Path
import os


def _resolve(data_dir: str | None) -> Path:
    return Path(data_dir if data_dir is not None else os.environ.get("DATA_DIR", "data"))


def construct_file_path(path: str, data_dir: str | None = None) -> Path:
   """Create a Path object for a file.
      Ensure the data directory exists and return a Path for the file.
      File Path => {data_dir}/{path}.
   """
   base = _resolve(data_dir)
   base.mkdir(exist_ok=True)
   return base / path


def construct_directory_path(path: str, data_dir: str | None = None) -> Path:
   """Create a Path object for a directory.
      Ensure data_dir exists and create the requested subdirectory (with parents).
      Directory Path => {data_dir}/{path}.
   """
   base = _resolve(data_dir)
   working_directory = base / path
   working_directory.mkdir(exist_ok=True, parents=True)
   return working_directory


def construct_directory_path_limited(path: str, data_dir: str | None = None) -> Path:
   """Create a Path object for a directory.
      Ensure data_dir exists and create the requested directory (no parent dirs).
      Directory Path => {data_dir}/{path}.
   """
   base = _resolve(data_dir)
   working_directory = base / path
   working_directory.mkdir(exist_ok=True)
   return working_directory
