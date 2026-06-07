import logging
import os
import uuid
from typing import Any, Dict


def _get_file_logger(filename: str) -> logging.Logger:
    log = logging.getLogger(filename)
    if not log.handlers:
        os.makedirs("logs", exist_ok=True)
        handler = logging.FileHandler(f"logs/{filename}")
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s\n%(message)s"))
        log.addHandler(handler)
        log.setLevel(logging.INFO)
    return log


def _get_audit_logger() -> logging.Logger:
    log = logging.getLogger("audit")
    if not log.handlers:
        os.makedirs("logs", exist_ok=True)
        handler = logging.FileHandler("logs/audit.log")
        handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
        log.addHandler(handler)
        log.setLevel(logging.INFO)
    return log


def new_request_id() -> str:
    return uuid.uuid4().hex[:8]


def log_conversation(enabled: bool, messages: Dict[str, Any], filename: str) -> None:
    if not enabled:
        return
    summary = "\n".join(f"{m['type']}: {m['content']}" for m in messages["messages"])
    _get_file_logger(filename).info(f"\n{summary}\n{'=' * 30}")


def audit_log(action: str, detail: str = "", request_id: str = "") -> None:
    """Write a single-line structured audit entry to logs/audit.log."""
    parts = [f"action={action}"]
    if request_id:
        parts.append(f"req={request_id}")
    if detail:
        parts.append(detail)
    _get_audit_logger().info(" | ".join(parts))
