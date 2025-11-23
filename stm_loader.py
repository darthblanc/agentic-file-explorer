import json
from langchain_ollama import ChatOllama
from langchain.agents import create_agent

def load_system_prompt(path: str) -> str:
    system_prompt = ""
    with open(path, "r") as fd:
        system_prompt = fd.read()
    return system_prompt

def load_stm_config():
    json_config = {}
    with open("configs/stm_config.json", "r") as fd:
        json_config = json.load(fd)
    return json_config

def load_summarization_agent(summarization_model_details: dict):
    model = ChatOllama(model=summarization_model_details["MODEL_NAME"], temperature=summarization_model_details["TEMPERATURE"])
    agent = create_agent(model=model, system_prompt=load_system_prompt(summarization_model_details["SYSTEM_PROMPT_FILE"]))

    return agent
