# Adapting this template to your own case

## What to tailor, what to leave alone

| Tailor to your domain | Leave alone unless you have a reason |
|---|---|
| `SCHEMA.md` Domain paragraph | The three-layer split (raw / wiki / schema) |
| `SCHEMA.md` tag taxonomy | The closed-taxonomy rule |
| `AGENTS.md` confidentiality section | Raw immutability + sha256 |
| Folder names under `entities/` | Frontmatter required fields |
| Which templates you actually use | `index.md` + `log.md` as mandatory spine |

## Step 1: write the Domain paragraph

One paragraph in `SCHEMA.md`: what the wiki covers, who reads it, what it is *not* for.
The agent uses this to decide what is worth a page. Vague domain, vague wiki.

## Step 2: design the tag taxonomy

This is the highest-leverage edit. Tags are how you filter later, and the agent will
invent near-duplicates if you let it, so the taxonomy is **closed**.

Group tags into four buckets (the template's grouping):

1. **Domain**: the business or product areas (e.g. `checkout`, `payments`, `onboarding`).
2. **System / API**: the technical components people name in meetings.
3. **People / Org**: what kind of entity the page is (`person`, `team`, `project`, `system`). Keep these as-is.
4. **Meta**: what kind of knowledge it is (`decision`, `investigation`, `blocker`, `meeting`, `compliance`). Keep these too.

Start small (10–20 tags). Adding a tag is cheap; merging 400 is not. Every tag needs a
one-line meaning so the agent can choose between neighbours.

## Step 3: decide confidentiality *before* the first ingest

Edit `AGENTS.md` section 8. Answer: who can read this repo, and what must never go in it.
Raw files are immutable by rule, so a mistake in `raw/` is awkward to undo.

## Step 4: pick your entity folders

The template ships `people/ projects/ systems/ teams/`. Drop what you will not use
(an empty folder invites empty stub pages) and add what you need, such as `customers/`
or `vendors/`. Update the structure listing in `AGENTS.md`, `CLAUDE.md` and `README.md`,
and the `lint.py` `WIKI_DIRS` list, if you change them.

## Step 5: run a first ingest by hand

Pick one real, low-risk source, such as a meeting transcript.

1. Copy `templates/raw-transcript.md` to `raw/transcripts/YYYY-MM-DD-slug.md` and paste the content.
2. Run `python3 scripts/hash_raw.py raw/transcripts/YYYY-MM-DD-slug.md` to fill in `sha256`. Never ask the LLM for the hash: models cannot compute SHA-256 and will invent one.
3. Tell the agent: *"Read AGENTS.md. Ingest that file."*
4. Read what it wrote. Fix the rules in `AGENTS.md` where it did the wrong thing, rather than just correcting the pages.

Doing this once teaches you which rules your agent follows and which need to be more explicit.

## Step 6: make it a habit

- Ingest after the meeting, not at the end of the quarter.
- File good answers back as `queries/` pages. This is where the wiki compounds.
- Run `python3 scripts/lint.py` regularly, and have the agent do the judgement-based
  checks (stale content, contradictions) in `AGENTS.md` section 5.

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Duplicate pages for the same thing | Agent skipped orientation | Make "read SCHEMA, index, log tail first" non-negotiable in AGENTS.md |
| Tags multiply | Taxonomy not enforced | Run lint; reject pages with unknown tags |
| Pages become raw dumps | Synthesis rule ignored | Re-state "never paste raw content into wiki pages" and check on review |
| Confident wrong claims | Single-source facts marked `high` | Enforce the confidence rules; use `contested: true` |
| `index.md` rots | Forgot to update on create | Lint reports pages missing from the index |
| Log is empty | Agent skips it | Treat a missing log entry as a failed operation |

## Scaling notes

- Past ~50 pages, the index alone is not enough; the agent must also grep before creating.
- Past ~500 log entries, rotate to `log-YYYY.md`.
- Pages over ~200 lines should be split into sub-topics with cross-links.
- At very large scale, consider adding a search tool (embedding or full-text) on top; the
  markdown stays the source of truth.
