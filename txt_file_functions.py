from langchain.tools import tool, ToolException
from setup_directory import construct_file_path
from typing import List

@tool(description="Read the contents of a txt file specified by a path.")
def read_txt(path: str) -> str:
    working_path = construct_file_path(path)

    try:
        with open(working_path, "r") as fd:
            return fd.read()
    except Exception as e:
        raise ToolException(e)
    
@tool(description="Read the contents of a txt file specified by a path as a list of lines.")
def read_txt_lines(path: str) -> List[str]:
    working_path = construct_file_path(path)

    try:
        with open(working_path, "r") as fd:
            return fd.readlines()
    except Exception as e:
        raise ToolException(e)

@tool(description="Write new content to a txt file specified by a path. This tool will overwrite the previous content of the txt file.")
def write_to_txt(path: str, content: str) -> str:
    working_path = construct_file_path(path)

    try:
        with open(working_path, "w") as fd:
            fd.write(content)
            return f"Wrote {content[:15]}... to ({path})"
    except Exception as e:
        raise ToolException(e)

@tool(description="Write new content to a txt file specified by a path. This tool will append the new content to a new line after the previous content of the txt file.")
def append_to_txt(path: str, content: str) -> str:
    working_path = construct_file_path(path)

    try:
        with open(working_path, "a") as fd:
            fd.write(f"\n{content}")
            return f"Wrote: {content[:15]}... to ({path})"
    except Exception as e:
        raise ToolException(e)

@tool(description="Clear the contents of a file specified by a path.")
def clear(path: str) -> str:
    working_path = construct_file_path(path)

    try:
        with open(working_path, "w") as fd:
            fd.write("")
            return f"Cleared content from ({path})"
    except Exception as e:
        raise ToolException(e)

txt_tools = [
    read_txt,
    read_txt_lines,
    write_to_txt,
    append_to_txt,
    # clear,
]
