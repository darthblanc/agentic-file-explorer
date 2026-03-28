from configs import SANDBOX_DIR
import os
os.environ.setdefault("DATA_DIR", SANDBOX_DIR)

from chat_meta import ChatMeta
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from hierarchical_agent_tools import create_hierarchical_tools
from stm_context_agent import stream as stm_stream
from stm import ShortTermMemory, MessageContext
from langchain_core.messages import HumanMessage
from configs import UI_CONFIGS

chat_meta = ChatMeta(
        model_name=UI_CONFIGS["model"]["default"],
        keep_logs=UI_CONFIGS["verbose"]["default"],
        username=UI_CONFIGS["username"]["default"],
        temperature=UI_CONFIGS["temperature"]["default"],
        stm=UI_CONFIGS["stm"]["default"])

model = ChatOllama(model=chat_meta.model_name, temperature=chat_meta.temperature, think=UI_CONFIGS["think"]["default"], disable_streaming=False)
agent = create_agent(
    model=model,
    tools=create_hierarchical_tools(model, allow_clear_txt=UI_CONFIGS["allow_clear_txt"]["default"]),
)

session_stm = ShortTermMemory(message_contexts=MessageContext(messages=[]), token_count=0)

def agent_for_ui(user_prompt: str):
    for token in stm_stream(agent, chat_meta, user_prompt=user_prompt, stm=session_stm):
        yield token

def reset_session_stm():
    global session_stm
    session_stm = ShortTermMemory(message_contexts=MessageContext(messages=[]), token_count=0)

def inject_notice(content: str):
    session_stm.add_message(HumanMessage(content=content))
