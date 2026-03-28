from langchain_core.tools import ToolException
from setup_directory import construct_file_path
from rollback import commit_async
import csv
import os
from typing import List, Dict, Optional
import json

def read(path: str, n_rows: Optional[int] = None, from_end: bool = False, columns: Optional[List[str]] = None, data_dir: str | None = None) -> str:
    """Read a CSV file with optional row slicing and column filtering.

    Args:
        path: Path to the CSV file.
        n_rows: If set, return only the first (or last) n rows of data (excluding header).
        from_end: When True and n_rows is set, return the last n rows instead of the first.
        columns: If set, return only the specified column headers.
    """
    working_path = construct_file_path(path, data_dir)
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

        if columns:
            rv = [{col: row[col] for col in columns if col in row} for row in rv]

        if n_rows is not None:
            rv = rv[-n_rows:] if from_end else rv[:n_rows]

    except Exception as e:
        return f"Error encountered while reading from file ({path}): {e}"

    return json.dumps(rv)

def get_headers(path: str, data_dir: str | None = None) -> str:
    working_path = construct_file_path(path, data_dir)
    try:
        with open(working_path, "r") as fd:
            headers = next(csv.reader(fd))
    except Exception as e:
        return f"Error encountered while reading headers from file ({path}): {e}"

    return json.dumps(headers)

def write(path: str, data: List[Dict[str, str]], column_names: List[str], data_dir: str | None = None) -> str:
    working_path = construct_file_path(path, data_dir)
    try:
        with open(working_path, "w") as fd:
            writer = csv.DictWriter(fd, fieldnames=column_names)
            writer.writeheader()
            writer.writerows(data)
            commit_async(path, "write_csv", data_dir)
            return f"Write successful on {path}"

    except Exception as e:
        return f"Error encountered while reading from file ({path}): {e}"

def append(path: str, data: List[Dict[str, str]], column_names: List[str], data_dir: str | None = None) -> str:
    working_path = construct_file_path(path, data_dir)
    try:
        with open(working_path, "a") as fd:
            writer = csv.DictWriter(fd, fieldnames=column_names)
            writer.writerows(data)
            commit_async(path, "append_csv", data_dir)
            return f"Write successful on {path}"

    except Exception as e:
        return f"Error encountered while reading from file ({path}): {e}"
