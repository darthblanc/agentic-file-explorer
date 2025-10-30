from langchain.tools import tool
from setup_directory import construct_file_path
import csv
from typing import List, Dict
import json

@tool(description="Read the contents of a csv file specified by a path.")
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
        return f"Error encountered while reading from file ({path}): {e}"
    return json.dumps(rv)

@tool(description="""Write new content to a csv file specified by a path. Content should be formatted similar to [{"col_a": "val_a"}, {"col_b": "val_b"}] where "col_a" and "col_b" are column names and in the column_names parameter. This tool will overwrite the previous content of the csv file.""")
def write_to_csv(path: str, data: List[Dict[str, str]], column_names: List[str]) -> str:
    working_path = construct_file_path(path)

    try:
        with open(working_path, "w") as fd:
            writer = csv.DictWriter(fd, fieldnames=column_names)
            writer.writeheader()
            writer.writerows(data)
            return f"Wrote: content to ({path})"
    except Exception as e:
        return f"Error encountered while writing to file ({path}): {e}"
    
@tool(description="""Append new content to a csv file specified by a path. Content should be formatted similar to [{"col_a": "val_a"}, {"col_b": "val_b"}] where "col_a" and "col_b" are column names and in the column_names parameter. This tool will write each row to the next available row in the csv file.""")
def append_to_csv(path: str, data: List[Dict[str, str]], column_names: List[str]) -> str:
    working_path = construct_file_path(path)

    try:
        with open(working_path, "a") as fd:
            writer = csv.DictWriter(fd, fieldnames=column_names)
            writer.writerows(data)
            return f"Wrote: content to ({path})"
    except Exception as e:
        return f"Error encountered while writing to file ({path}): {e}"


csv_tools = [
    read_csv,
    write_to_csv,
    append_to_csv
]
