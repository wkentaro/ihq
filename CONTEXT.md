# nhq

`nhq` ("notes headquarters") keeps private notes alongside a git repo without
ever committing them. It manages a symlink from inside a checkout to a notes
directory that lives outside git, in a folder the user already syncs. The
layout is modeled on `ghq`: a configurable root, with a fixed
`host/user/repo` layout derived beneath it.

## Language

**Store**:
The actual private notes directory for one repo (or one subtree of a repo),
living under the root, outside git, and shared across all of a user's machines.
The "headquarters" half of the model.
_Avoid_: notes folder, backup dir.

**Link**:
The `nhq` symlink inside a checkout that points at the store. Per-checkout and
per-machine, never committed (it lives only in the working tree and is hidden
via `.git/info/exclude`). The "outpost" half of the model.
_Avoid_: alias, shortcut.

**Root**:
The configurable base directory under which every store lives (resolved from
`NHQ_ROOT`, then `git config nhq.root`, then the default `~/nhq`). Points at a
folder some other tool already syncs; `nhq` itself never syncs.
_Avoid_: base, home, NHQ_ROOT (that is the env var, not the concept).

**Subpath**:
The in-repo path from the repo toplevel to the working directory where a verb
is run (`git rev-parse --show-prefix`). Empty at the repo root; identifies a
subtree store otherwise. It is repo-relative, so it is identical on every
machine.
_Avoid_: prefix, relative path.
