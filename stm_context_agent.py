import chat_meta
from langchain.messages import AIMessage, HumanMessage, SystemMessage
from stm import ShortTermMemory, MessageContext
from stm_loader import load_system_prompt, load_stm_config
from context import count_tokens

def main(agent, chat_meta: chat_meta.ChatMeta):
    configs = load_stm_config()
    SYSTEM_PROMPT = load_system_prompt(configs["SYSTEM_PROMPT_FILE"])
    stm = ShortTermMemory(message_contexts=MessageContext(messages=[SystemMessage(content=SYSTEM_PROMPT)]), token_count=count_tokens(SYSTEM_PROMPT))

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
