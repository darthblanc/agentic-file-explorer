import logging
from typing import Any

def logger(keep_logs: bool, response: dict[str, Any] | Any, filename = "agentic-fe.log"):
    if keep_logs:
        logging.basicConfig(level=logging.INFO, filename=filename, format='%(asctime)s - %(levelname)s - %(message)s')
        tool_call_summary = "\n".join([f"\t\t{m.type} -> {m.content}" for m in response["messages"]])
        logging.info(f"\n\t\tSummary of conversation:\n{tool_call_summary}")
