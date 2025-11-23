from langchain.tools import tool, ToolException
from setup_directory import construct_file_path
from typing import List
import json

configs = json.load(open("configs/tool_config.json"))
TXT_TOOL_DESCRIPTIONS = configs["TXTTools"]["functions"]

@tool(description=TXT_TOOL_DESCRIPTIONS["read_txt"])
def read_txt(path: str) -> str:
    working_path = construct_file_path(path)

    try:
        with open(working_path, "r") as fd:
            return fd.read()
    except Exception as e:
        raise ToolException(e)
    
@tool(description=TXT_TOOL_DESCRIPTIONS["read_txt_lines"])
def read_txt_lines(path: str) -> List[str]:
    working_path = construct_file_path(path)

    try:
        with open(working_path, "r") as fd:
            return fd.readlines()
    except Exception as e:
        raise ToolException(e)

@tool(description=TXT_TOOL_DESCRIPTIONS["write_to_txt"])
def write_to_txt(path: str, content: str) -> str:
    working_path = construct_file_path(path)

    try:
        with open(working_path, "w") as fd:
            fd.write(content)
            return f"Wrote {content[:15]}... to ({path})"
    except Exception as e:
        raise ToolException(e)

@tool(description=TXT_TOOL_DESCRIPTIONS["append_to_txt"])
def append_to_txt(path: str, content: str) -> str:
    working_path = construct_file_path(path)

    try:
        with open(working_path, "a") as fd:
            fd.write(f"\n{content}")
            return f"Wrote: {content[:15]}... to ({path})"
    except Exception as e:
        raise ToolException(e)

@tool(description=TXT_TOOL_DESCRIPTIONS["clear"])
def clear(path: str) -> str:
    working_path = construct_file_path(path)

    try:
        with open(working_path, "w") as fd:
            fd.write("")
            return f"Cleared content from ({path})"
    except Exception as e:
        raise ToolException(e)

txt_tools = [
    read_txt,
    read_txt_lines,
    write_to_txt,
    append_to_txt,
    # clear,
]
