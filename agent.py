import os
os.environ.setdefault("DATA_DIR", "data")

from chat_meta import ChatMeta
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from agent_tools import tools
from stm_context_agent import main as stm_main
from configs import UI_CONFIGS

chat_meta = ChatMeta(
        model_name=UI_CONFIGS["model"]["default"],
        keep_logs=UI_CONFIGS["verbose"]["default"],
        username=UI_CONFIGS["username"]["default"],
        temperature=UI_CONFIGS["temperature"]["default"],
        stm=UI_CONFIGS["stm"]["default"])

model = ChatOllama(model=chat_meta.model_name, temperature=chat_meta.temperature, disable_streaming=False)
agent = create_agent(
    model=model,
    tools=tools,
)

def agent_for_ui(user_prompt: str):
    for token in stm_main(agent, chat_meta, user_prompt=user_prompt):
        yield token
