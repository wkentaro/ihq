# Hide via `.git/info/exclude` only; `link` never auto-creates the store

The link is hidden from git using a single anchored line in
`.git/info/exclude` (per-repo, untracked, invisible to the team). There are
**no git hooks and no pre-commit guard** ("trust the ignore"). And `nhq link`
**errors if the store does not exist** ("no store for this repo; run
`nhq init`") rather than creating it; store creation is the separate, deliberate
`nhq init` act.

## Why exclude-only

`.git/info/exclude` is the one ignore mechanism that is per-checkout and never
travels into the repo's history or to teammates, which is exactly the privacy
property wanted. Hooks would add a moving part, can be bypassed, and are
per-repo state that has to be installed and maintained. The ignore is trusted;
the tool does not police commits.

## Why `link` refuses to auto-init

Auto-creating a store on `link` would silently manufacture a store for a typo'd
or wrong-identity repo (for example a misconfigured remote), scattering junk
stores. Splitting the deliberate once-ever `init` (store plane) from the routine
per-machine `link` (link plane) makes store creation an explicit choice and the
refusal a safety guard.

## Consequence

A reviewer may expect a commit-time guard and find none; that is deliberate. The
two-verb split (`init` creates the store, `link` only connects to an existing
one) is load-bearing, not incidental.
