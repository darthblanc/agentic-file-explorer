from langchain.tools import ToolException
from setup_directory import construct_directory_path
import os
from typing import List

def get_content(directory: str) -> List[str]:
    try:
        working_path = construct_directory_path(directory)
    except Exception as e:
        raise ToolException(e)

    try:
        return os.listdir(working_path)
    except Exception as e:
        raise ToolException(e)

def create(directory: str) -> str:
    try:
        working_path = construct_directory_path(directory)
        return f"Created directory: {working_path}"
    except Exception as e:
        raise ToolException(e)
