from langchain.agents import create_agent
from langchain_core.tools import Tool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from txt_tools import get_txt_tools
from csv_tools import csv_tools
from directory_tools import directory_tools
from traversal_tools import traversal_tools
from configs import (
    TOOL_CONFIGS,
    SUB_AGENT_MODEL_CONFIG,
    TXT_AGENT_PROMPT,
    CSV_AGENT_PROMPT,
    DIRECTORY_AGENT_PROMPT,
    TRAVERSAL_AGENT_PROMPT,
)
from logger import audit_log, new_request_id

_sub_agent_model = ChatOllama(
    model=SUB_AGENT_MODEL_CONFIG["MODEL_NAME"],
    temperature=SUB_AGENT_MODEL_CONFIG["TEMPERATURE"],
    think=SUB_AGENT_MODEL_CONFIG["THINK"],
)


def _make_sub_agent_tool(name: str, description: str, domain_tools: list, system_prompt: str) -> Tool:
    sub_agent = create_agent(model=_sub_agent_model, tools=domain_tools)

    def run(query: str) -> str:
        req_id = new_request_id()
        audit_log("sub_agent_query", f"agent={name} query={query!r}", req_id)
        result = sub_agent.invoke({
            "messages": [SystemMessage(content=system_prompt), HumanMessage(content=query)]
        })
        response = result["messages"][-1].content
        audit_log("sub_agent_response", f"agent={name} response={response!r}", req_id)
        return response

    return Tool(name=name, description=description, func=run)


def create_hierarchical_tools(model, allow_clear_txt: bool = False) -> list:
    return [
        _make_sub_agent_tool(
            name="txt_file_agent",
            description=TOOL_CONFIGS["TXTTools"]["description"],
            domain_tools=get_txt_tools(allow_clear_txt),
            system_prompt=TXT_AGENT_PROMPT,
        ),
        _make_sub_agent_tool(
            name="csv_file_agent",
            description=TOOL_CONFIGS["CSVTools"]["description"],
            domain_tools=csv_tools,
            system_prompt=CSV_AGENT_PROMPT,
        ),
        _make_sub_agent_tool(
            name="directory_agent",
            description=TOOL_CONFIGS["DirectoryTools"]["description"],
            domain_tools=directory_tools,
            system_prompt=DIRECTORY_AGENT_PROMPT,
        ),
        _make_sub_agent_tool(
            name="traversal_agent",
            description=TOOL_CONFIGS["TraversalTools"]["description"],
            domain_tools=traversal_tools,
            system_prompt=TRAVERSAL_AGENT_PROMPT,
        ),
    ]
