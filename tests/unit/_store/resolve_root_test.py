from pathlib import Path

from nhq._store import resolve_root


def test_resolve_root_default() -> None:
    assert resolve_root(env_root=None, config_root=None) == Path.home() / "nhq"


def test_resolve_root_env_wins() -> None:
    assert resolve_root(env_root="/env", config_root="/config") == Path("/env")


def test_resolve_root_config_when_no_env() -> None:
    assert resolve_root(env_root=None, config_root="/config") == Path("/config")


def test_resolve_root_empty_env_falls_through() -> None:
    assert resolve_root(env_root="", config_root="/config") == Path("/config")


def test_resolve_root_expanduser() -> None:
    assert resolve_root(env_root="~/notes", config_root=None) == Path.home() / "notes"
