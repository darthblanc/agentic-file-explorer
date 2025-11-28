from configs import CSV_TOOL_DESCRIPTIONS
from langchain_core.tools import StructuredTool
from csv_functions import read, write, append

read_csv = StructuredTool.from_function(
    func=read,
    name="read_csv",
    description=CSV_TOOL_DESCRIPTIONS["read"],
)

write_to_csv = StructuredTool.from_function(
    func=write,
    name="write_to_csv",
    description=CSV_TOOL_DESCRIPTIONS["write"],
)

append_to_csv = StructuredTool.from_function(
    func=append,
    name="append_to_csv",
    description=CSV_TOOL_DESCRIPTIONS["append"],
)

csv_tools = [
    read_csv,
    write_to_csv,
    append_to_csv
]
