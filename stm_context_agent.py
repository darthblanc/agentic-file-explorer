import chat_meta
from langchain.messages import AIMessage, HumanMessage
from stm import ShortTermMemory, MessageContext
from logger import log_conversation

def main(agent, chat_meta: chat_meta.ChatMeta):
    stm = ShortTermMemory(message_contexts=MessageContext(messages=[]), token_count=0)
    while True:
        user_prompt = input(f"({chat_meta.username}): ")
        stm.add_message(HumanMessage(content=user_prompt))

        print(f"({chat_meta.model_name}): ", end="", flush=True)
        response = ""
        for token in agent.stream({"messages": stm.get_comprehensive_context()}, stream_mode="messages"): # type: ignore
            if token[0].type == "AIMessageChunk": # type: ignore
                print(token[0].content, end="", flush=True) # type: ignore
                response += token[0].content  # type: ignore

        print("\n\n")
        stm.add_message(AIMessage(content=response))
        log_conversation(chat_meta.keep_logs, stm.get_message_contexts().model_dump(), filename="agentic-sum.log")

def stream(agent, chat_meta: chat_meta.ChatMeta, user_prompt: str, stm: ShortTermMemory | None = None):
    if stm is None:
        stm = ShortTermMemory(message_contexts=MessageContext(messages=[]), token_count=0)
    stm.add_message(HumanMessage(content=user_prompt))

    response = ""
    for token in agent.stream({"messages": stm.get_comprehensive_context()}, stream_mode="messages"): # type: ignore
        if token[0].type == "AIMessageChunk": # type: ignore
            response += token[0].content  # type: ignore
            yield token[0].content  # type: ignore

    stm.add_message(AIMessage(content=response))
    log_conversation(chat_meta.keep_logs, stm.get_message_contexts().model_dump(), filename="agentic-ui.log")
