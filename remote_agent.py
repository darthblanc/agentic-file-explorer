"""
Thin HTTP client that mirrors the agent.py interface consumed by ui.py and main.py.

Set AGENT_SERVER_URL to point at the running server (default: http://localhost:8000).
"""
import os
import httpx

SERVER_URL = os.environ.get("AGENT_SERVER_URL", "http://localhost:8000")


def agent_for_ui(user_prompt: str):
    """Yield response tokens streamed from the remote agent via SSE."""
    with httpx.stream(
        "POST",
        f"{SERVER_URL}/chat",
        json={"message": user_prompt},
        timeout=None,
    ) as response:
        for line in response.iter_lines():
            if line.startswith("data: "):
                token = line[6:]
                if token == "[DONE]":
                    return
                # Restore newlines that were escaped for SSE framing
                yield token.replace("\\n", "\n")


def reset_session_stm():
    httpx.post(f"{SERVER_URL}/new-chat")


def inject_notice(notice: str):
    httpx.post(f"{SERVER_URL}/inject", json={"notice": notice})
