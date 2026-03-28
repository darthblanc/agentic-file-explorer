import chat_meta
from langchain.messages import HumanMessage

def main(agent, chat_meta: chat_meta.ChatMeta):
    while True:
        user_prompt = input(f"({chat_meta.username}): ")

        print(f"({chat_meta.model_name}): ", end="", flush=True)
        response = ""
        for token in agent.stream({"messages":  [HumanMessage(content=user_prompt)]}, stream_mode="messages"): # type: ignore
            if token[0].type == "AIMessageChunk": # type: ignore
                print(token[0].content, end="", flush=True) # type: ignore
                response += token[0].content  # type: ignore
        
        print("\n\n")
