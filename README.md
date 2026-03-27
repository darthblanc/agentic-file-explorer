# Agentic File Explorer

A file explorer powered by AI agents that can read, write, search, and manage files through natural language commands. Built with LangChain and Gradio, it runs locally using Ollama.

## Overview

This project implements an intelligent file management system using a [ReAct agent](https://docs.langchain.com/oss/python/langchain/agents#example-of-react-loop) that can understand and execute file operations through conversation. All operations are sandboxed to a local `data/` directory for safety.

**Key Features:**

- Natural language file operations (read, write, append, search)
- Smart file search with BFS/DFS strategies and fuzzy matching
- Short-term memory (STM) with automatic context summarization
- In-session file dictionary for fast re-access without re-reading disk
- Interactive web UI built with Gradio
- Runs entirely locally with Ollama (no external API calls)

## Prerequisites

Install [Ollama](https://ollama.com/download/linux) to run LLMs locally.

## Quick Start

1. **Pull the recommended model:**

   ```bash
   ollama pull qwen3:8b
   ```

2. **Install UV package manager:**

   ```bash
   # Using curl
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Or using wget
   wget -qO- https://astral.sh/uv/install.sh | sh
   ```

3. **Set up the environment:**

   ```bash
   uv sync
   ```

4. **Run the agent:**

   ```bash
   uv run main.py
   ```

5. **Launch the UI (optional):**
   ```bash
   uv run ui.py
   ```

## Available Tools

| Tool                 | Description                                    | Supported Formats   |
| -------------------- | ---------------------------------------------- | ------------------- |
| **Read**             | Read file contents                             | `.txt`, `.csv`      |
| **Write**            | Write or overwrite file contents               | `.txt`, `.csv`      |
| **Append**           | Append content to a new line                   | `.txt`, `.csv`      |
| **Clear**            | Clear file contents (disabled by default)      | `.txt`, `.csv`      |
| **List Directory**   | Display files and subdirectories               | All                 |
| **Create Directory** | Create new directories                         | N/A                 |
| **BFS Search**       | Breadth-first file system search               | Files & directories |
| **DFS Search**       | Depth-first file system search                 | Files & directories |

Search tools support both exact matching and approximate (fuzzy) matching using a 0.8 similarity threshold via `SequenceMatcher`.

## Configuration

### Command-Line Flags

| Flag            | Default    | Description                          |
| --------------- | ---------- | ------------------------------------ |
| `--model`       | `qwen3:8b` | LLM model to use                     |
| `--verbose`     | `false`    | Enable logging to `logs/agentic-fe.log` |
| `--username`    | `user`     | Display name for the user            |
| `--temperature` | `0`        | Model temperature (0-1)              |
| `--stm`         | `true`     | Enable short-term memory             |

> **Note:** The `--verbose` flag requires an explicit value: `--verbose true`.

### Usage Examples

```bash
# Change model
uv run main.py --model llama3.1

# Enable verbose logging
uv run main.py --verbose true

# Set custom username
uv run main.py --username alice

# Adjust temperature for more creative responses
uv run main.py --temperature 0.7

# Combine multiple flags
uv run main.py --model llama3.1 --username alice --temperature 0.4 --verbose true
```

## User Interface

Run the Gradio UI for an interactive chat experience:

```bash
# Standard launch
uv run ui.py

# Development mode with auto-reload
gradio ui.py
```

![Agentic File Explorer UI](images/agentic_file_explorer_ui.png)

The UI includes:
- A chat page with streaming responses
- A settings page with customizable bot message colors (Purple, Blue, Emerald, Orange, Pink, Cyan)

## How It Works

### Agent System

The project uses two agents:

- **Main agent** (`stm_context_agent.py`): ReAct agent with short-term memory, streaming responses, and tool access. Handles both CLI and UI modes.
- **Summarization agent** (`stm_loader.py`): A secondary agent that automatically summarizes older conversation history when the context window exceeds 1000 tokens.

### Short-Term Memory & Context

When STM is enabled, the agent tracks message history with token counts (via tiktoken). If the conversation exceeds the configured `MAX_CONTEXT_WINDOW` (1000 tokens by default), older messages are summarized and replaced with a compact summary to preserve context without hitting model limits.

### File Dictionary

Files read or written during a session are cached in an in-memory file dictionary and injected into system prompts. This lets the agent reference previously accessed files without re-reading them from disk.

### Sandboxing

All file operations are restricted to the `data/` directory. Path construction ensures that no file or directory can be created or accessed outside this sandbox.

## Project Structure

```
agentic-file-explorer/
├── main.py                    # CLI entry point
├── ui.py                      # Gradio web UI
├── agent.py                   # Agent wrapper for UI streaming
├── stm_context_agent.py       # Main agent with short-term memory
├── no_context_agent.py        # Legacy stateless agent
├── stm.py                     # Short-term memory implementation
├── stm_loader.py              # Summarization agent loader
├── context.py                 # Context trimming and token counting
├── file.py                    # File model (Pydantic)
├── file_dictionary.py         # In-session file cache
├── compare.py                 # Exact and fuzzy string matching
├── setup_directory.py         # Sandboxed path construction
├── string_functions.py        # Path display utilities
├── arguments.py               # CLI argument parsing
├── chat_meta.py               # Session metadata model
├── logger.py                  # Logging utilities
├── txt_functions.py           # Text file I/O functions
├── txt_tools.py               # LangChain tool wrappers for txt
├── csv_functions.py           # CSV file I/O functions
├── csv_tools.py               # LangChain tool wrappers for csv
├── directory_functions.py     # Directory operation functions
├── directory_tools.py         # LangChain tool wrappers for directories
├── traversal_functions.py     # BFS/DFS search functions
├── traversal_tools.py         # LangChain tool wrappers for search
├── data/                      # Sandboxed workspace for file operations
├── logs/                      # Conversation and system logs
├── configs/                   # JSON configuration files
├── prompts/                   # System and assistant prompt templates
└── tests/                     # Unit tests
```

## Testing

Run the test suite:

```bash
uv run python -m unittest discover -s tests
```

Tests cover: text file operations, CSV operations, BFS/DFS traversal, directory functions, file model validation, file dictionary, path construction, and string utilities.

## Recommended Models

The following Ollama models work well with this project:

- **`qwen3:8b`** (recommended) - Best performance in testing
- `llama3.1` - Strong general performance; also used as the default summarization model
- `phi3.5` - Lightweight alternative

Browse more models at [Ollama Library](https://ollama.com/library).

## Resources

- [LangChain Documentation](https://docs.langchain.com/)
- [Gradio Documentation](https://www.gradio.app/docs)
- [Ollama Documentation](https://ollama.com/)
- [UV Package Manager](https://docs.astral.sh/uv/)

## Notes

- All file operations are sandboxed within the `data/` directory
- The `clear` tool is disabled by default and must be manually enabled in `tool_config.json`
- Search tools support both exact and approximate (fuzzy) matching
- Conversation logs are saved to `logs/agentic-fe.log` when verbose mode is enabled
- Short-term memory is enabled by default; disable with `--stm false`

## Development

### Capture Dependencies

```bash
uv lock
```

### Manual Virtual Environment Setup

```bash
# Create environment
uv venv --python /path/to/python3.12

# Activate
source .venv/bin/activate

# Deactivate when done
deactivate
```
