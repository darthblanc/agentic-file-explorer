from pydantic import BaseModel

class ChatMeta(BaseModel):
    model_name: str
    keep_logs: bool
    username: str
    temperature: float
    stm: bool
