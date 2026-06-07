import unittest
from unittest.mock import patch

from langchain.messages import AIMessage, HumanMessage, SystemMessage

from core import stm
from core.context import count_tokens
from core.stm import MessageContext, ShortTermMemory


def make_stm(messages=None, token_count=0):
    return ShortTermMemory(message_contexts=MessageContext(messages=messages or []), token_count=token_count)


class TestAddMessage(unittest.TestCase):
    def test_appends_message_and_accumulates_token_count(self):
        memory = make_stm()
        message = HumanMessage(content="hello there")

        memory.add_message(message)

        self.assertEqual(memory.get_message_contexts().messages, [message])
        self.assertEqual(memory.token_count, count_tokens("hello there"))

    def test_token_count_accumulates_across_messages(self):
        memory = make_stm()

        memory.add_message(HumanMessage(content="hello there"))
        memory.add_message(AIMessage(content="general kenobi"))

        expected = count_tokens("hello there") + count_tokens("general kenobi")
        self.assertEqual(memory.token_count, expected)


class TestGetComprehensiveContext(unittest.TestCase):
    def test_injects_system_prompts_and_leaves_history_untouched_when_not_trimmed(self):
        message = HumanMessage(content="hi")
        memory = make_stm([message], token_count=5)

        with patch.object(stm, "trim_context", return_value=(False, memory.message_contexts.messages)) as mock_trim:
            result = memory.get_comprehensive_context()

        mock_trim.assert_called_once_with([message], 5)
        # history and token count are untouched when no trimming occurred
        self.assertEqual(memory.message_contexts.messages, [message])
        self.assertEqual(memory.token_count, 5)
        # system prompts are prepended ahead of the conversation
        self.assertIsInstance(result[0], SystemMessage)
        self.assertIsInstance(result[1], SystemMessage)
        self.assertIs(result[2], message)

    def test_replaces_history_and_recounts_tokens_when_trimmed(self):
        original = [HumanMessage(content="long ago"), HumanMessage(content="latest")]
        memory = make_stm(original, token_count=999)
        trimmed_messages = [
            AIMessage(content="Last messages summary:\nrecap"),
            HumanMessage(content="latest"),
        ]

        with patch.object(stm, "trim_context", return_value=(True, trimmed_messages)):
            result = memory.get_comprehensive_context()

        self.assertEqual(memory.message_contexts.messages, trimmed_messages)
        expected_count = sum(count_tokens(message.content) for message in trimmed_messages)
        self.assertEqual(memory.token_count, expected_count)
        # the (possibly trimmed) conversation still gets system prompts prepended
        self.assertEqual(result[2:], trimmed_messages)

    def test_archives_summarized_messages_without_sending_them_to_the_agent(self):
        original = [
            HumanMessage(content="long ago"),
            AIMessage(content="ancient reply"),
            HumanMessage(content="latest"),
        ]
        memory = make_stm(original, token_count=999)
        summary = AIMessage(content="Last messages summary:\nrecap")
        trimmed_messages = [summary, original[-1]]

        with patch.object(stm, "trim_context", return_value=(True, trimmed_messages)):
            result = memory.get_comprehensive_context()

        # the messages that got summarized away are archived under the summary text...
        self.assertEqual(memory.summary_archive[summary.content], original[:-1])
        # ...but the agent only ever sees the summary + preserved last message, never the archive
        self.assertEqual(result[2:], trimmed_messages)
        self.assertEqual(len(result), 4)


if __name__ == "__main__":
    unittest.main()
