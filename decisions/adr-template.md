---
title: ADR Template
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: decision
tags: [decision]
sources: []
confidence: medium
---

# ADR: Decision Title

**Author:** [[person-name]]
**Date:** YYYY-MM-DD
**Status:** draft | in review | accepted | rejected | superseded by [[other-adr]]

## Context

The problem and the pressures behind it: constraints, deadlines, who is affected.

## Options considered

1. **Option A** — summary, main trade-off
2. **Option B** — summary, main trade-off

## Decision

What was decided, in one or two sentences.

## Solution

The chosen approach in detail: key design choices, how it addresses the context,
trade-offs accepted.

## Consequences

What gets easier, what gets harder, what is now owed (follow-up work, tech debt).

## Related decisions

- [[related-adr]] — how it relates

---

## How to use this template

1. Copy this file to `decisions/adr-<short-slug>.md` (this template itself is skipped by the
   linter and is not listed in `index.md`).
2. Replace the frontmatter placeholders and every bracketed or placeholder section.
3. Start with `Status: draft`; update it as the decision moves through review.
4. Link related decisions with `[[wikilinks]]`. If an ADR supersedes another, set the old
   one's status to `superseded by [[new-adr]]` rather than deleting it.
5. Add the ADR to `index.md` under Decisions and append to `log.md`.
6. Bump `updated:` whenever you modify it.
