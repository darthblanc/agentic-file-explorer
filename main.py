import os
os.environ.setdefault("DATA_DIR", "data")

from arguments import parser
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from agent_tools import tools
from arguments import parser
from chat_meta import ChatMeta

def main(args):
    chat_meta = ChatMeta(
        model_name=args.model,
        keep_logs=args.verbose,
        username=args.username,
        temperature=args.temperature,
        stm=args.stm)

    model = ChatOllama(model=chat_meta.model_name, temperature=chat_meta.temperature)
    agent = create_agent(
        model=model,
        tools=tools,
    )

    if chat_meta.stm:
        from stm_context_agent import main as stm_main
        print("Using short-term memory context agent.")
        stm_main(agent, chat_meta)
    else:
        from no_context_agent import main as no_stm_main
        print("Using no short-term memory context agent.")
        no_stm_main(agent, chat_meta)

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
