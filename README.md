# LLM Wiki Template

A content-free skeleton of an **LLM wiki**, based on
[Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f):
a knowledge base that an AI agent builds and maintains for you, where knowledge is compiled
once, kept current and cross-referenced, instead of being rediscovered from scratch every
time someone asks.

The idea and the core pattern are Karpathy's. This repository adds a practical working
setup on top of it: a folder layout, a schema with a closed tag taxonomy, an operating
manual for the agent, page templates and a small lint script, so you can apply it to your
own case.

## The idea in 30 seconds

```
 raw sources                 the agent                      the wiki
 (transcripts, docs)  ──►  reads, extracts, links  ──►  synthesis pages with
 immutable                 follows AGENTS.md              frontmatter + [[wikilinks]]
                                                                │
                                          questions ◄───────────┘
                                          answered from the wiki, good answers filed back
```

Three layers, never blurred:

| Layer | Where | Rule |
|---|---|---|
| Raw | `raw/` | Immutable after ingest. Source of truth for *what was said*. |
| Wiki | `entities/ concepts/ comparisons/ queries/ decisions/` | Agent-maintained synthesis. Source of truth for *what we currently believe*. |
| Schema | `SCHEMA.md`, `AGENTS.md`, `index.md`, `log.md` | The contract, the catalog and the history. |

## Structure

```
raw/                   Immutable source material
  transcripts/         Meeting notes, interviews
  articles/            Specs, design docs, external references
  assets/              Images and diagrams

entities/              One page per notable thing
  people/ projects/ systems/ teams/
concepts/              Architecture concepts, APIs, patterns
comparisons/           Side-by-side analyses and trade-offs
queries/               Filed investigations and answered questions
decisions/             ADRs (adr-template.md is the ADR skeleton)

templates/             Page skeletons for entities, concepts, comparisons, queries, raw sources
scripts/lint.py        Mechanical health check (links, tags, index, hashes)
scripts/hash_raw.py    Computes the sha256 for raw files (LLMs cannot do this reliably)

.agents/               Agent pipeline (PM -> Architect -> Developer -> Tester -> Reviewer)
opencode.jsonc         Registers the agents for opencode
docs/                  How to adapt this to your own case

SCHEMA.md              Conventions, frontmatter, closed tag taxonomy, page thresholds
AGENTS.md              Operating manual for the agent: ingest / query / lint
CLAUDE.md              Thin pointer to AGENTS.md for Claude Code
index.md               Full catalog. The agent reads this first.
log.md                 Append-only history of every action
```

## Quick start

1. **Use this template** (green button on GitHub) or clone it.
2. Fill in the `[PLACEHOLDERS]`. Do these first, in this order:
   - `SCHEMA.md`: the Domain paragraph and the tag taxonomy.
   - `AGENTS.md`: section 8 (Confidentiality) and section 9 (Environment).
   - `CLAUDE.md` / `AGENTS.md`: the team/project name.
3. Open the folder in your agent (Claude Code, Codex, Cursor, ...) and say
   *"Read AGENTS.md, then ingest `raw/transcripts/<file>`."*
4. Check the result with `python3 scripts/lint.py`.

The step-by-step version, including what to tailor and what to leave alone, is in
[docs/adapting-this-template.md](docs/adapting-this-template.md).

## Agent pipeline (optional)

`.agents/` holds a set of agent prompts that use the wiki as shared memory: a PM, Architect,
Developer, Tester and Reviewer run in sequence under an orchestrator, with a human approval
gate between every stage, and the wiki is updated when the pull request opens. See
[.agents/README.md](.agents/README.md).

## The four operations

- **Ingest**: new source → saved in `raw/` with a hash → agent updates 3–10 wiki pages → `index.md` → `log.md`.
- **Query**: agent reads `index.md`, greps, reads candidates, answers with `[[citations]]`, and files substantial answers back as `queries/` pages.
- **Lint**: broken links, orphans, index gaps, tags outside the taxonomy, hash drift, stale or oversized pages.
- **Log**: every action recorded. A wiki without a log decays.

## Works as an Obsidian vault

Open the directory in [Obsidian](https://obsidian.md) for graph view, backlinks and
wikilink navigation. `.obsidian/graph.json` colours the graph by folder.

## Before you put real content in

Raw transcripts contain things people said in confidence. Decide who can read the repo
and what must never be written into it **before** the first ingest, and write it down in
`AGENTS.md` section 8. Keep a repo with real content private unless it is cleared for
publication.

## License

MIT. See [LICENSE](LICENSE).
