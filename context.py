from langchain_text_splitters import TokenTextSplitter
from typing import Dict, List, Tuple
from langchain.messages import HumanMessage, SystemMessage, AnyMessage
from stm_loader import load_stm_config, load_summarization_agent

def count_context_tokens(messages: List[Dict[str, str]]):
    text = ""
    for message_dict in messages:
        text += message_dict["content"] + "\n"
    return len(text_splitter.split_text(text))

def count_tokens(text: str):
    return len(text_splitter.split_text(text))

def trim_context(messages: List[AnyMessage], token_count: int) -> Tuple[bool, List[AnyMessage]]:
    if token_count >= MAX_CONTEXT_WINDOW:
        print("\n=======================INTERRUPTION START============================")
        print("Trimming context...")
        print(f"Current Context Size: {token_count}, Effective Context Size: {MAX_CONTEXT_WINDOW}")
        response = ""
        for token in agent.stream({"messages": messages + [HumanMessage(content="Summarise the following conversation focus on retaining information on goals, plans, knowledge.")]}, stream_mode="messages"): # type: ignore
            if token[0].type == "AIMessageChunk": # type: ignore
                response += token[0].content  # type: ignore
        print(f"SUMMARY:\n{response}.\n")
        print("Trimmed context.")
        print("=======================INTERRUPTION END============================")
        return True, [SystemMessage(content=response)]

    return False, messages


text_splitter = TokenTextSplitter.from_tiktoken_encoder(
        chunk_size=1, chunk_overlap=0
    )
json_config = load_stm_config()
MAX_CONTEXT_WINDOW = json_config["CONTEXT_SIZING"]["MAX_CONTEXT_WINDOW"]
agent = load_summarization_agent(json_config["SUMMARIZATION_MODEL"])