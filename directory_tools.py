from langchain.tools import tool, ToolException
from setup_directory import construct_directory_path
import os
from typing import List
import json

configs = json.load(open("configs/tool_config.json"))
DIRECTORY_TOOL_DESCRIPTIONS = configs["DirectoryTools"]["functions"]

@tool(description=DIRECTORY_TOOL_DESCRIPTIONS["get_directory_content"])
def get_directory_content(directory: str) -> List[str]:
    try:
        working_path = construct_directory_path(directory)
    except Exception as e:
        raise ToolException(e)

    try:
        return os.listdir(working_path)
    except Exception as e:
        raise ToolException(e)
    
@tool(description=DIRECTORY_TOOL_DESCRIPTIONS["create_directory"])
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
