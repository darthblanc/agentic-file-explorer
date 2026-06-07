from typing import Dict, List
from pydantic import BaseModel
from langchain.messages import AnyMessage
from core.context import trim_context, count_tokens, inject_system_prompts

class MessageContext(BaseModel):
    messages: List[AnyMessage]
    
class ShortTermMemory(BaseModel):
    message_contexts: MessageContext
    token_count: int = 0
    summary_archive: Dict[str, List[AnyMessage]] = {}

    def add_message(self, message: AnyMessage):
        self.message_contexts.messages.append(message)
        self.token_count += count_tokens(message.content) # type: ignore

    def get_message_contexts(self) -> MessageContext:
        return self.message_contexts

    def get_comprehensive_context(self) -> List[AnyMessage]:
        original_messages = self.message_contexts.messages
        trimmed, messages = trim_context(original_messages, self.token_count)

        if trimmed:
            # trim_context always preserves the last message verbatim and folds
            # everything before it into messages[0] (the summary)
            self.summary_archive[messages[0].content] = original_messages[:-1]  # type: ignore
            self.message_contexts.messages = messages
            self.token_count = sum(count_tokens(message.content) for message in messages)  # type: ignore

        messages = inject_system_prompts(messages)
        return messages
