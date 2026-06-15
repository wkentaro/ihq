# Derive the managed set by scanning the store, marking directories

Supersedes ADR-0008 (a manifest in the store records the managed set).

There is no `.ihq` manifest. The managed set for a repo is **derived by walking
the store**: every file is a managed leaf, every directory is either a managed
unit or an intermediate mirror directory that only holds deeper managed paths.
The two directory cases are told apart by a **marker**: an empty reserved file
`.ihqdir` placed *inside* a managed directory. A directory with the marker is a
managed unit and the walk stops there; an unmarked directory is intermediate and
the walk recurses into it. Files carry no marker, since a leaf is unambiguous.

## Why

ADR-0008 introduced the manifest precisely because "walking the store cannot
tell whether `backend` is the managed unit or `backend/.env` is." The marker
removes that obstacle: it records the unit boundary in the store's own
structure, so the boundary no longer needs a separate index. Deleting a managed
path then becomes the *whole* operation, no second edit, which is the entire
point. With the manifest, deleting a store folder left a dangling entry the user
had to hand-remove from `.ihq`.

The marker lives **inside** the managed directory, not beside it, so that marker
and data are atomic: created together by `migrate`, deleted together when the
folder is removed, and synced together as one unit. There is no way for the
record and the data to desync, so there are no orphan markers and no "missing
from store" record to reconcile.

## Considered and rejected

- **Keep the manifest but auto-prune it.** On each command, drop entries whose
  store slot is gone. This fixes the manual-edit pain but is unsafe on a
  sync-backed store (ADR-0001, ADR-0002): if sync has not yet pulled a folder,
  the slot looks missing and auto-prune would *permanently* destroy the record
  for data about to arrive. Scanning has nothing to destroy. A transiently
  absent folder simply is not linked this run and links once sync catches up.

- **A sibling marker** (`scratch.ihqdir` next to `scratch/`). Keeps the marker
  out of the checkout, but reintroduces the pain for directories: deleting
  `scratch/` orphans the marker, so the dangling-record problem returns. Worse,
  deleting the marker silently reclassifies the directory's contents as
  individually-managed files. The inside marker is one hidden dotfile per
  managed directory, the cost of which is trivial next to atomicity.

## Consequence

- **Incomplete-store detection is gone.** With no recorded expectation to
  compare against, present-in-store *is* the managed set. If a sync is mid-pull,
  a checkout links the partial set and the user re-runs later.
- `migrate` writes the marker only when externalizing a directory, and refuses
  any path whose basename is `.ihqdir` (the old refusal of `.ihq` is dropped).
  The overlap guard and `migratable` read the scanned set, not a manifest.
- The scan never descends into a managed directory, so its cost is proportional
  to the managed-path skeleton, not to the content under it.
- `list`'s `!` mark is re-pointed (amending ADR-0011's note about it): it no
  longer means "manifest entry missing from store" but "a link present in this
  checkout whose store slot is gone." That state is sourced from
  `.git/info/exclude`, the per-checkout footprint ihq already maintains, and is
  shared with `unlink --all` so the same orphan links it flags can be cleaned.
