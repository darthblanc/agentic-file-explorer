from langchain.tools import tool
from setup_directory import construct_directory_path
import os

@tool(description="List the files and subdirectories in a specified directory.")
def get_directory(directory: str) -> str:
    try:
        working_path = construct_directory_path(directory)
    except Exception as e:
        return f"{e}"
    
    content = os.listdir(working_path)
    directory_size = len(content)
    size_string = ""

    if directory_size > 1:
        size_string = f"{directory_size} items [{", ".join(content)}]"
    elif directory_size == 1:
        size_string = f"{directory_size} item [{", ".join(content)}]"
    else:
        size_string = f"{directory_size} items"

    try:
        return f"Listed: {size_string} from directory ({directory})"
    except Exception as e:
        return f"Error encountered while reading from directory ({directory}): {e}"
    
@tool(description="Create a specified directory.")
def create_directory(directory: str) -> str:
    try:
        working_path = construct_directory_path(directory)
        return f"Created directory: {working_path}"
    except Exception as e:
        return f"{e}"
    
directory_tools = [
    get_directory,
    create_directory
]
