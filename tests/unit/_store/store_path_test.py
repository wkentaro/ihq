from pathlib import Path

from nhq._store import store_path

_IDENTITY = "github.com/wkentaro/labelme"


def test_store_path_root() -> None:
    assert store_path(Path("/r"), _IDENTITY, "") == Path("/r") / _IDENTITY


def test_store_path_subtree() -> None:
    result = store_path(Path("/r"), _IDENTITY, "tests/")
    assert result == Path("/r/github.com/wkentaro/labelme%2Ftests")


def test_store_path_nested_subtree() -> None:
    result = store_path(Path("/r"), _IDENTITY, "labelme/widgets")
    assert result == Path("/r/github.com/wkentaro/labelme%2Flabelme%2Fwidgets")


def test_store_path_percent_in_subpath_is_encoded() -> None:
    result = store_path(Path("/r"), _IDENTITY, "a%b")
    assert result == Path("/r/github.com/wkentaro/labelme%2Fa%25b")
