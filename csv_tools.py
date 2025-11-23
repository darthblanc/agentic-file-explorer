from langchain.tools import tool, ToolException
from setup_directory import construct_file_path
import csv
from typing import List, Dict
import json

configs = json.load(open("configs/tool_config.json"))
CSV_TOOL_DESCRIPTIONS = configs["CSVTools"]["functions"]

@tool(description=CSV_TOOL_DESCRIPTIONS["read_csv"])
def read_csv(path: str) -> str:
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
        raise ToolException(e)
    return json.dumps(rv)

@tool(description=CSV_TOOL_DESCRIPTIONS["write_to_csv"])
def write_to_csv(path: str, data: List[Dict[str, str]], column_names: List[str]) -> str:
    working_path = construct_file_path(path)

    try:
        with open(working_path, "w") as fd:
            writer = csv.DictWriter(fd, fieldnames=column_names)
            writer.writeheader()
            writer.writerows(data)
            return f"Wrote: content to ({path})"
    except Exception as e:
        raise ToolException(e)
    
@tool(description=CSV_TOOL_DESCRIPTIONS["append_to_csv"])
def append_to_csv(path: str, data: List[Dict[str, str]], column_names: List[str]) -> str:
    working_path = construct_file_path(path)

    try:
        with open(working_path, "a") as fd:
            writer = csv.DictWriter(fd, fieldnames=column_names)
            writer.writerows(data)
            return f"Wrote: content to ({path})"
    except Exception as e:
        raise ToolException(e)


csv_tools = [
    read_csv,
    write_to_csv,
    append_to_csv
]
