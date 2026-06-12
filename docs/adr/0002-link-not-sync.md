# nhq manages a link, not sync

`nhq` creates and manages a symlink from a checkout to a store. It makes **no
backup or sync promise** and contains zero sync code. Backup is achieved
entirely by pointing the root at a folder another tool already syncs (Dropbox,
iCloud, Syncthing, a NAS mount). The default root is `~/nhq` and deliberately
does **not** mention any sync provider.

## Why

Sync is a solved, deep problem (rclone and the named services own it); a small
personal tool reimplementing it would be both redundant and fragile. Decoupling
keeps `nhq` to two verbs and lets the user choose any sync mechanism. The store
living in an already-synced folder is what makes notes durable, not anything
`nhq` does.

## Consequence

A reader expecting a "notes backup tool" will find a tool that never touches the
network. That is intentional: the boundary is "manage the link and the derived
path"; everything about replication is out of scope. v1 touches no sync code at
all.
