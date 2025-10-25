from langchain.tools import tool
from setup_directory import construct_file_path, construct_directory_path
import os

@tool(description="Read the contents of a file specified by a path.")
def read(path: str) -> str:
    working_path = construct_file_path(path)

    try:
        with open(working_path, "r") as fd:
            return fd.read()
    except Exception as e:
        return f"Error encountered while reading from file ({path}): {e}"

@tool(description="Write new content to a file specified by a path. This tool will overwrite the previous content of the file.")
def write(path: str, content: str) -> str:
    working_path = construct_file_path(path)

    try:
        with open(working_path, "w") as fd:
            fd.write(content)
            return f"Wrote: content to ({path})"
    except Exception as e:
        return f"Error encountered while writing to file ({path}): {e}"

@tool(description="Write new content to a file specified by a path. This tool will append the new content to the previous content of the file.")
def append(path: str, content: str) -> str:
    working_path = construct_file_path(path)

    try:
        with open(working_path, "a") as fd:
            fd.write(content)
            return f"Wrote: content to ({path})"
    except Exception as e:
        return f"Error encountered while writing to file ({path}): {e}"

@tool(description="Clear the contents of a file specified by a path.")
def clear(path: str) -> str:
    working_path = construct_file_path(path)

    try:
        with open(working_path, "w") as fd:
            fd.write("")
            return f"Cleared: content in ({path})"
    except Exception as e:
        return f"Error encountered while writing to file ({path}): {e}"

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

tools = [
    read,
    write,
    append,
    # clear,
    get_directory
]
