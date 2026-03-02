# Patch Notes — engine-1.9.0

Date: 2026-03-02
Scope: assembled prose boundary overlays + provenance-safe edit routing (phase-1)

## Summary

This release adds assembled prose projection for any scope unit (scene/chapter/act/book)
with explicit segment provenance and safe unit-local edit routing from assembled view.

## Added

- New API endpoint:
  - `GET /v2/prose-assembled/{unitId}`
- Assembled prose response includes:
  - `assembledText`
  - `segments[]` with `unitId`, `start`, `end`, title/type, word/page stats
  - scope-level word/page totals
- Unit editor overlay mode `Unit Boundaries` now renders:
  - boundary cards per source segment
  - segment metadata (type/title/range/word/pages)
  - per-segment `Open Unit` action for provenance-safe editing.

## Changed

- Assembled prose is projection-only and read-only in boundary mode.
- Editing from assembled context routes to a single underlying unit editor
  (`Open Unit`) instead of cross-boundary direct mutation.

## Story Agent Guidance

- Use assembled boundary mode for chapter/act pacing review and provenance checks.
- Continue authoring prose canon in unit-local files (`narrative.textRef`).
- Treat assembled view as inspection/navigation, not as canonical write surface.
