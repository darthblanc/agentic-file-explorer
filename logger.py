import logging
from typing import Any, List, Dict

def logger(keep_logs: bool, response: Dict[str, Any] | Any, filename = "agentic-fe.log"):
    if keep_logs:
        logging.basicConfig(level=logging.INFO, filename=filename, format='%(asctime)s - %(levelname)s - %(message)s')
        tool_call_summary = "\n".join([f"{m["type"]} -> {m["content"]}" for m in response["messages"]])
        logging.info(f"\n{tool_call_summary}")
        logging.info("="*30)

def ctx_logger(keep_logs: bool, context: List[Dict[str, str]] | Any, filename = "agentic-ctx.log"):
    if keep_logs:
        logging.basicConfig(level=logging.INFO, filename=filename, format='%(asctime)s - %(levelname)s - %(message)s')
        context = "\n".join([ctx["content"] for ctx in context])
        logging.info(f"\n{context}")
        logging.info("="*30)
