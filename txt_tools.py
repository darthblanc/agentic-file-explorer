from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from configs import TXT_TOOL_DESCRIPTIONS, TXT_TOOL_READ_ARGS, TXT_TOOL_WRITE_ARGS
from txt_functions import read, write, append, clear

class ReadArgs(BaseModel):
    path: str = Field(..., description=TXT_TOOL_READ_ARGS["path"])

class WriteArgs(BaseModel):
    path: str = Field(..., description=TXT_TOOL_WRITE_ARGS["path"])
    content: str = Field(..., description=TXT_TOOL_WRITE_ARGS["content"])

read_txt = StructuredTool.from_function(
    func=read,
    name="read_txt",
    description=TXT_TOOL_DESCRIPTIONS["read"],
)

write_to_txt = StructuredTool.from_function(
    func=write,
    name="write_to_txt",
    description=TXT_TOOL_DESCRIPTIONS["write"],
)

append_to_txt = StructuredTool.from_function(
    func=append,
    name="append_to_txt",
    description=TXT_TOOL_DESCRIPTIONS["append"],
)

clear_txt = StructuredTool.from_function(
    func=clear,
    name="clear_txt",
    description=TXT_TOOL_DESCRIPTIONS["clear"],
)

txt_tools = [
    read_txt,
    write_to_txt,
    append_to_txt,
    # clear_txt,
]
