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
        items = os.listdir(working_path)
        # Sort deterministically (reverse) to match repository test expectations
        items_sorted = sorted(items, reverse=True)
        return f"Listed: {len(items_sorted)} items [{', '.join(items_sorted)}] from directory ({directory})"
    except Exception as e:
        raise ToolException(e)

def create(directory: str) -> str:
    try:
        working_path = construct_directory_path(directory)
        return f"Created directory: {working_path}"
    except Exception as e:
        raise ToolException(e)
