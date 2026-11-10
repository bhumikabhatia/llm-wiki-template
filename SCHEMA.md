# Wiki Schema

> This file is the contract between you and the agent. Edit the `[PLACEHOLDERS]`
> before ingesting anything. The tag taxonomy in particular should be tailored to
> your domain — the one below is an example of *shape*, not of content.

## Domain

[ONE PARAGRAPH: what is this wiki about, who is it for, what is it NOT for.]

Example: "Technical and product knowledge base for the <Initiative> team. Covers
architecture decisions, system landscape, APIs, team context, investigation findings,
and working decisions. Audience: engineers and PMs on the team."

## Conventions

- File names: lowercase, hyphens, no spaces (`my-system-name.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Links between pages use `[[wikilinks]]` — plain, never backticked
- Every new page needs at least 2 outbound `[[wikilinks]]`
- Bump `updated:` date whenever a page is modified
- Every new page goes into `index.md` under the correct section, alphabetically
- Every action is appended to `log.md`
- Raw sources in `raw/` are immutable after ingest — corrections go in wiki pages only

## Frontmatter

Wiki pages:

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | decision
tags: [from taxonomy below]
sources: [raw/transcripts/YYYY-MM-DD-meeting.md]
confidence: high | medium | low
---
```

Optional fields, used only when relevant (add your own, e.g. an `audience:` field, if you need them):

| Field | Meaning |
|---|---|
| `contested: true` | Claims on this page are disputed; see body |
| `contradictions: [other-page]` | Pages that disagree with this one |

Raw sources (in `raw/`) use a different frontmatter:

```yaml
---
source_url: <url, or a description if there is none>
ingested: YYYY-MM-DD
sha256: <hash of the body only, not the frontmatter>
---
```

## Tag Taxonomy

**The taxonomy is closed.** Add a tag here *before* using it on a page. This is what
stops the wiki drifting into 400 near-duplicate tags.

Group tags by what they describe. Suggested groups (rename freely):

Domain — the business / product areas:
- `[domain-tag-1]` — [what it covers]
- `[domain-tag-2]` — [what it covers]

System / API — the technical components:
- `[system-tag-1]` — [what it covers]
- `[system-tag-2]` — [what it covers]

People / Org — what kind of entity a page describes:
- `person` — individual team member or stakeholder
- `team` — team or org unit
- `project` — project or initiative
- `system` — a deployed service or system entity

Meta — what kind of knowledge a page holds:
- `compliance` — regulatory or legal topics
- `decision` — architectural or product decision
- `investigation` — ongoing investigation or root-cause analysis
- `blocker` — active blocker
- `meeting` — meeting notes reference

Rule: add new tags here before using them on pages.

## Page Thresholds

- **Create** when an entity/concept appears in 2+ sources or is central to one source
- **Update** when a source mentions something already covered
- **Skip** for passing mentions
- **Split** pages over ~200 lines into sub-topics with cross-links
- **Archive** fully superseded content → move to `_archive/`

## Update Policy

When new info conflicts with existing content:
1. Newer source generally wins
2. Genuine contradiction → note both with dates and sources, set `contradictions: [other-page]`
3. Flag for team review

## Confidence Levels

- `high` — corroborated by 2+ independent sources, or a primary source (the spec, the code)
- `medium` — single source, or opinion-heavy
- `low` — inferred, second-hand, or possibly out of date. Pair with `contested: true` if disputed
