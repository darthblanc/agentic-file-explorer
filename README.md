# Agentic File Explorer

A locally-running AI agent that navigates, reads, writes, searches, and reasons over a file system through natural language — built on a **ReAct agent loop**, **modular tool architecture**, **short-term memory**, and **automatic context compaction**.

Structurally similar to document processing pipelines used in production legal and enterprise AI systems — running entirely on-device with no API keys required.

> **Stack:** LangChain · Ollama · Gradio · Python · uv

---

## How It Works

### Agent Loop

The agent runs a [ReAct (Reason + Act) loop](https://docs.langchain.com/oss/python/langchain/agents#example-of-react-loop) — at each turn it reasons about what needs to be done, selects the appropriate tool, observes the result, and decides whether to act again or respond. This lets it handle multi-step tasks like:

> *"Find all CSV files in the project folder, read the one that mentions sales, and summarize the top 3 rows"*

without the user having to decompose the task manually.

Two agent variants are available:

- **`stm_context_agent`** — Full agent with short-term memory, context compaction, and streaming responses. Default mode.
- **`no_context_agent`** — Lightweight stateless agent with no memory. Useful for isolated single-turn tasks.

### Context Management

Running agents on smaller local models (8B parameters) introduces a hard constraint: limited context windows. This project addresses that with two mechanisms working in tandem:

**Short-term memory (STM):** Token count is tracked incrementally across turns. When the conversation exceeds `MAX_CONTEXT_WINDOW` (1000 tokens by default), a secondary summarization agent compresses older messages into a compact summary — preserving continuity without truncating history or blowing up the window.

**File references instead of content injection:** Rather than inserting raw file contents into the system prompt, the agent maintains a `FileDictionary` — a lightweight in-memory registry mapping file IDs to metadata. The system prompt receives references, not contents. Files are only read in full when a tool explicitly requests them.

This prevents context pollution and eliminates cross-turn file confusion in the model. It also makes agent behavior more auditable: tool calls are the only path to file data, so you can always see exactly what the agent accessed and when.

*Context management approach informed by the taxonomy in [Context Engineering 2.0](https://arxiv.org/abs/2510.26493) (Hua et al., 2025).*

### Tool Architecture

Tools are organized into **modular, domain-specific layers** rather than a flat list. A flat tool list degrades agent tool-selection accuracy as the tool count grows — the model struggles to choose correctly. Domain-grouped modules keep the tool surface clean:

```
agent_tools.py          ← top-level tool registry
├── traversal_tools.py  ← BFS / DFS search strategies
├── directory_tools.py  ← directory listing and creation
├── txt_tools.py        ← .txt read / write / append / clear
└── csv_tools.py        ← .csv read / write / append / clear
```

Each domain has a separate **functions layer** (pure logic) and a **tools layer** (LangChain wrappers) — keeping the agent core decoupled from file I/O implementation. Adding support for a new file type means adding one functions file and one tools file; the agent is untouched.

### Search Strategies

The agent selects between two traversal strategies depending on the task:

- **BFS (Breadth-First Search):** Best for finding files near the top of a directory tree
- **DFS (Depth-First Search):** Best for locating deeply nested files

Both support exact and approximate (fuzzy) matching using a 0.8 similarity threshold via `SequenceMatcher`.

---

## Design Decisions

**Why Qwen3:8b?** It consistently outperformed larger models on tool-selection accuracy in local testing. ReAct loops depend heavily on instruction-following quality — the model needs to correctly identify which tool to call and with what arguments on every step. That benefits more from instruction-following discipline than raw parameter count.

**Why local / Ollama?** Zero API costs, no data leaving the machine, and the freedom to swap models freely via `--model`. The context management work was motivated directly by the constraints of running 8B models — those constraints don't disappear at larger scales, they just shift.

**Why modular tools over a flat list?** A flat tool list causes the model to select incorrectly as tool count grows. Grouping by domain keeps the surface lean and makes failure modes easier to diagnose — if the agent misuses a file operation, you know exactly which module to inspect.

**Why file references?** Early testing showed that injecting raw file contents into the system prompt caused the model to hallucinate edits and confuse files across turns. Replacing contents with lightweight references keeps context lean and forces tool calls to be the only path to file data — which also makes agent behavior more predictable and auditable. Approach informed by [Context Engineering 2.0](https://arxiv.org/abs/2510.26493) (Hua et al., 2025).

**Why BFS and DFS as separate tools?** Giving the agent both strategies and letting it choose based on task context — rather than always running one — improves search efficiency and mirrors how a human would approach the problem. Shallow search for obvious files, deep search when you expect nesting.

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

## Available Tools

| Tool | Description | Formats |
|------|-------------|---------|
| **Read** | Read file contents | `.txt`, `.csv` |
| **Write** | Write or overwrite a file | `.txt`, `.csv` |
| **Append** | Append content to a new line | `.txt`, `.csv` |
| **Clear** | Clear file contents (disabled by default) | `.txt`, `.csv` |
| **List Directory** | Display files and subdirectories | All |
| **Create Directory** | Create new directories | — |
| **BFS Search** | Breadth-first file system search | Files & dirs |
| **DFS Search** | Depth-first file system search | Files & dirs |

All operations are sandboxed within the `data/` directory. The `clear` tool must be manually enabled in `configs/tool_config.json`.

---

## Configuration

| Flag | Default | Description |
|------|---------|-------------|
| `--model` | `qwen3:8b` | LLM model to use via Ollama |
| `--verbose` | `false` | Enable logging to `logs/agentic-fe.log` |
| `--username` | `user` | Display name in the UI |
| `--temperature` | `0` | Model temperature (0 = deterministic) |
| `--stm` | `true` | Enable short-term memory and context compaction |

> **Note:** Boolean flags require an explicit value: `--verbose true`, `--stm false`.

```bash
# Use a different model
uv run main.py --model llama3.1

# Verbose logging + custom username
uv run main.py --verbose true --username alice

# More creative responses
uv run main.py --temperature 0.7

# Combine flags
uv run main.py --model llama3.1 --username alice --temperature 0.4 --verbose true
```

### Recommended Models

| Model | Notes |
|-------|-------|
| `qwen3:8b` ✅ | Best tool-selection accuracy in testing |
| `llama3.1` | Strong general performance; also used as default summarization model |
| `phi3.5` | Lightweight alternative for lower-resource machines |

The agent is model-agnostic — any Ollama-compatible model can be swapped in via `--model`.

---

## Project Structure

```
agentic-file-explorer/
├── main.py                   # CLI entry point and agent initialization
├── ui.py                     # Gradio web UI
├── agent.py                  # Agent wrapper for UI streaming
├── stm_context_agent.py      # Main agent: STM + context compaction + streaming
├── no_context_agent.py       # Lightweight stateless agent (no memory)
│
├── stm.py                    # Short-term memory: token tracking + compaction trigger
├── stm_loader.py             # Summarization agent loader
├── context.py                # Context window management, trimming, token counting
│
├── file.py                   # File model (Pydantic)
├── file_dictionary.py        # In-session file reference registry
│
├── agent_tools.py            # Top-level tool registry
├── traversal_tools.py        # BFS / DFS LangChain tool wrappers
├── traversal_functions.py    # BFS / DFS traversal logic
├── directory_tools.py        # Directory operation tool wrappers
├── directory_functions.py    # Directory operation logic
├── txt_tools.py              # .txt file tool wrappers
├── txt_functions.py          # .txt file I/O logic
├── csv_tools.py              # .csv file tool wrappers
├── csv_functions.py          # .csv file I/O logic
│
├── compare.py                # Exact and fuzzy string matching
├── setup_directory.py        # Sandboxed path construction
├── string_functions.py       # Path display utilities
├── chat_meta.py              # Session metadata model
├── arguments.py              # CLI argument parsing
├── logger.py                 # Logging utilities
│
├── configs/                  # JSON configuration files (model settings, tool flags)
├── prompts/                  # Prompt templates
├── system_prompts/           # System prompt definitions
├── tests/                    # Unit test suite
├── data/                     # Sandboxed workspace — all file operations run here
└── logs/                     # Conversation and system logs
```

---

## Testing

```bash
uv run python -m unittest discover -s tests
```

Tests cover: text file operations, CSV operations, BFS/DFS traversal, directory functions, file model validation, file dictionary, sandboxed path construction, and string utilities.

---

## Resources

- [Context Engineering 2.0](https://arxiv.org/abs/2510.26493) — Hua et al., 2025 (theoretical foundation for context management approach)
- [LangChain Documentation](https://docs.langchain.com/)
- [Ollama Library](https://ollama.com/library)
- [Gradio Documentation](https://www.gradio.app/docs)
- [uv Package Manager](https://docs.astral.sh/uv/)