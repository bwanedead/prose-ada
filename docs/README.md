# Prose Ada Root Docs Primer

This `docs/` folder contains the operating standards and creative intent for the book.
Use it together with `/prosada/`, which is the primary intent engine for story construction.
This repository is story-only and uses ProSada as the primary structuring/development tool.

## What ProSada Is For

`/prosada/` is the canonical structured workspace for building the story at any resolution:
- high-level story architecture (book, acts, sequences, chapters)
- scene and beat-level intent
- prose-linked drafting flow (page-by-page writing guided by unit intent)

In short: we design and evolve structure in ProSada, then draft prose from that structure.

## Canonical Workflow

1. Define or revise narrative structure in `prosada/units/*.json`.
2. Maintain shared story entities in `prosada/registries/*.json`.
3. Keep prose linked via `narrative.textRef` and draft in markdown files.
4. Validate integrity and refs before major writing passes.

## Read These First

- `docs/quality-standards.md`
- `docs/prosada-usage.md`
- `docs/ethos/writing-style-ethos.md`
- `docs/ethos/plot-structure-ethos.md`
- `docs/ethos/beauty-ethos.md`
- `prosada/docs/AGENT_START_HERE.md`
- `prosada/docs/WORKFLOWS.md`
