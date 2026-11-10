#!/usr/bin/env python3
"""Minimal wiki lint. Implements the mechanical checks from AGENTS.md section 5.

Usage:  python3 scripts/lint.py [wiki-root]

Checks: broken wikilinks, orphan pages, pages missing from index.md, frontmatter
fields, tags not in the SCHEMA.md taxonomy, raw/ sha256 drift, pages >200 lines.
Exits non-zero if any broken link / frontmatter / tag / drift problem is found.
Standard library only.
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
WIKI_DIRS = ["entities", "concepts", "comparisons", "queries", "decisions"]
REQUIRED = ["title", "created", "updated", "type", "tags", "confidence"]
SKIP_NAMES = {"adr-template"}  # files that are templates, not pages

FM_RE = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)
LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")


def split_frontmatter(text):
    m = FM_RE.match(text)
    if not m:
        return None, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "-")):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, m.group(2)


def taxonomy_tags():
    """Tags are the backticked names at the start of bullet lines in SCHEMA.md's taxonomy."""
    schema = (ROOT / "SCHEMA.md").read_text()
    section = schema.split("## Tag Taxonomy", 1)[-1].split("\n## ", 1)[0]
    return set(re.findall(r"^- `([a-z0-9-]+)`", section, re.M))


def main():
    problems, warnings = [], []
    allowed = taxonomy_tags()

    pages = {}
    for d in WIKI_DIRS:
        for p in (ROOT / d).rglob("*.md"):
            if p.stem not in SKIP_NAMES and "_archive" not in p.parts:
                pages[p.stem] = p

    index_text = (ROOT / "index.md").read_text() if (ROOT / "index.md").exists() else ""
    inbound = {name: 0 for name in pages}

    for name, path in pages.items():
        rel = path.relative_to(ROOT)
        text = path.read_text()
        fm, body = split_frontmatter(text)
        if fm is None:
            problems.append(f"{rel}: missing frontmatter")
            continue
        for field in REQUIRED:
            if field not in fm:
                problems.append(f"{rel}: frontmatter missing '{field}'")
        tags = [t.strip() for t in fm.get("tags", "").strip("[]").split(",") if t.strip()]
        for t in tags:
            if allowed and t not in allowed:
                problems.append(f"{rel}: tag '{t}' not in SCHEMA.md taxonomy")
        links = set(LINK_RE.findall(body))
        for target in links:
            target = target.strip()
            if target in pages:
                inbound[target] += 1
            else:
                problems.append(f"{rel}: broken wikilink [[{target}]]")
        if len(links) < 2:
            warnings.append(f"{rel}: fewer than 2 outbound wikilinks")
        if f"[[{name}]]" not in index_text:
            warnings.append(f"{rel}: not listed in index.md")
        if len(text.splitlines()) > 200:
            warnings.append(f"{rel}: over 200 lines - split candidate")

    for name, n in inbound.items():
        if n == 0 and f"[[{name}]]" not in index_text:
            warnings.append(f"{pages[name].relative_to(ROOT)}: orphan (no inbound links)")

    for path in (ROOT / "raw").rglob("*.md"):
        fm, body = split_frontmatter(path.read_text())
        if fm is None or "sha256" not in fm:
            problems.append(f"{path.relative_to(ROOT)}: raw file missing sha256 frontmatter")
            continue
        recorded = fm["sha256"]
        if recorded.startswith("<"):  # untouched placeholder
            continue
        actual = hashlib.sha256(body.strip().encode("utf-8")).hexdigest()  # same as hash_raw.py
        if actual != recorded:
            problems.append(f"{path.relative_to(ROOT)}: sha256 mismatch (edited after ingest, or hash not from scripts/hash_raw.py)")

    for w in warnings:
        print("WARN ", w)
    for p in problems:
        print("ERROR", p)
    print(f"\n{len(pages)} pages checked, {len(problems)} errors, {len(warnings)} warnings")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
