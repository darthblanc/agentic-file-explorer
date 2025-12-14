from pathlib import Path
import os

def _data_dir_path() -> Path:
    return Path(os.environ["DATA_DIR"])


def construct_file_path(path: str):
   """Create a Path object for a file.
      Ensure the environment `DATA_DIR` directory exists and return a Path for the file.
      File Path => {DATA_DIR}/{path}.
   """

   data_dir = _data_dir_path()
   data_dir.mkdir(exist_ok=True)

   return data_dir / path

def construct_directory_path(path: str) -> Path:
   """Create a Path object for a directory.
      Ensure the environment `DATA_DIR` exists and create the requested subdirectory (with parents).
      Directory Path => {DATA_DIR}/{path}.
   """

   data_dir = _data_dir_path()
   working_directory = data_dir / path
   working_directory.mkdir(exist_ok=True, parents=True)

   return working_directory

def construct_directory_path_limited(path: str) -> Path:
   """Create a Path object for a directory.
      Ensure the environment `DATA_DIR` exists and create the requested directory (no parent dirs).
      Directory Path => {DATA_DIR}/{path}.
   """

   data_dir = _data_dir_path()
   working_directory = data_dir / path
   working_directory.mkdir(exist_ok=True)

   return working_directory