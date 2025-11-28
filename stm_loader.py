import json
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from configs import SUMMARIZATION_PROMPT

def load_summarization_agent(summarization_model_details: dict):
    model = ChatOllama(model=summarization_model_details["MODEL_NAME"], temperature=summarization_model_details["TEMPERATURE"])
    agent = create_agent(model=model, system_prompt=SUMMARIZATION_PROMPT)
    return agent
