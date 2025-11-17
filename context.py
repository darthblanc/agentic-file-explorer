from langchain_text_splitters import TokenTextSplitter
from typing import Dict, List

MAX_CONTEXT_WINDOW = 1000 # This might be about the effective context window for qwen3:8b
system_prompt = ""
with open("system_prompt.txt", "r") as fd:
    system_prompt = fd.read()

text_splitter = TokenTextSplitter.from_tiktoken_encoder(
    chunk_size=1, chunk_overlap=0
)

system_prompt_size = len(text_splitter.split_text(system_prompt))

def count_context_tokens(messages: List[Dict[str, str]]):
    text = ""
    for message_dict in messages:
        text += message_dict["content"] + "\n"
    return len(text_splitter.split_text(text))

def trim_context(messages: List[Dict[str, str]]):
    context_window = 0
    for i, message_dict in enumerate(messages[::-1]):
        context_window += len(text_splitter.split_text(message_dict["content"]))
        if (system_prompt_size + context_window) >= MAX_CONTEXT_WINDOW:
            return messages[-i-1:]

    return messages
