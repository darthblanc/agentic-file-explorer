from configs import DIRECTORY_TOOL_DESCRIPTIONS
from langchain_core.tools import StructuredTool
from directory_functions import get_content, create

get_directory_content = StructuredTool.from_function(
    func=get_content,
    name="get_directory_content",
    description=DIRECTORY_TOOL_DESCRIPTIONS["get_directory_content"],
)

create_directory = StructuredTool.from_function(
    func=create,
    name="create_directory",
    description=DIRECTORY_TOOL_DESCRIPTIONS["create_directory"],
)

directory_tools = [
    get_directory_content,
    create_directory
]
