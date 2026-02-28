# Story Repository Guide: The Content

Welcome to the **Story Universe** of Prose Ada. This directory is the creative core of the project. If you are here, your role is that of a co-author, editor, or creative strategist.

## The North Star: Quality Standards

All work performed within this directory must adhere to the **[Quality Standard Imperative](docs/quality-standards.md)**.

> [!IMPORTANT]
> This is a no-compromise project. We do not settle for "pretty good." Every scene, character, and sentence must justify its existence and contribute to a coherent, integrated whole.

## Creative Philosophy: The Ethos Docs

Before contributing any creative writing or structural changes, you MUST internalize our core ethos:

1.  **[Writing Style Ethos](docs/ethos/writing-style-ethos.md)**: Our voice, tone, and linguistic precision.
2.  **[Plot & Structure Ethos](docs/ethos/plot-structure-ethos.md)**: How we build tension, propulsion, and inevitability.
3.  **[Beauty Ethos](docs/ethos/beauty-ethos.md)**: The aesthetic and emotional resonance we strive for.

## Session-Start Requirement

At the start of **every** working session, agents must:

1. Re-read `docs/quality-standards.md`.
2. Re-read all ethos docs in `docs/ethos/`.
3. Use those standards as explicit decision criteria for outlining, drafting, revision, and structural edits.

If a proposed change conflicts with these standards, revise or reject the change until it aligns.

## Directory Structure

- **`/chapters`**: Current drafts and manuscripts.
- **`/vision` & `/big-picture`**: Strategic alignment and high-level story goals.
- **`/references`**: Historical and mythological research foundations.
- **`/docs/`**: Root documentation, ethos, and working primers.
- **`/prosada/`**: Canonical story intent engine workspace (JSON units + registries).

## ProSada Intent Engine (Primary Workflow)

`/prosada/` is the main planning and story-construction engine for this repository.
It is where we outline, structure, and evolve the book at every resolution:
high-level architecture, act/chapter/scene decomposition, and page-level drafting intent.

Repository scope note:
- This repository is story-only.
- There is no separate application folder or app/content split in this repo.
- ProSada is the primary structuring and development tool used to grow the book.

Working rule:
- Structural truth lives in `prosada/units/*.json` and `prosada/registries/*.json`.
- Markdown prose files are authored outputs linked from units (for example via `narrative.textRef`), not the structural source of truth.

When working on story development, prefer this order:
1. Shape intent and structure in `/prosada/`.
2. Validate coherence and dependencies (parents/children, refs, streams).
3. Draft or revise prose from that intent model in `/chapters/` and related markdown files.

Start here for ProSada operating details:
- `prosada/docs/AGENT_START_HERE.md`
- `prosada/docs/WORKFLOWS.md`
- `prosada/docs/FORMAT_CHEATSHEET.md`
- `prosada/docs/TOOLING.md`

## Operating Rules for Agents

- **Ruthless Revision**: Drafting is for discovery; the final artifact must be precise.
- **No Fillers**: If a section doesn't meet the bar, cut it or rewrite it. Do not excuse it.
- **Earned Emotionality**: Every emotion invoked must be earned through setup and structure.
- **Precision over Complexity**: Choose the right amount of detail, not the maximum amount.

---
*This guide ensures that the engine serves the story, and the story lives up to its own promise.*
