import os
os.environ.setdefault("DATA_DIR", "data")

from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from agent_tools import tools
from arguments import parser
from logger import logger

def main(args):
    model_name = args.model
    keep_logs = args.verbose
    username = args.username
    temperature = args.temperature

    model = ChatOllama(model=model_name, temperature=temperature)
    agent = create_agent(
        model=model,
        tools=tools
    )

    human_message: str = input(f"{username}: ")

    while human_message:
        response = agent.invoke({"messages":[{"role": "user", "content": human_message}]})
        print("Agent:", response["messages"][-1].content)
        logger(keep_logs=keep_logs, response=response)
        human_message: str = input(f"{username}: ")

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
