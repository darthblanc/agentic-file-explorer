import os
os.environ.setdefault("DATA_DIR", "data")

from arguments import parser


def _run_remote(args):
    """Simple CLI loop that streams tokens from the remote agent server."""
    from remote_agent import agent_for_ui, reset_session_stm
    username = args.username if hasattr(args, "username") else "user"
    print("Remote mode — connected to", os.environ.get("AGENT_SERVER_URL", "http://localhost:8000"))
    while True:
        try:
            user_prompt = input(f"({username}): ")
        except (EOFError, KeyboardInterrupt):
            break
        if user_prompt.strip().lower() in ("/new", "/reset"):
            reset_session_stm()
            print("[session reset]")
            continue
        print("(agent): ", end="", flush=True)
        for token in agent_for_ui(user_prompt):
            print(token, end="", flush=True)
        print("\n")


def _run_local(args):
    from configs import SANDBOX_DIR
    os.environ.setdefault("DATA_DIR", SANDBOX_DIR)

    from langchain_ollama import ChatOllama
    from langchain.agents import create_agent
    from hierarchical_agent_tools import create_hierarchical_tools
    from chat_meta import ChatMeta

    chat_meta = ChatMeta(
        model_name=args.model,
        keep_logs=args.verbose,
        username=args.username,
        temperature=args.temperature,
        stm=args.stm)

    model = ChatOllama(model=chat_meta.model_name, temperature=chat_meta.temperature, think=args.think)
    agent = create_agent(
        model=model,
        tools=create_hierarchical_tools(model, allow_clear_txt=args.allow_clear_txt),
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
    if os.environ.get("REMOTE_MODE"):
        _run_remote(args)
    else:
        _run_local(args)
