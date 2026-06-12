from pathlib import Path

from tests.conftest import GitRepo

from .conftest import NhqCLI


def _exclude_lines(git_repo: GitRepo) -> list[str]:
    exclude = Path(git_repo.path) / ".git/info/exclude"
    return exclude.read_text().splitlines()


def test_link_creates_symlink_and_exclude(cli: NhqCLI, git_repo: GitRepo) -> None:
    cli.run_ok("init")

    result = cli.run_ok("link")

    store = cli.nhq_root / "github.com/wkentaro/labelme"
    link = Path(git_repo.path) / "nhq"
    assert link.is_symlink()
    assert link.readlink() == store
    assert "/nhq" in _exclude_lines(git_repo)
    assert "already linked" not in result.stderr
    assert "linked" in result.stderr


def test_link_is_idempotent(cli: NhqCLI, git_repo: GitRepo) -> None:
    cli.run_ok("init")
    cli.run_ok("link")

    result = cli.run_ok("link")

    assert "already linked" in result.stderr
    assert _exclude_lines(git_repo).count("/nhq") == 1


def test_link_subtree(cli: NhqCLI, git_repo: GitRepo) -> None:
    subdir = git_repo.mkdir("services/api")
    cli.run_ok("init", cwd=subdir)

    cli.run_ok("link", cwd=subdir)

    store = cli.nhq_root / "github.com/wkentaro/labelme%2Fservices%2Fapi"
    link = Path(subdir) / "nhq"
    assert link.is_symlink()
    assert link.readlink() == store
    assert "/services/api/nhq" in _exclude_lines(git_repo)


def test_link_appends_after_file_without_trailing_newline(
    cli: NhqCLI, git_repo: GitRepo
) -> None:
    cli.run_ok("init")
    exclude = Path(git_repo.path) / ".git/info/exclude"
    exclude.write_text("manual-entry")  # no trailing newline

    cli.run_ok("link")

    lines = _exclude_lines(git_repo)
    assert "manual-entry" in lines
    assert "/nhq" in lines


def test_link_requires_store(cli: NhqCLI) -> None:
    result = cli.run("link")

    assert result.returncode == 1
    assert "no store for this repo" in result.stderr


def test_link_refuses_foreign_symlink(cli: NhqCLI, git_repo: GitRepo) -> None:
    cli.run_ok("init")
    (Path(git_repo.path) / "nhq").symlink_to("/somewhere/else")

    result = cli.run("link")

    assert result.returncode == 1
    assert "already links to" in result.stderr


def test_link_store_missing_wins_over_existing_link(
    cli: NhqCLI, git_repo: GitRepo
) -> None:
    # No init, so the store does not exist; an unrelated ./nhq is also present.
    (Path(git_repo.path) / "nhq").symlink_to("/somewhere/else")

    result = cli.run("link")

    assert result.returncode == 1
    assert "no store for this repo" in result.stderr


def test_link_refuses_regular_file(cli: NhqCLI, git_repo: GitRepo) -> None:
    cli.run_ok("init")
    (Path(git_repo.path) / "nhq").write_text("not a link")

    result = cli.run("link")

    assert result.returncode == 1
    assert "not an nhq symlink" in result.stderr


def test_link_help(cli: NhqCLI) -> None:
    result = cli.run_ok("link", "--help")

    assert "nhq link" in result.stderr
