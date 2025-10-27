from pathlib import Path
import os

# DATA_DIR = Path(os.environ["DATA_DIR"])
DATA_DIR = Path("data")

def construct_file_path(path: str):
   """Create a Path object for a file.\n
      Create a directory called \"data\" if not already in existence.\n
      This is where all operations will be observed.\n
      File Path => data/{path}.
   """

   working_directory = DATA_DIR
   working_directory.mkdir(exist_ok=True)

   return DATA_DIR / path

def construct_directory_path(path: str) -> Path:
   """Create a Path object for a directory.\n
      Create a directory called \"data\" if not already in existence.\n
      This is where all operations will be observed.\n
      Directory Path => data/{path}.
   """

   working_directory = DATA_DIR / path
   working_directory.mkdir(exist_ok=True, parents=True)

   return working_directory    

def construct_directory_path_limited(path: str) -> Path:
   """Create a Path object for a directory.\n
      Create a directory called \"data\" if not already in existence.\n
      This is where all operations will be observed.\n
      Directory Path => data/{path}.
      Will not automatically create any subdirectories.
   """

   working_directory = DATA_DIR / path
   working_directory.mkdir(exist_ok=True)

   return working_directory  