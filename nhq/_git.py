import subprocess
from pathlib import Path


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], capture_output=True, text=True)


def is_git_repo() -> bool:
    return _run("rev-parse", "--is-inside-work-tree").stdout.strip() == "true"


def get_origin_url() -> str | None:
    result = _run("remote", "get-url", "origin")
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def get_show_prefix() -> str:
    return _run("rev-parse", "--show-prefix").stdout.strip()


def get_config(key: str) -> str | None:
    result = _run("config", key)
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def get_exclude_path() -> str:
    return _run("rev-parse", "--git-path", "info/exclude").stdout.strip()


def ensure_excluded(line: str) -> None:
    exclude = Path(get_exclude_path())
    content = exclude.read_text() if exclude.exists() else ""
    if line in content.splitlines():
        return
    prefix = "" if content == "" or content.endswith("\n") else "\n"
    exclude.parent.mkdir(parents=True, exist_ok=True)
    with exclude.open("a") as file:
        file.write(prefix + line + "\n")
