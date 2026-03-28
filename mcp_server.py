"""
MCP server exposing file-exploration tools so any MCP-compatible client
(Claude Desktop, etc.) can read, write, and search the data directory.

Run with:
    mcp dev mcp_server.py

Or install into Claude Desktop's config:
    mcp install mcp_server.py --name "agentic-file-explorer"
"""
import os
from mcp.server.fastmcp import FastMCP
from txt_functions import read as _txt_read, write as _txt_write, append as _txt_append
from csv_functions import (
    read as _csv_read,
    write as _csv_write,
    append as _csv_append,
    get_headers as _csv_headers,
)
from directory_functions import get_content as _dir_list, create as _dir_create
from traversal_functions import breadth_first_search, depth_first_search

_DATA_DIR = os.environ.get("DATA_DIR", "data")

mcp = FastMCP("agentic-file-explorer")


# ── Text file tools ───────────────────────────────────────────────────────────

@mcp.tool()
def read_txt_file(path: str) -> str:
    """Read a text file from the data directory. Returns the file contents."""
    return _txt_read(path, data_dir=_DATA_DIR)


@mcp.tool()
def write_txt_file(path: str, content: str) -> str:
    """Write (overwrite) a text file in the data directory."""
    return _txt_write(path, content, data_dir=_DATA_DIR)


@mcp.tool()
def append_txt_file(path: str, content: str) -> str:
    """Append text to a file in the data directory."""
    return _txt_append(path, content, data_dir=_DATA_DIR)


# ── CSV file tools ────────────────────────────────────────────────────────────

@mcp.tool()
def read_csv_file(path: str, n_rows: int = 0, from_end: bool = False) -> str:
    """Read a CSV file. Returns JSON-encoded list of row dicts.
    n_rows=0 means all rows. Set from_end=True to read the last n rows.
    """
    return _csv_read(
        path,
        n_rows=n_rows if n_rows > 0 else None,
        from_end=from_end,
        data_dir=_DATA_DIR,
    )


@mcp.tool()
def get_csv_headers(path: str) -> str:
    """Return JSON-encoded list of column headers from a CSV file."""
    return _csv_headers(path, data_dir=_DATA_DIR)


@mcp.tool()
def write_csv_file(path: str, rows_json: str, column_names: list[str]) -> str:
    """Write (overwrite) a CSV file. rows_json is a JSON-encoded list of row dicts."""
    import json
    rows = json.loads(rows_json)
    return _csv_write(path, rows, column_names, data_dir=_DATA_DIR)


@mcp.tool()
def append_csv_file(path: str, rows_json: str, column_names: list[str]) -> str:
    """Append rows to a CSV file. rows_json is a JSON-encoded list of row dicts."""
    import json
    rows = json.loads(rows_json)
    return _csv_append(path, rows, column_names, data_dir=_DATA_DIR)


# ── Directory tools ───────────────────────────────────────────────────────────

@mcp.tool()
def list_directory(directory: str) -> str:
    """List contents of a directory inside the data directory."""
    return _dir_list(directory)


@mcp.tool()
def create_directory(directory: str) -> str:
    """Create a directory (and parents) inside the data directory."""
    return _dir_create(directory)


# ── Search / traversal tools ──────────────────────────────────────────────────

@mcp.tool()
def search_bfs(source_directory: str, target: str = "", approximate: bool = False) -> dict:
    """Breadth-first search through the data directory tree.
    Leave target empty to list all files. Set approximate=True for fuzzy name matching.
    """
    return breadth_first_search(source_directory, target=target, approximate=approximate)


@mcp.tool()
def search_dfs(source_directory: str, target: str = "", approximate: bool = False) -> dict:
    """Depth-first search through the data directory tree.
    Leave target empty to list all files. Set approximate=True for fuzzy name matching.
    """
    return depth_first_search(source_directory, target=target, approximate=approximate)


if __name__ == "__main__":
    mcp.run()
