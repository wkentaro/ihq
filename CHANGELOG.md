# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `ihq migrate <path>` moves an existing, untracked path into this repo's store
  under `$IHQ_ROOT/<host>/<user>/<repo>/`, leaves a symlink behind, adds a
  `.git/info/exclude` entry, and (for a directory) drops an empty `.ihqdir`
  marker so the managed set can be derived by scanning the store. It is the only
  verb that creates store content, and it hard-refuses git-tracked paths.
- `ihq link [path]` attaches a path the store already has; with no argument it
  links every managed path not yet linked here (the second-machine flow). It
  never creates store content.
- `ihq unlink <path>` / `ihq unlink --all` remove links and their exclude
  entries, leaving the store untouched; `--all` also clears broken links whose
  store slot is gone.
- `ihq list` shows every managed path and its per-checkout status.
- `ihq root` prints the resolved store-root directory, the same way `ghq root`
  does.
- The store is a per-repo mirror tree: each externalized path lives at its
  repo-relative location, with every managed directory marked by an empty
  `.ihqdir` file, so a nested path simply nests and any checkout derives the full
  set to link by scanning the store.
- `--version` and `--help` output on stdout, with Examples sections in each
  subcommand's help.
