#!/usr/bin/env python3
"""Compute and write the sha256 field for raw source files.

Usage:  python3 scripts/hash_raw.py raw/transcripts/2026-01-01-foo.md [more files...]

Convention (shared with lint.py): the hash is SHA-256 of the file body - everything after
the closing '---' of the frontmatter - with leading and trailing whitespace stripped,
UTF-8 encoded. Run this instead of asking an LLM for the hash: models cannot compute
SHA-256 and will invent a plausible-looking value.

Refuses to overwrite an existing real hash (raw files are immutable); it only fills in
placeholder or missing values. Standard library only.
"""
import hashlib
import re
import sys
from pathlib import Path

FM_RE = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)


def body_hash(body: str) -> str:
    return hashlib.sha256(body.strip().encode("utf-8")).hexdigest()


def main(paths):
    status = 0
    for arg in paths:
        p = Path(arg)
        m = FM_RE.match(p.read_text())
        if not m:
            print(f"SKIP  {p}: no frontmatter")
            status = 1
            continue
        fm, body = m.groups()
        digest = body_hash(body)
        existing = re.search(r"^sha256:\s*(\S.*)$", fm, re.M)
        if existing and not existing.group(1).startswith("<"):
            ok = existing.group(1).strip() == digest
            print(f"{'OK   ' if ok else 'DRIFT'} {p}")
            status |= 0 if ok else 1
            continue
        if existing:
            fm = fm.replace(existing.group(0), f"sha256: {digest}")
        else:
            fm += f"\nsha256: {digest}"
        p.write_text(f"---\n{fm}\n---\n{body}")
        print(f"WROTE {p}: {digest}")
    return status


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1:]))
