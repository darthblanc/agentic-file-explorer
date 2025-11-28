import chat_meta
from langchain.messages import AIMessage, HumanMessage
from stm import ShortTermMemory, MessageContext
from logger import logger

def main(agent, chat_meta: chat_meta.ChatMeta):
    stm = ShortTermMemory(message_contexts=MessageContext(messages=[]), token_count=0)

    while True:
        user_prompt = input(f"{chat_meta.username}: ")
        stm.add_message(HumanMessage(content=user_prompt))

        print(f"{chat_meta.model_name}: ", end="", flush=True)
        response = ""
        for token in agent.stream({"messages": stm.get_comprehensive_context()}, stream_mode="messages"): # type: ignore
            if token[0].type == "AIMessageChunk": # type: ignore
                print(token[0].content, end="", flush=True) # type: ignore
                response += token[0].content  # type: ignore
        
        print("\n\n")
        stm.add_message(AIMessage(content=response))
        logger(chat_meta.keep_logs, stm.get_message_contexts().model_dump(), filename="agentic.log")
