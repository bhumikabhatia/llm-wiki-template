# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this repository is

A **Karpathy-style LLM wiki** for **[TEAM / PROJECT NAME]**. The wiki holds
**synthesis**. Raw sources go in `raw/` and are immutable after ingest.

**Read `AGENTS.md` before doing any work in this repo.** It is the complete operating
manual (ingest, query, lint, hard rules). This file is only a pointer plus a cheat sheet,
so the rules live in exactly one place.

## Repository structure

```
raw/                   Immutable source material (never edit after ingest)
  transcripts/         Meeting notes, interview notes
  articles/            Specs, design docs, external references
  assets/              Images and diagrams

entities/              One page per notable entity
  people/  projects/  systems/  teams/

concepts/              Architecture concepts, APIs, patterns
comparisons/           Side-by-side analyses and trade-offs
queries/               Filed investigations and answered questions
decisions/             Architectural and product decisions (ADRs)
templates/             Copy-paste page skeletons (ADR skeleton: decisions/adr-template.md)

SCHEMA.md              Conventions, tag taxonomy, page rules
index.md               Full catalog — start here
log.md                 Append-only action history
AGENTS.md              Operating manual (mandatory reading)
```

## Before any write

Read, in order: `SCHEMA.md` → `index.md` → last 20–30 entries of `log.md`.

## Hard rules (summary — full text in AGENTS.md)

1. `raw/` is immutable.
2. Every page has frontmatter, is listed in `index.md`, and every action is in `log.md`.
3. The tag taxonomy is closed — add to `SCHEMA.md` first.
4. Bump `updated:` when the body changes.
5. At least 2 outbound `[[wikilinks]]` per page.
6. Do not invent facts; use `confidence: low` / `contested: true`.

## Git workflow

Commit after each significant operation, `<verb>: <subject>`:

```
ingest: 2026-01-15 weekly sync notes
update: payments-service with retry behaviour
lint: fix broken wikilinks and stale dates
```
