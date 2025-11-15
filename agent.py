import os
os.environ.setdefault("DATA_DIR", "data")

from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from agent_tools import tools
from logger import logger

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

    response = agent.invoke({"messages": context})
    logger(True, response, "agentic-ui.log")
    return response["messages"][-1].content
