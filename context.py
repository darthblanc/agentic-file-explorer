from langchain_text_splitters import TokenTextSplitter
from typing import Dict, List, Tuple
from langchain.messages import HumanMessage, SystemMessage, AIMessage, AnyMessage
from stm_loader import load_summarization_agent
from configs import CONTEXT_SIZING, SUMMARIZATION_MODEL, BASE_SYSTEM_PROMPT, REFERENCE_INSTRUCTIONS, ASSISTANT_PROMPT
from file_dictionary import file_dict

def count_context_tokens(messages: List[Dict[str, str]]):
    text = ""
    for message_dict in messages:
        text += message_dict["content"] + "\n"
    return len(text_splitter.split_text(text))

def count_tokens(text: str):
    return len(text_splitter.split_text(text))

def trim_context(messages: List[AnyMessage], token_count: int) -> Tuple[bool, List[AnyMessage]]:
    if token_count >= MAX_CONTEXT_WINDOW:
        print("\n\n=======================INTERRUPTION START============================")
        print("Trimming context...")
        print(f"Current Context Size: {token_count}, Effective Context Size: {MAX_CONTEXT_WINDOW}")
        response = ""
        for token in agent.stream({"messages": messages[:-1] + [HumanMessage(content=ASSISTANT_PROMPT + messages[-1].content)]}, stream_mode="messages"): # type: ignore
            if token[0].type == "AIMessageChunk": # type: ignore
                response += token[0].content  # type: ignore
        
        response = "Last messages summary:\n" + response
        print(f"\n{response}\n")
        print("Trimmed context successfully.")
        print("=======================INTERRUPTION END============================\n")
        return True, [AIMessage(content=response), messages[-1]]

    return False, messages

def inject_system_prompts(messages: List[AnyMessage]) -> List[AnyMessage]:
    system_messages = [SystemMessage(content=BASE_SYSTEM_PROMPT), SystemMessage(content=REFERENCE_INSTRUCTIONS+"\n\nCurrent files in the system:\n"+str(file_dict)+"\n\n")]
    return system_messages + messages

text_splitter = TokenTextSplitter.from_tiktoken_encoder(
        chunk_size=1, chunk_overlap=0
    )
MAX_CONTEXT_WINDOW = CONTEXT_SIZING["MAX_CONTEXT_WINDOW"]
agent = load_summarization_agent(SUMMARIZATION_MODEL)
