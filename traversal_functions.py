from langchain.tools import tool
import os
from collections import deque
from compare import compare
from setup_directory import construct_directory_path_limited

@tool(description="Perform a Breadth First Search (BFS) traversal on a source directory. Set target as 'null' for a targeted search By default set as 'null'. Set approximate as 'Yes' for an approximate search. By default set as 'No'")
def breadth_first_search(source_directory: str, target: str, approximate: str) -> str:
    source = str(construct_directory_path_limited(source_directory))
    targeted_search = target != "null"
    approximate_search = approximate == "Yes"

    q = deque([source])
    results = []
    visited = set()

    if targeted_search:
        compare(target, source_directory, approximate_search, results)
        if not approximate_search and results:
            return f"Target: {target} was found"

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
                    return f"Target: {target} was found"

            if "." in nbr:
                if not targeted_search:
                    results.append(nbr)
                continue
            q.append(f"{item}/{nbr}")

    approximate_search_clause = "(including approximate search results)" if approximate_search else ""
    return f"Breadth First Traversal Result {approximate_search_clause}: {results}"

@tool(description="Perform a Depth First Search (DFS) traversal on a source directory. Set target as 'null' for a targeted search By default set as 'null'. Set approximate as 'Yes' for an approximate search. By default set as 'No'")
def depth_first_search(source_directory: str, target: str, approximate: str) -> str:
    source = str(construct_directory_path_limited(source_directory))
    targeted_search = target != "null"
    approximate_search = approximate == "Yes"

    stack = [source]
    results = []
    visited = set()

    if targeted_search:
        compare(target, source_directory, approximate_search, results)
        if not approximate_search and results:
            return f"Target: {target} was found"

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
                    return f"Target: {target} was found"
                
            if "." in nbr:
                if not targeted_search:
                    results.append(nbr)
                continue
            stack.append(f"{item}/{nbr}")

    approximate_search_clause = "(including approximate search results)" if approximate_search else ""
    return f"Depth First Traversal Result {approximate_search_clause}: {results}"

traversal_tools = [
    breadth_first_search,
    depth_first_search
]
