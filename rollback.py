import os
import subprocess
import threading


def _default_data_dir() -> str:
    return os.environ.get("DATA_DIR", "data")


# Per-directory locks to prevent git lock-file races from concurrent commits
_git_locks: dict[str, threading.Lock] = {}
_git_locks_mu = threading.Lock()


def _get_lock(data_dir: str) -> threading.Lock:
    with _git_locks_mu:
        if data_dir not in _git_locks:
            _git_locks[data_dir] = threading.Lock()
        return _git_locks[data_dir]


def _run_git(args: list, data_dir: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git"] + args,
        cwd=data_dir,
        capture_output=True,
        text=True,
    )


def ensure_git_repo(data_dir: str | None = None) -> None:
    data_dir = data_dir or _default_data_dir()
    os.makedirs(data_dir, exist_ok=True)
    if not os.path.exists(os.path.join(data_dir, ".git")):
        _run_git(["init"], data_dir)
        _run_git(["config", "user.email", "agent@local"], data_dir)
        _run_git(["config", "user.name", "Agent"], data_dir)
        _run_git(["add", "."], data_dir)
        _run_git(["commit", "--allow-empty", "-m", "initial: snapshot data directory"], data_dir)


def _do_commit(filepath: str, operation: str, data_dir: str) -> None:
    with _get_lock(data_dir):
        _run_git(["add", filepath], data_dir)
        _run_git(["commit", "-m", f"agent: {operation} {filepath}"], data_dir)


def commit_async(filepath: str, operation: str, data_dir: str | None = None) -> None:
    """Fire-and-forget background commit after a file operation."""
    data_dir = data_dir or _default_data_dir()
    threading.Thread(target=_do_commit, args=(filepath, operation, data_dir), daemon=True).start()


def rollback_last_change(data_dir: str | None = None) -> str:
    data_dir = data_dir or _default_data_dir()
    last = _run_git(["log", "--oneline", "-1"], data_dir)
    if not last.stdout.strip():
        return "No committed changes to roll back."
    result = _run_git(["revert", "HEAD", "--no-edit"], data_dir)
    if result.returncode == 0:
        return f"Rolled back: {last.stdout.strip()}"
    return f"Rollback failed: {result.stderr}"


def rollback_all_changes(data_dir: str | None = None) -> str:
    data_dir = data_dir or _default_data_dir()
    log = _run_git(["log", "--oneline"], data_dir)
    commits = [c for c in log.stdout.strip().split("\n") if c]
    if len(commits) <= 1:
        return "Already at initial state, nothing to roll back."
    initial_hash = commits[-1].split()[0]
    result = _run_git(["reset", "--hard", initial_hash], data_dir)
    if result.returncode == 0:
        return "Rolled back all changes to initial state."
    return f"Rollback failed: {result.stderr}"


def list_changes(data_dir: str | None = None) -> str:
    data_dir = data_dir or _default_data_dir()
    result = _run_git(["log", "--oneline"], data_dir)
    return result.stdout.strip() or "No changes recorded."


def get_commits(n: int = 10, skip: int = 0, data_dir: str | None = None) -> list[dict]:
    data_dir = data_dir or _default_data_dir()
    result = _run_git(["log", "--format=%h|%s", f"-n{n}", f"--skip={skip}"], data_dir)
    commits = []
    for line in result.stdout.strip().splitlines():
        if "|" in line:
            h, msg = line.split("|", 1)
            commits.append({"hash": h.strip(), "message": msg.strip()})
    return commits


def get_commit_stat(commit_hash: str, data_dir: str | None = None) -> list[str]:
    data_dir = data_dir or _default_data_dir()
    result = _run_git(["diff-tree", "--no-commit-id", "-r", "--name-only", commit_hash], data_dir)
    return [f.strip() for f in result.stdout.strip().splitlines() if f.strip()]


def get_file_diff(commit_hash: str, filepath: str, data_dir: str | None = None) -> str:
    data_dir = data_dir or _default_data_dir()
    result = _run_git(["show", commit_hash, "--", filepath], data_dir)
    return result.stdout


# Initialize on import
ensure_git_repo()
