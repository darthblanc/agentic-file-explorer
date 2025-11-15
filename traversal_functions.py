from langchain_core.tools import StructuredTool
import os
from collections import deque
from compare import compare
from setup_directory import construct_directory_path_limited
from pydantic import BaseModel, Field
from typing import List, Set, Deque, Dict
from string_functions import strip_base_directory

class SearchArgs(BaseModel):
    source_directory: str = Field(..., description="The directory path to start searching from.")
    target: str = Field("null", description="The name of the file or directory to find. Defaults to 'null' if unspecified.")
    approximate: str = Field("No", description="If 'Yes', enables approximate/fuzzy matching. Any other value disables it.")

class SearchObject:
    def __init__(self, processor_array: List[str] | Deque[str], results: Dict[str, List[str]], visited: Set[str], directory: str, target: str, targeted_search: bool, approximate_search: bool) -> None:
        self.processor_array: List[str] | Deque[str] = processor_array
        self.results: Dict[str, List[str]] = results
        self.visited: Set[str] = visited
        self.directory: str = directory
        self.target: str = target
        self.targeted_search: bool = targeted_search
        self.approximate_search: bool = approximate_search

def inner_search(search_object: SearchObject) -> bool:
    processor_array = search_object.processor_array
    results = search_object.results
    visited = search_object.visited
    directory = search_object.directory
    target = search_object.target
    targeted_search = search_object.targeted_search
    approximate_search = search_object.approximate_search

    if directory in visited:
        return False
    visited.add(directory)

    if not targeted_search:
        results["match"].append(strip_base_directory(directory))
    
    for nbr in os.listdir(directory):
        if targeted_search:
            compare(directory, target, nbr, approximate_search, results)
            if not approximate_search and results:
                return True

        if "." in nbr:
            if not targeted_search:
                results["match"].append(strip_base_directory(f"{directory}/{nbr}"))
            continue
        processor_array.append(f"{directory}/{nbr}")

    return False


def breadth_first_search(source_directory: str, target: str = "null", approximate: str = "No") -> Dict[str, List[str]]:
    source = str(construct_directory_path_limited(source_directory))
    targeted_search = target != "null"
    approximate_search = approximate == "Yes"

    results = {"match": []}
    if approximate_search:
        results["fuzzy"] = []

    if targeted_search:
        compare(source_directory, target, source_directory, approximate_search, results)
        if not approximate_search and []:
            return {"match": [strip_base_directory(f"{source}/{target}")]}
    
    search_object = SearchObject(deque([source]), results, set(), source, target, targeted_search, approximate_search)

    while search_object.processor_array:
        directory = search_object.processor_array.popleft() # type: ignore
        search_object.directory = directory
        found = inner_search(search_object)
        if found:
            return search_object.results

    return search_object.results

def depth_first_search(source_directory: str, target: str = "null", approximate: str = "No") -> Dict[str, List[str]]:
    source = str(construct_directory_path_limited(source_directory))
    targeted_search = target != "null"
    approximate_search = approximate == "Yes"

    results = {"match": []}
    if approximate_search:
        results["fuzzy"] = []

    if targeted_search:
        compare(source_directory, target, source_directory, approximate_search, results)
        if not approximate_search and []:
            return {"match": [strip_base_directory(f"{source}/{target}")]}
    
    search_object = SearchObject([source], results, set(), source, target, targeted_search, approximate_search)

    while search_object.processor_array:
        directory = search_object.processor_array.pop() # type: ignore
        search_object.directory = directory
        found = inner_search(search_object)
        if found:
            return search_object.results

    return search_object.results

bfs_tool = StructuredTool.from_function(
    func=breadth_first_search,
    args_schema=SearchArgs,
    description="Performs a breadth-first search (BFS) through the filesystem. The path(s) to matching file(s) or directories, or an informative message if not found."
)

dfs_tool = StructuredTool.from_function(
    func=depth_first_search,
    args_schema=SearchArgs,
    description="Performs a depth-first search (DFS) through the filesystem. The path(s) to matching file(s) or directories, or an informative message if not found."
)
traversal_tools = [
    bfs_tool,
    dfs_tool
]
