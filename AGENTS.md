# AGENTS.md

Operating manual for any AI agent (Claude, Codex, Cursor, etc.) working in this wiki.
Read it before doing anything.

## What this repository is

A Karpathy-style LLM wiki for **[TEAM / PROJECT NAME]**.
It is the canonical shared knowledge base for this team — [architecture, systems,
decisions, investigations, working context — edit to fit].

The wiki holds synthesis. Raw sources go in `raw/` and are immutable after ingest.
Do not maintain a second copy of this content elsewhere.

---

## Hard rules

1. **`raw/` is immutable.** Source material is never edited after ingest. Corrections go
   in wiki pages only. If a raw source has changed, ingest a new file with a date suffix
   and link both.

2. **Every page has frontmatter, every page is in `index.md`, every action is in
   `log.md`.** No exceptions. These are the wiki's spine.

3. **Tag taxonomy is closed.** New tags get added to `SCHEMA.md` first. No freeform tags.

4. **Bump `updated:` whenever the body changes.**

5. **Cross-link aggressively.** Minimum 2 outbound `[[wikilinks]]` per page.
   Bare `[[wikilinks]]` are for passing mentions only — use them semantically.

6. **Do not invent facts.** Mark `confidence: low` and `contested: true` rather than
   asserting uncertain claims.

7. **Do not skip `log.md`.** A wiki without a log decays fast.

---

## 1. Orientation (mandatory before any write)

Always do these reads first:

1. `SCHEMA.md` — conventions, tag taxonomy, page thresholds.
2. `index.md` — what already exists; avoid duplicates.
3. Tail of `log.md` (last 20–30 entries) — recent activity.

For wikis past ~50 pages, also run a content search before creating anything:

```bash
grep -ril "<entity or concept>" . --include="*.md" | grep -v -e .obsidian -e .git/
```

Skipping orientation causes duplicate pages and schema drift.

---

## 2. The three layers (do not blur them)

```
raw/                  Immutable source material. Read, never edit after ingest.
                      Subfolders: transcripts/, articles/, assets/
                      Frontmatter: source_url, ingested, sha256 (of body only)

entities/             Agent-owned wiki pages for people, projects, systems, teams
concepts/             Architecture concepts, APIs, patterns
comparisons/          Side-by-side analyses and trade-offs
queries/              Filed investigations and answered questions
decisions/            ADRs and other recorded decisions (adr-template.md is the skeleton)

SCHEMA.md             Tag taxonomy, conventions, page thresholds
index.md              Full catalog — every wiki page, one-line summary
log.md                Append-only action history
```

The cardinal rule: never paste raw content directly into wiki pages. A meeting
transcript goes into `raw/transcripts/`. The agent then extracts entities,
decisions, and action items into the relevant pages. Do not turn wiki pages
into raw dumps.

Page templates live in `templates/` (the ADR template is `decisions/adr-template.md`).
Copy one rather than writing frontmatter from memory.

---

## 3. Ingest

Trigger: new source arrives (meeting notes, doc, spec, paste).

1. Save to `raw/<subdir>/YYYY-MM-DD-<slug>.md` with raw frontmatter:
   `source_url`, `ingested`, `sha256` (of body only, not frontmatter).
   Compute the hash with `python3 scripts/hash_raw.py <file>` - never produce it yourself;
   LLMs cannot compute SHA-256 and will fabricate one.
   On re-ingest: skip if sha256 matches, flag drift if changed.
2. Search `index.md` and grep for entities the source mentions.
   Update existing pages instead of creating duplicates.
3. Create or update wiki pages. A single source typically touches 3–10 pages.
   For each touched page:
   - Add the raw path to `sources:` frontmatter.
   - Append a dated synthesis section.
   - Cross-reference ≥2 other pages via `[[wikilinks]]`.
   - Bump `updated:`.
4. Provenance: on pages synthesizing 3+ sources, append `^[raw/<path>.md]`
   after paragraphs tracing to a specific source.
