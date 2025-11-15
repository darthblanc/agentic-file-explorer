from langchain.tools import tool, ToolException
from setup_directory import construct_directory_path
import os
from typing import List

@tool(description="List the files and subdirectories in a specified directory.")
def get_directory_content(directory: str) -> List[str]:
    try:
        working_path = construct_directory_path(directory)
    except Exception as e:
        raise ToolException(e)

    try:
        return os.listdir(working_path)
    except Exception as e:
        raise ToolException(e)
    
@tool(description="Create a specified directory.")
def create_directory(directory: str) -> str:
    try:
        working_path = construct_directory_path(directory)
        return f"Created directory: {working_path}"
    except Exception as e:
        raise ToolException(e)
    
directory_tools = [
    get_directory_content,
    create_directory
]
