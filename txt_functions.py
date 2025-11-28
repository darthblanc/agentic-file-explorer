import os
os.environ.setdefault("DATA_DIR", "data")

from langchain.tools import ToolException
from setup_directory import construct_file_path
from file_dictionary import file_dict
from file import File

def read(path: str) -> str:
    working_path = construct_file_path(path)
    
    if path in file_dict:
        return file_dict.files[path].get_content()
    
    try:
        with open(working_path, "r") as fd:
            content = fd.read()
            file_dict.add(File.new_file(path, content, "text/plain"))
            return content
    except Exception as e:
        raise ToolException(e)

def write(path: str, content: str) -> str:
    working_path = construct_file_path(path)
    try:
        with open(working_path, "w") as fd:
            fd.write(content)
            file_dict.add(File.new_file(path, content, "text/plain"))
            return f"Wrote {content[:15]}... to ({path})"
    except Exception as e:
        raise ToolException(e)

def append(path: str, content: str) -> str:
    working_path = construct_file_path(path)
    try:
        with open(working_path, "a") as fd:
            fd.write(f"\n{content}")
            file_dict.add(File.new_file(path, content, "text/plain"))
            return f"Wrote: {content[:15]}... to ({path})"
    except Exception as e:
        raise ToolException(e)

def clear(path: str) -> str:
    working_path = construct_file_path(path)
    try:
        with open(working_path, "w") as fd:
            fd.write("")
            file_dict.add(File.new_file(path, "", "text/plain"))
            return f"Cleared content from ({path})"
    except Exception as e:
        raise ToolException(e)
