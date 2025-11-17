import os
os.environ.setdefault("DATA_DIR", "data")

from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from agent_tools import tools
from logger import logger, ctx_logger
from context import trim_context

system_prompt = ""

with open("system_prompt.txt", "r") as fd:
    system_prompt = fd.read()

def my_agent(human_message: str, context=[]):

    model = ChatOllama(model="qwen3:8b", temperature=0)
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=system_prompt
    )
    trimmed_context = trim_context(context)
    response = agent.invoke({"messages": trimmed_context}) # type: ignore
    # logger(True, response, "agentic-ui.log")

    response_content = response["messages"][-1].content
    ctx_logger(True, trimmed_context + [{"role": "assistant", "content": response_content}])

    new_context = {"messages": context + [{"role": "assistant", "content": response_content}]}
    return response_content, new_context
