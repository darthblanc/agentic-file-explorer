from langchain.tools import ToolException
from setup_directory import construct_file_path
import csv
from typing import List, Dict
import json

def read(path: str) -> str:
    working_path = construct_file_path(path)
    try:
        rv = []
        headers = []
        with open(working_path, "r") as fd:
            rows = csv.reader(fd)
            for i, row in enumerate(rows):
                if i == 0:
                    headers = row
                else:
                    sub_dict = {}
                    for j, item in enumerate(row):
                        sub_dict[headers[j]] = item
                    rv.append(sub_dict)

    except Exception as e:
        return f"Error encountered while reading from file ({path}): {e}"

    return json.dumps(rv)

def write(path: str, data: List[Dict[str, str]], column_names: List[str]) -> str:
    working_path = construct_file_path(path)
    try:
        with open(working_path, "w") as fd:
            writer = csv.DictWriter(fd, fieldnames=column_names)
            writer.writeheader()
            writer.writerows(data)
            return f"Wrote: content to ({path})"

    except Exception as e:
        # raise ToolException(e)
        return f"Error encountered while reading from file ({path}): {e}"
    
def append(path: str, data: List[Dict[str, str]], column_names: List[str]) -> str:
    working_path = construct_file_path(path)
    try:
        with open(working_path, "a") as fd:
            writer = csv.DictWriter(fd, fieldnames=column_names)
            writer.writerows(data)
            return f"Wrote: content to ({path})"

    except Exception as e:
        # raise ToolException(e)
        return f"Error encountered while reading from file ({path}): {e}"
