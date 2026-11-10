---
name: sync-wiki
description: Use after a pull request is opened or merged, or whenever the wiki may be stale relative to live PRs, tickets or tracked repos. Fetches current state, updates every wiki page that references it, and opens a wiki PR if anything changed.
---

# Sync Wiki

## Overview

Fetch live PR/ticket state from GitHub (and optionally your ticket tracker), update all
interlinked wiki pages that reference those PRs, then commit, push and open a **wiki PR**.
This is how the wiki learns what shipped, so it stays accurate without manual cross-referencing.

The Orchestrator runs this right after it opens a feature PR. It can also be run on demand.

## When to use

- A feature PR was just opened (pipeline stage "Sync the wiki")
- Someone asks "is the wiki up to date?"
- You notice stale status markers that may have changed
- After a sprint or milestone where several PRs were merged

## Steps

### 1. Identify tracked PRs / tickets

Collect every PR number and repo the relevant wiki pages mention (the ADR, the architecture
pages for the changed service, any intake or change-table page). Include the PR the
Orchestrator just opened.

```bash
grep -r "PR #\|pull/" <wiki-dir> --include="*.md" | grep -v ".git/"
```

### 2. Fetch live status with `gh`

```bash
gh pr view <NUMBER> --repo <org>/<repo> --json state,title,mergedAt
```

State values: `OPEN`, `MERGED`, `CLOSED`. Use one marker convention everywhere:

| State | Marker | Label |
|---|---|---|
| Open, no approvals | 🔄 | under review |
| Open, approved | 🟡 | approved, pending merge |
| Merged | ✅ | merged |
| Closed without merge | ❌ | closed |

### 3. Update all interlinked wiki pages

For each stale status, update **every page that references that PR** — not just one.

- The ADR itself (`decisions/`): set status, add the PR link
- Entity/concept pages for the changed service: record what changed and link the ADR
- `index.md`: add the entry if the ADR is missing
- Bump `updated:` on every touched page
- Do not paste raw material into wiki pages; follow `AGENTS.md`

### 4. Decide whether there is anything to open

If no page needs a change, stop and report "no wiki changes needed". Do not open an empty PR.

### 5. Append to `log.md`

```
## [YYYY-MM-DD] update | <subject>

Sources: GitHub PR state (gh cli)

Changes:
- <file>: <what changed and why>
```

### 6. Commit, push, open the wiki PR

```bash
git checkout -b update/<slug>
git add <changed files>
git commit -m "update: <subject>"
git push -u origin update/<slug>
gh pr create --title "update: <subject>" --body "..."
```

Never force-push. Never merge the wiki PR yourself; a human reviews it.

## Common mistakes

- Updating only the ADR but not the architecture page for the service (or vice versa) — grep for every file referencing the PR
- Marking a PR ✅ in one page and 🔄 in another — sync all occurrences
- Forgetting to bump `updated:`
- Forgetting to add a missing ADR to `index.md`
- Opening an empty wiki PR when nothing changed
