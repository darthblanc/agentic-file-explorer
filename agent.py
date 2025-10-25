import os
os.environ.setdefault("DATA_DIR", "data")

from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from basic_file_functions import tools

def my_agent(human_message: str, context=[]):

    model = ChatOllama(model="qwen3:8b", temperature=0)
    agent = create_agent(
        model=model,
        tools=tools
    )

    response = agent.invoke({"messages": context})
    return response["messages"][-1].content
