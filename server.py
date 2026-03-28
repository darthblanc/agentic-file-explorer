"""
FastAPI server exposing the agent over HTTP as a Server-Sent Events stream.

Only AI response tokens cross the wire — file contents stay on the server.

Run with:
    uvicorn server:app --host 0.0.0.0 --port 8000
"""
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agent import agent_for_ui, reset_session_stm, inject_notice
from logger import audit_log, new_request_id

app = FastAPI(title="Agentic File Explorer")


class ChatRequest(BaseModel):
    message: str


class InjectRequest(BaseModel):
    notice: str


@app.post("/chat")
async def chat(request: Request, body: ChatRequest):
    """Stream agent response tokens as SSE. File contents never appear in the stream."""
    client = request.client.host if request.client else "unknown"
    req_id = new_request_id()
    audit_log("chat", f"client={client} message={body.message!r}", request_id=req_id)

    def generate():
        response_parts = []
        for token in agent_for_ui(user_prompt=body.message):
            response_parts.append(token)
            # Replace newlines so each SSE frame is a single line
            safe = token.replace("\n", "\\n")
            yield f"data: {safe}\n\n"
        audit_log("chat-response", f"client={client} response={''.join(response_parts)!r}", request_id=req_id)
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/new-chat")
async def new_chat(request: Request):
    client = request.client.host if request.client else "unknown"
    audit_log("new-chat", f"client={client}", request_id=new_request_id())
    reset_session_stm()
    return {"ok": True}


@app.post("/inject")
async def inject(request: Request, body: InjectRequest):
    client = request.client.host if request.client else "unknown"
    audit_log("inject", f"client={client} notice={body.notice!r}", request_id=new_request_id())
    inject_notice(body.notice)
    return {"ok": True}
