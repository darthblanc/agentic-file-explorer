import unittest
from unittest.mock import patch

from langchain.messages import AIMessage, AIMessageChunk, HumanMessage, SystemMessage

from core import context
from core.context import MAX_CONTEXT_WINDOW, inject_system_prompts, trim_context
from core.configs import ASSISTANT_PROMPT, BASE_SYSTEM_PROMPT, REFERENCE_INSTRUCTIONS


class FakeStreamingAgent:
    """Stand-in for the summarization agent so tests don't hit a real Ollama model."""

    def __init__(self, chunks):
        self.chunks = chunks
        self.received_messages = None

    def stream(self, payload, stream_mode="messages"):
        self.received_messages = payload["messages"]
        for chunk in self.chunks:
            yield (AIMessageChunk(content=chunk), {})


class TestTrimContext(unittest.TestCase):
    def test_returns_unchanged_when_under_limit(self):
        messages = [HumanMessage(content="hello")]

        trimmed, result = trim_context(messages, token_count=MAX_CONTEXT_WINDOW - 1)

        self.assertFalse(trimmed)
        self.assertEqual(result, messages)

    def test_collapses_history_into_summary_and_last_message_when_over_limit(self):
        messages = [
            HumanMessage(content="first message"),
            AIMessage(content="first reply"),
            HumanMessage(content="latest question"),
        ]
        fake_agent = FakeStreamingAgent(["short ", "summary"])

        with patch.object(context, "agent", fake_agent):
            trimmed, result = trim_context(messages, token_count=MAX_CONTEXT_WINDOW)

        self.assertTrue(trimmed)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], AIMessage)
        self.assertEqual(result[0].content, "Last messages summary:\nshort summary")
        self.assertIs(result[1], messages[-1])

    def test_summarization_request_prefixes_last_message_with_assistant_prompt(self):
        messages = [
            HumanMessage(content="first message"),
            HumanMessage(content="latest question"),
        ]
        fake_agent = FakeStreamingAgent(["summary"])

        with patch.object(context, "agent", fake_agent):
            trim_context(messages, token_count=MAX_CONTEXT_WINDOW)

        sent = fake_agent.received_messages
        self.assertEqual(sent[0], messages[0])
        self.assertEqual(sent[-1].content, ASSISTANT_PROMPT + "latest question")


class TestInjectSystemPrompts(unittest.TestCase):
    def test_prepends_base_and_reference_system_messages(self):
        messages = [HumanMessage(content="hi")]

        result = inject_system_prompts(messages)

        self.assertEqual(len(result), 3)
        self.assertIsInstance(result[0], SystemMessage)
        self.assertIsInstance(result[1], SystemMessage)
        self.assertEqual(result[0].content, BASE_SYSTEM_PROMPT)
        self.assertIn(REFERENCE_INSTRUCTIONS, result[1].content)
        self.assertIs(result[2], messages[0])


if __name__ == "__main__":
    unittest.main()
