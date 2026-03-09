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

## Guidance Stack Definition

For this repository, a **guidance stack** means the canonical story guidance document stack that applies to the current scope of concern.

In practice, this includes:

1. `docs/quality-standards.md`
2. all story-wide ethos docs in `docs/ethos/`
3. the canonical readable docs linked from applicable `theory` / `ethos` guidance artifacts in `prosada/`
4. inherited higher-scope story guidance that governs the current unit or prose scope

Working rule:
- Do not treat only the immediate unit brief as the full guidance stack.
- When asking for the guidance stack for a unit, prefer the canonical readable document corpus rather than structural wrappers.
- In ProsAda terms, guidance-doc stack resolution is derived at read-time, not persisted as separate story data.
- Story-wide ethos and higher-scope guidance remain part of evaluation unless a lower-scope instruction legitimately refines them without contradicting them.
- The story guidance stack excludes governed story units and excludes operational engine/repo docs.

Engine protocol alignment:
- Use attached `theory` / `ethos` artifacts in `prosada/` as the structural attachment layer for guidance.
- Treat ancestor-attached artifacts as inherited guidance.
- Treat directly attached artifacts as local guidance.
- Use `GET /v2/guidance-doc-stack/<unitId>` as the authoritative discovery mechanism for a story-agent reading stack.
- Use `GET /v2/guidance-stack/<unitId>` only when structural governance/provenance details are specifically needed.

When mentioning guidance documents from a resolved guidance stack:
- Include the guidance type explicitly.
- Prefer this format: `Document Name — artifact type / guidance kind / applicability`.
- Example: `Scene 1 Prose Brief — theory / prose_brief / local_only`.
- If `guidance.kind` is unavailable, still report `artifact type`.

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
