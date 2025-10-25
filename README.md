# Agentic File Explorer

File explorer that uses Agentic Frameworks to perform tasks such as file reading, writing, and summarization.

## Getting Started

#### Set up Llama

```
ollama pull qwen3:8b
```

#### Install [UV](https://docs.astral.sh/uv/getting-started/installation/)

```
curl -LsSf https://astral.sh/uv/install.sh | sh # curl
wget -qO- https://astral.sh/uv/install.sh | sh # wget
```

#### Set up Environment (create environment and install dependencies)

```
uv sync
```

#### Run scripts

```
uv run main.py
```

## Auxiliary

#### Capture Dependencies

```
uv lock
```

#### Create Virtual Environment

```
uv venv --python /home/andi/.local/bin/python3.12
```

#### Activate Virtual Environment

```
source .venv/bin/activate
```

#### Deactivate Virtual Environment

```
deactivate
```
