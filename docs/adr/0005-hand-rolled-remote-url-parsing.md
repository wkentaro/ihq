# Remote URL parsing is hand-rolled, dep-free, and must not use `urlparse`

`parse_remote_url` in `_store.py` parses the `origin` URL into `host/user/repo`
with a small hand-written parser and no third-party dependency. It must branch
explicitly on the **scp-like** form (`git@host:path`) versus scheme URLs
(`https://`, `ssh://`), strip `user@` / scheme / port / a trailing `.git`, and
preserve arbitrary path depth. It is backed by a "URL zoo" test covering scp,
https, ssh-with-port, deep (gitlab subgroup) paths, and `.git`-less forms.

## Why not `urllib.parse.urlparse`

The scp-like form is the most common git remote and is **not** a URL.
`urlparse("git@github.com:wkentaro/labelme.git")` returns an empty scheme/host
and dumps everything into `path`, so any parser built on `urlparse` silently
mishandles the dominant case. The explicit scp branch is the reason this code
exists; do not "simplify" it onto `urlparse`.

## Why no library

`giturlparse` would handle the long tail correctly, but the parsing nhq needs is
~12 lines and adding a runtime dependency for it is not worth it given the small,
well-tested surface. The zoo test is what guards correctness, not the dependency.

Trade-off: a hand-rolled parser can miss an exotic URL form a library would
catch. The zoo test is the mitigation; extend it when a new form appears rather
than reaching for a dependency.