5. Confidence: `medium` or `low` for opinion-heavy or single-source claims.
   Do not mark `high` without corroboration.
6. Update `index.md`: insert new pages alphabetically under the correct section,
   bump page count, update "Last updated".
7. Append to `log.md`: `## [YYYY-MM-DD] ingest | <subject>` listing every
   file created or updated.
8. If ingest would touch 10+ existing pages, confirm scope with the user first.

---

## 4. Query

Trigger: user asks a question whose answer should come from the wiki.

1. Read `index.md` to identify candidate pages.
2. Grep for key terms — index alone misses things.
3. Read candidate pages. Do not bulk-cat the vault.
4. Synthesize the answer, citing pages with `[[wikilinks]]`.
5. File valuable answers back: substantial syntheses or novel comparisons become
   pages in `queries/` or `comparisons/`. Skip trivial lookups.
   Heuristic: if re-deriving the answer would take ≥10 minutes, file it.
6. Append to `log.md`: `## [YYYY-MM-DD] query | <subject>`.

---

## 5. Lint

Trigger: user asks to lint, or periodic health check.

Check in order of severity:

1. Broken wikilinks — `[[links]]` pointing to pages that don't exist.
2. Orphan pages — wiki pages with zero inbound wikilinks.
3. Index completeness — every wiki page must appear in `index.md`.
4. Frontmatter validation — required fields present; tags in SCHEMA taxonomy.
5. Source drift — recompute sha256 for raw files; mismatch = investigate.
6. Contested pages — surface `contested: true` or `contradictions: [...]` for review.
7. Confidence gaps — list `confidence: low` and single-source pages.
8. Stale content — pages with `updated:` >90 days older than latest related source.
9. Page size — flag pages over 200 lines as split candidates.
10. Tag audit — list all tags in use; flag any not in SCHEMA taxonomy.
11. Log rotation — if `log.md` exceeds 500 entries, rename to `log-YYYY.md` and restart.

Group findings by severity. Report file paths and suggested actions.
Append to `log.md`: `## [YYYY-MM-DD] lint | N issues found`.

---

## 6. Page thresholds

- **Create**: entity/concept appears in 2+ sources or is central to one source.
- **Update**: source mentions something already covered.
- **Skip**: passing mentions.
- **Split**: pages over ~200 lines.
- **Archive**: fully superseded content → move to `_archive/`.

---

## 7. What NOT to do

- Don't create pages for passing mentions.
- Don't create empty stubs.
- Don't paste raw content into wiki pages — that belongs in `raw/`.
- Don't silently overwrite contradictions — note both with dates, set `contradictions:`.
- Don't invent tags — add to SCHEMA first.
- Don't skip `index.md` or `log.md` updates.
- Don't modify source repositories — this wiki stores conclusions, not code.
- Don't make outbound communications, calendar changes, or external API calls
  without explicit user approval.

---

## 8. Confidentiality

[EDIT THIS SECTION. It is the one most likely to hurt you if left generic.]

- Who can read this repository? [e.g. "everyone in the company", "this team only", "public"]
- What must never be written into a wiki page? [e.g. third-party NDA content, customer
  data, credentials, personal data beyond names and roles]
- Who may add raw sources, and what do they need to check first?

Raw transcripts frequently contain things people said in confidence. Review before
ingesting; the immutability rule means a mistake in `raw/` is awkward to undo.

---

## 9. Environment

- Wiki root: `[PATH]`
- Git repo. Commit after each significant operation:
  `git commit -m "<verb>: <subject>"`
- Search: grep / ripgrep for content scans; never bulk-cat the vault.
- Bulk operations (lint, frontmatter edits): write a script rather than shell loops.

---

## Quick reference

```
ingest  → raw/<subdir>/slug.md  →  update wiki pages  →  index.md  →  log.md  →  commit
query   → index + search + read  →  answer with [[citations]]  →  file if substantial
lint    → links → orphans → index → frontmatter → drift → stale → size → tags  →  log.md
```
