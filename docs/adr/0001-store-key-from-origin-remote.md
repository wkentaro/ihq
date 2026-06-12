# Store key is derived from the origin remote, ghq-style

A repo's store path is derived from its `origin` remote URL, normalized the way
`ghq` lays out checkouts: `<host>/<user>/<repo>`, arbitrary depth, `.git`
stripped. So `git@github.com:wkentaro/labelme.git` keys to
`<root>/github.com/wkentaro/labelme`. A repo with no `origin` remote is a hard
error, not a fallback to some local name.

## Why

The key must be stable across machines and checkouts, and it must be the *same*
regardless of where the repo is cloned on disk. Repo identity (the remote)
satisfies this; the filesystem path does not (it varies per machine and per
clone). Keying off the remote is also the `ghq` mental model the tool homages,
so the store path mirrors the ghq checkout path one-to-one.

## Considered and rejected

- **Filesystem path relative to a ghq root.** Breaks if the repo lives outside a
  ghq root or is cloned to a different path on another machine; the store would
  not be shared.
- **Any remote, or the first remote.** Non-deterministic; a stray fork remote
  could silently retarget the store. `origin` specifically is the deterministic
  common case.

This is hard to reverse: changing the derivation orphans every existing store.
