# ProSada Usage Primer

## Purpose

`/prosada/` is the primary intent engine for this repository.
Use it to outline, structure, and evolve the story at any resolution:

- book-level architecture
- act/chapter/scene/beat decomposition
- page-level drafting intent linked to prose

This repository is story-only. There is no separate application/content split here.

## Canonical Source of Truth

- Structural canon: `prosada/units/*.json`
- Story bible entities: `prosada/registries/*.json`
- Draft prose: markdown files referenced by `narrative.textRef`

Rule: prose expresses the story; ProSada defines the structure and intent.

## Recommended Workflow

1. Plan or revise structure in ProSada units.
2. Update entities/threads in registries.
3. Link or create prose targets via `narrative.textRef`.
4. Draft and revise prose from the unit intent model.
5. Validate unit relationships and semantic references.

## Editing Guardrails

- Keep `unitId` stable; do not rename casually.
- Keep `parentId` and `children[]` consistent.
- Treat `view.*` as layout/UI hints, not narrative canon.
- Use semantic refs where useful: `VisibleText[[kind:entity-id]]`.

## Operational References

- `prosada/docs/AGENT_START_HERE.md`
- `prosada/docs/FORMAT_CHEATSHEET.md`
- `prosada/docs/WORKFLOWS.md`
- `prosada/docs/TOOLING.md`

## Prose Wiring Convention

To keep prose authoring predictable and provenance-safe, use this default protocol:

1. Every authored scene/chapter unit should set `narrative.textRef`.
2. Store prose files under `chapters/<chapter-folder>/`.
3. Use filename = unitId + `.md` (for example `scene-02-drive-anomaly.md`).
4. Keep `textRef` relative from `prosada/units/*.json` to the prose file.

Current path pattern:
- `../../chapters/<chapter-folder>/<unit-id>.md`

When creating a new scene unit, create its prose file immediately and wire `textRef` in the same change.
