import unittest
from unittest.mock import patch

from core.configs import SUMMARIZATION_PROMPT
from core.stm_loader import load_summarization_agent


class TestLoadSummarizationAgent(unittest.TestCase):
    """`core.context` builds this agent at import time, so construction must stay
    network-free: ChatOllama only calls validate_model when validate_model_on_init
    is truthy, and create_agent merely compiles a graph. These assertions guard
    that guarantee against future regressions."""

    def test_builds_model_from_config_without_eager_validation(self):
        with patch("core.stm_loader.ChatOllama") as MockChatOllama, \
                patch("core.stm_loader.create_agent") as mock_create_agent:
            mock_model = MockChatOllama.return_value

            result = load_summarization_agent({"MODEL_NAME": "llama3.1", "TEMPERATURE": 0})

        MockChatOllama.assert_called_once_with(model="llama3.1", temperature=0)
        _, kwargs = MockChatOllama.call_args
        self.assertNotIn("validate_model_on_init", kwargs)

        mock_create_agent.assert_called_once_with(model=mock_model, system_prompt=SUMMARIZATION_PROMPT)
        self.assertIs(result, mock_create_agent.return_value)


if __name__ == "__main__":
    unittest.main()
