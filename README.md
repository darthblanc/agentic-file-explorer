# Agentic File Explorer

A file explorer powered by AI agents that can read, write, search, and manage files through natural language commands. Built with LangChain and Gradio, it runs locally using Ollama.

## Overview

This project implements an intelligent file management system using a [ReAct agent](https://docs.langchain.com/oss/python/langchain/agents#example-of-react-loop) that can understand and execute file operations through conversation. All operations happen in a sandboxed environment for safety.

**Key Features:**

- Natural language file operations (read, write, append, search)
- Smart file search with BFS/DFS strategies
- Short-term memory for contextual conversations
- Interactive UI built with Gradio
- Runs entirely locally with Ollama

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

| Tool                 | Description                                  | Supported Formats   |
| -------------------- | -------------------------------------------- | ------------------- |
| **Read**             | Read file contents                           | `.txt`, `.csv`      |
| **Write**            | Write or overwrite file contents             | `.txt`, `.csv`      |
| **Append**           | Append content to a new line                 | `.txt`, `.csv`      |
| **Clear**            | Clear file contents (manual enable required) | `.txt`, `.csv`      |
| **List Directory**   | Display files and subdirectories             | All                 |
| **Create Directory** | Create new directories                       | N/A                 |
| **BFS Search**       | Breadth-first file system search             | Files & directories |
| **DFS Search**       | Depth-first file system search               | Files & directories |

## Configuration

### Command-Line Flags

| Flag            | Default    | Description                         |
| --------------- | ---------- | ----------------------------------- |
| `--model`       | `qwen3:8b` | LLM model to use                    |
| `--verbose`     | `true`     | Enable logging to `agentic-fe.logs` |
| `--username`    | `User`     | Display name for the user           |
| `--temperature` | `0`        | Model temperature (0-1)             |
| `--stm`         | `true`     | Enable short-term memory            |

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
uv run main.py --model llama3.1 --username alice --temperature 0.4 --stm
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

## Project Structure

- **`data/`** - Sandboxed workspace for all file operations
- **`logs/`** - Conversation logs and system logs
- **`configs/`** - Agent configuration files
- **`prompts/`** - Pre-defined prompt templates
- **`tests/`** - Unit tests

## Testing

Run the test suite:

```bash
uv run python -m unittest discover -s tests
```

## Recommended Models

The following Ollama models work well with this project:

- **`qwen3:8b`** (recommended) - Best performance in testing
- `llama3.1` - Strong general performance
- `phi3.5` - Lightweight alternative

Browse more models at [Ollama Library](https://ollama.com/library).

## Resources

- [LangChain Documentation](https://docs.langchain.com/)
- [Gradio Documentation](https://www.gradio.app/docs)
- [Ollama Documentation](https://ollama.com/)
- [UV Package Manager](https://docs.astral.sh/uv/)

## Notes

- All file operations are sandboxed within the `data/` directory
- Search tools support both exact and approximate matching
- Conversation logs are automatically saved to the `logs/` directory
- Short-term memory is enabled by default for contextual conversations
- The `--verbose true` syntax is required for the verbose flag due to parsing behavior

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
