---
title: System Name
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity
tags: [system]
sources: [raw/articles/YYYY-MM-DD-design-doc.md]
confidence: medium
---

# System Name

One or two sentences: what it is, who owns it ([[team-name]]), and what it is for.

## Role in the landscape

What calls it, what it calls, what data it owns. A small ASCII or Mermaid diagram helps:

```
upstream-system → THIS SYSTEM → downstream-system
```

## Interfaces

| Interface | Direction | Consumers / producers | Notes |
|---|---|---|---|
| `GET /example` | in | [[other-system]] | |

## Constraints and gotchas

Things that surprised someone. Latency limits, ownership boundaries, known incidents.
Each with a date and a source.

## Open questions

- [ ] Question nobody has answered yet — and who might know.
