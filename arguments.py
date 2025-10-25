import argparse

parser = argparse.ArgumentParser(description="Agentic File Explorer")

parser.add_argument(
    "--model",
    type=str,
    default="qwen3:8b",
    choices=["qwen3:8b", "llama3.1", "phi3.5"],
    help="The LLM model that would be used for the task"
)

parser.add_argument(
    "--verbose",
    action="store_true",
    default=False,
    help="Enable verbose logging into agentic-fe.log"
)

parser.add_argument(
    "--username",
    type=str,
    default="User",
    help="The name of the user."
)

parser.add_argument(
    "--temperature",
    type=int,
    default=0,
    help="The temperature of the model."
)
