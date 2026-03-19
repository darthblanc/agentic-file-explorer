# Agentic File Explorer

A locally-running AI agent that navigates, reads, writes, searches, and reasons over a file system through natural language — built on a **ReAct agent loop**, **modular tool architecture**, **short-term memory**, and **automatic context compaction**.

Structurally similar to document processing pipelines used in production legal and enterprise AI systems — running entirely on-device with no API keys required.

> **Stack:** LangChain · Ollama · Gradio · Python · uv

---

## How It Works

The agent runs a [ReAct (Reason + Act) loop](https://docs.langchain.com/oss/python/langchain/agents#example-of-react-loop) — at each turn it reasons about what needs to be done, selects the appropriate tool, observes the result, and decides whether to act again or respond. This allows it to handle multi-step tasks like:

> _"Find all CSV files in the project folder, read the one that mentions sales, and summarize the top 3 rows"_

without the user having to break the task down manually.

### Context Management

Running agents on smaller local models (8B parameters) introduces a hard constraint: limited context windows. This project solves that with two mechanisms:

- **Short-term memory (STM):** Maintains a rolling summary of the conversation rather than the full raw history, keeping context lean across long sessions
- **Automatic context compaction:** When the context approaches the model's limit, older content is summarized and compressed rather than truncated — preserving continuity without blowing up the window

This is the same class of problem solved in production agentic systems at scale.

### Tool Architecture

Tools are organized into **modular, domain-specific layers** rather than a monolithic tool list. Each file type and operation category has its own module:

```
agent_tools.py          ← top-level tool registry
├── traversal_tools.py  ← BFS / DFS search strategies
├── directory_tools.py  ← directory listing, creation
├── txt_tools.py        ← .txt read / write / append / clear
└── csv_tools.py        ← .csv read / write / append / clear
```

This separation makes it straightforward to add new file types or operation categories without touching the agent core — the same pattern used in production tool-use systems.

### Search Strategies

The agent chooses between two search strategies depending on the task:

- **BFS (Breadth-First Search):** Best for finding files near the top of a directory tree
- **DFS (Depth-First Search):** Best for locating deeply nested files

Both support exact and approximate matching.

---

## Available Tools

| Tool | Description | Formats |
|------|-------------|---------|
| **Read** | Read file contents | `.txt`, `.csv` |
| **Write** | Write or overwrite a file | `.txt`, `.csv` |
| **Append** | Append content to a new line | `.txt`, `.csv` |
| **Clear** | Clear file contents | `.txt`, `.csv` |
| **List Directory** | Display files and subdirectories | All |
| **Create Directory** | Create new directories | — |
| **BFS Search** | Breadth-first file system search | Files & dirs |
| **DFS Search** | Depth-first file system search | Files & dirs |

All operations are sandboxed within the `data/` directory.

---

## Quick Start

**1. Install [Ollama](https://ollama.com/download/linux) and pull the recommended model:**

```bash
ollama pull qwen3:8b
```

**2. Install the [uv](https://docs.astral.sh/uv/) package manager:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**3. Set up and run:**

```bash
uv sync
uv run main.py
```

**4. (Optional) Launch the Gradio UI:**

```bash
uv run ui.py
```

![Agentic File Explorer UI](images/agentic_file_explorer_ui.png)

---

## Configuration

| Flag | Default | Description |
|------|---------|-------------|
| `--model` | `qwen3:8b` | LLM model to use via Ollama |
| `--verbose` | `true` | Enable logging to `agentic-fe.logs` |
| `--username` | `User` | Display name in the UI |
| `--temperature` | `0` | Model temperature (0 = deterministic) |
| `--stm` | `true` | Enable short-term memory |

```bash
# Examples
uv run main.py --model llama3.1
uv run main.py --model qwen3:8b --username alice --temperature 0.4 --stm true
```

### Recommended Models

| Model | Notes |
|-------|-------|
| `qwen3:8b` ✅ | Best performance in testing |
| `llama3.1` | Strong general performance |
| `phi3.5` | Lightweight alternative |

The agent is model-agnostic — any Ollama-compatible model can be swapped in via `--model`.

---

## Project Structure

```
agentic-file-explorer/
├── agent.py                  # ReAct agent core
├── stm_context_agent.py      # Agent variant with STM + context compaction
├── no_context_agent.py       # Lightweight agent without memory
├── agent_tools.py            # Tool registry
├── traversal_tools.py        # BFS / DFS search tools
├── directory_tools.py        # Directory operations
├── txt_tools.py              # .txt file tools
├── csv_tools.py              # .csv file tools
├── stm.py                    # Short-term memory module
├── stm_loader.py             # STM initialization
├── context.py                # Context window management + compaction
├── compare.py                # File comparison utilities
├── chat_meta.py              # Conversation metadata tracking
├── logger.py                 # Logging utilities
├── ui.py                     # Gradio UI
├── configs/                  # Agent configuration files
├── prompts/                  # Prompt templates
├── system_prompts/           # System prompt definitions
├── tests/                    # Unit test suite
└── data/                     # Sandboxed workspace (all file ops run here)
```

---

## Testing

```bash
uv run python -m unittest discover -s tests
```

---

## Design Decisions

**Why Qwen3:8b?** It consistently outperformed larger models on tool-selection accuracy in local testing — the structured reasoning required for ReAct loops benefits more from instruction-following quality than raw parameter count.

**Why local / Ollama?** Zero API costs, no data leaving the machine, and the ability to swap models freely. The context management work was motivated specifically by the constraints of running 8B models — a constraint that doesn't disappear at larger scales, it just shifts.

**Why modular tools?** A flat list of tools degrades agent performance as the tool count grows — the model struggles to select correctly. Domain-grouped modules keep the tool surface clean and make the system easier to extend.

---

## Resources

- [LangChain Docs](https://docs.langchain.com/)
- [Ollama Library](https://ollama.com/library)
- [Gradio Docs](https://www.gradio.app/docs)
- [uv Package Manager](https://docs.astral.sh/uv/)
