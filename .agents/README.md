# Agent pipeline

Five specialist agents and an orchestrator that run a feature from ticket to pull request,
using the wiki in this repository as shared memory. Written for [opencode](https://opencode.ai);
the prompts are plain Markdown and port to any agent tool that supports subagents.

## How the workflow runs

The orchestrator hands each agent its input and asks the human for a **yes** at every gate.
Agents never talk to each other.

| # | Input | Agent | Output | Talks to |
|---|---|---|---|---|
| 1 | ticket | **PM** (what & why) | product brief | ticket tracker *(optional)* |
| 2 | brief + relevant wiki pages | **Architect** (picks the approach) | ADR in `decisions/` | service catalog, docs search, ticket tracker, logs & traces *(all optional)* |
| 3 | ADR + repos | **Developer** (plans, then codes) | `tasks.md`, then code | git repos, build & tests |
| 4 | changed files | **Tester** (tests behaviour) | tests + coverage | git repos, build & tests |
| 5 | branch + spec (the ADR) | **Reviewer** (build + review) | findings + verdict | git repos, build & tests, GitHub, a second model from another vendor |
| 6 | final yes | **Orchestrator** | opens the PR | git, GitHub |
| 7 | the new PR | **`sync-wiki` skill** | opens a wiki PR if the wiki needs changes | git, GitHub |

```
ticket -> PM -> yes -> Architect -> yes -> Developer -> yes -> Tester -> yes -> Reviewer -> yes
                          |                                                       |
                      writes ADR                                              ADR = spec
                          \_____________________ wiki (git) ____________________/
                                                    ^
        orchestrator opens the PR on the final yes, then runs sync-wiki  (feedback into the wiki)
```

Two ideas carry the design:

- **The ADR is the contract.** The Architect writes it, the Developer builds to it, and the
  Reviewer checks the code against it.
- **The wiki is the memory.** Agents read it before working, and the pipeline writes back to
  it at the end, so the next feature starts from what this one learned.

Each agent only gets the systems its job needs. The PM, Tester and second reviewers have no
network or catalog access; only the Reviewer and Orchestrator touch GitHub.

## Files

```
.agents/
  orchestrator.md            Drives the stages, enforces gates, opens the PR, triggers wiki sync
  pm.md                      Brief from a requirement
  architect.md               ADR from a brief
  developer.md               tasks.md, then code (invoked twice: plan, implement)
  tester.md                  Tests + coverage
  reviewer.md                Build verification + review; calls the second reviewer
  second-reviewer.md         Independent reviewer on a different vendor's model
  skills/sync-wiki/SKILL.md  Updates the wiki after a PR and opens a wiki PR
opencode.jsonc               Registers the agents and their permissions (repo root)
```

## Setup

1. Copy `.agents/` and `opencode.jsonc` into the root of your wiki repository, next to
   `SCHEMA.md` and `AGENTS.md`. The agents read the wiki from the directory they run in.
2. In `opencode.jsonc`, replace the two `REPLACE_WITH_...` model placeholders with models
   from a **different vendor** than the one running your main agents. That independence is
   what the second review is for. Optionally pin models for the other agents too.
3. Make the optional integrations available if you have them (service catalog, docs search,
   ticket tracker, logs). The prompts say what to do when one is missing.
4. Service code lives in separate repositories. The Architect lists them in the ADR's
   "Affected Repositories" table and the orchestrator clones and branches them.
5. Start the `orchestrator` agent and describe the requirement.

## Things you will want to change

- **Coverage target** (80%) and the **complexity rule** that selects the heavy or light
  second reviewer: both are in `orchestrator.md`.
- **Branch and commit naming**: `<ticket-id>-<slug>` in `orchestrator.md`.
- **Permissions**: the orchestrator may run shell (it needs git and `gh`) but cannot edit
  files. Tighten or loosen per agent in `opencode.jsonc`.
- **The config syntax**: `opencode.jsonc` uses the `permission` / `bash` / `task` field names.
  Newer opencode releases are moving to `permissions` / `shell` / `subagent`; see
  <https://opencode.ai/docs/permissions/> if yours rejects it.

## Safety properties worth keeping

- Nothing is committed to the wiki, pushed, or opened as a PR without an explicit human yes.
- Nothing force-pushes or merges.
- The Developer does not write tests and the Tester does not touch application code, so
  tests cannot be bent to fit a bug.
- Findings from the second reviewer must quote the source; the first reviewer verifies any
  `BLOCKING` claim before accepting it.
