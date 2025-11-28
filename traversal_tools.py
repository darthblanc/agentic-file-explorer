from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from configs import SEARCH_ARGS, FUNCTION_DESCRIPTION
from traversal_functions import breadth_first_search, depth_first_search

class SearchArgs(BaseModel):
    source_directory: str = Field(..., description=SEARCH_ARGS["source_directory"])
    target: str = Field("", description=SEARCH_ARGS["target_name"])
    approximate: bool = Field(False, description=SEARCH_ARGS["approximate"])

bfs_tool = StructuredTool.from_function(
    func=breadth_first_search,
    args_schema=SearchArgs,
    description=FUNCTION_DESCRIPTION["breadth_first_search"]
)

dfs_tool = StructuredTool.from_function(
    func=depth_first_search,
    args_schema=SearchArgs,
    description=FUNCTION_DESCRIPTION["depth_first_search"]
)
traversal_tools = [
    bfs_tool,
    dfs_tool
]
