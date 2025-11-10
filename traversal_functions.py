from langchain_core.tools import StructuredTool
import os
from collections import deque
from compare import compare
from setup_directory import construct_directory_path_limited
from pydantic import BaseModel, Field

class SearchArgs(BaseModel):
    source_directory: str = Field(..., description="The directory path to start searching from.")
    target: str = Field("null", description="The name of the file or directory to find. Defaults to 'null' if unspecified.")
    approximate: str = Field("No", description="If 'Yes', enables approximate/fuzzy matching. Any other value disables it.")

def breadth_first_search(source_directory: str, target: str = "null", approximate: str = "No") -> str:
    source = str(construct_directory_path_limited(source_directory))
    targeted_search = target != "null"
    approximate_search = approximate == "Yes"

    q = deque([source])
    results = []
    visited = set()

    if targeted_search:
        compare(target, source_directory, approximate_search, results)
        if not approximate_search and results:
            return f"Target: {target} was found. Path: {source}/{target}"

    while q:
        item = q.popleft()

        if item in visited:
            continue

        visited.add(item)

        if not targeted_search:
            results.append(item)

        for nbr in os.listdir(item):
            if targeted_search:
                compare(target, nbr, approximate_search, results)
                if not approximate_search and results:
                    return f"Target: {target} was found. Path: {item}/{target}"

            if "." in nbr:
                if not targeted_search:
                    results.append(f"{item}/{nbr}")
                continue
            q.append(f"{item}/{nbr}")

    approximate_search_clause = "(including approximate search results)" if approximate_search else ""
    return f"Breadth First Traversal Result {approximate_search_clause}: {results}"

def depth_first_search(source_directory: str, target: str = "null", approximate: str = "No") -> str:
    source = str(construct_directory_path_limited(source_directory))
    targeted_search = target != "null"
    approximate_search = approximate == "Yes"

    stack = [source]
    results = []
    visited = set()

    if targeted_search:
        compare(target, source_directory, approximate_search, results)
        if not approximate_search and results:
            return f"Target: {target} was found. Path: {source}/{target}"

    while stack:
        item = stack.pop()

        if item in visited:
            continue
        visited.add(item)

        if not targeted_search:
            results.append(item)

        for nbr in os.listdir(item):
            if targeted_search:
                compare(target, nbr, approximate_search, results)
                if not approximate_search and results:
                    return f"Target: {target} was found. Path: {item}/{target}"
                
            if "." in nbr:
                if not targeted_search:
                    results.append(f"{item}/{nbr}")
                continue
            stack.append(f"{item}/{nbr}")

    approximate_search_clause = "(including approximate search results)" if approximate_search else ""
    return f"Depth First Traversal Result {approximate_search_clause}: {results}"

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
