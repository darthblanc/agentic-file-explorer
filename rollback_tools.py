from langchain.tools import Tool
from rollback import rollback_last_change, rollback_all_changes, list_changes

rollback_tools = [
    Tool(
        name="rollback_last_change",
        description="Undo the most recent file change in the data directory. Use when the last write/append produced incorrect results.",
        func=lambda _: rollback_last_change(),
    ),
    Tool(
        name="rollback_all_changes",
        description="Undo ALL file changes made this session, restoring the data directory to its state at session start.",
        func=lambda _: rollback_all_changes(),
    ),
    Tool(
        name="list_file_changes",
        description="Show a log of all file changes made in the data directory this session.",
        func=lambda _: list_changes(),
    ),
]
