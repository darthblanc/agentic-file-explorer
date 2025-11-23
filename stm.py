from typing import List
from pydantic import BaseModel
from langchain.messages import AnyMessage
from context import trim_context, count_tokens

class MessageContext(BaseModel):
    messages: List[AnyMessage]
    
class ShortTermMemory(BaseModel):
    message_contexts: MessageContext
    token_count: int = 0

    def add_message(self, message: AnyMessage):
        self.message_contexts.messages.append(message)
        self.token_count += count_tokens(message.content) # type: ignore
    
    def get_message_contexts(self) -> MessageContext:
        return self.message_contexts
    
    def get_comprehensive_context(self) -> List[AnyMessage]:
        messages = self.message_contexts.messages
        trimmed, messages = trim_context(messages, self.token_count)

        if trimmed:
            self.message_contexts.messages = messages
            self.token_count = count_tokens("".join([message.content for message in messages]))  # type: ignore

        return messages
