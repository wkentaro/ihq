# Subtree stores are flattened siblings, percent-encoded

A subtree of a repo gets its own store, keyed by the subpath
(`git rev-parse --show-prefix`). Rather than nesting the subtree store inside the
repo store, the subpath is **percent-encoded and appended to the repo leaf** as a
sibling directory, via `urllib.parse.quote(subpath, safe="")`:

```
root of repo:           <root>/github.com/wkentaro/labelme
subtree tests/:         <root>/github.com/wkentaro/labelme%2Ftests
subtree labelme/widgets: <root>/github.com/wkentaro/labelme%2Flabelme%2Fwidgets
```

The repo leaf gets `quote("/" + subpath)` appended, so every `/` (including the
joining one) becomes `%2F` uniformly. The repo-root store has no suffix.

## Why flatten instead of nest

`ghq`, Go's module cache, Cargo, and Maven all *nest* identity into a directory
tree, and that was the obvious path. But those stores hold content fully
determined by the key; `nhq` stores mix **user-created free-form notes** at the
same level where structural subtree dirs would live. Nesting therefore allows a
real collision: a root note named `tests` (a file) cannot coexist with a
`tests/` subtree store (a directory). Flattening to siblings removes that class
of edge entirely. The free-form-notes-at-store-root property is the specific
reason `nhq` departs from the nest-everywhere idiom; do not "fix" it back to
nesting.

## Why percent-encoding specifically

The encoding must be injective (no two distinct keys collide), and the resulting
directory name must be valid on every filesystem the store may sync to.

- **A bare `%` separator** (`labelme%tests`) is readable but not injective without
  a guard, and is not reversible.
- **systemd-escape semantics** (`/` -> `-`, literal `-` -> `\x2d`) is the Unix
  standard and is reversible, but its escape emits a backslash, which is invalid
  in Windows filenames and would break a store synced to a Windows machine.
- **`urllib.parse.quote(safe="")`** (RFC 3986 percent-encoding) is stdlib,
  injective by construction (no guard needed), reversible via `unquote` (keeps a
  future `nhq list` / `nhq path` viable), and `%` is a legal filename character
  on NTFS, APFS, and ext4 and passes cleanly through rsync, Dropbox, iCloud, and
  Syncthing. The only cost is readability of the directory name, which is not a
  priority for a machine-managed store.

This is hard to reverse: changing the layout or encoding orphans every existing
subtree store.
