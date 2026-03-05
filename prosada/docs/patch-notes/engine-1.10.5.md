# Patch Notes — engine-1.10.5

Date: 2026-03-05
Scope: soft guidance taxonomy namespace for theory/ethos units

## Summary

This release adds a lightweight, optional taxonomy layer for guidance artifacts
without expanding top-level unit types.

## Added

- Optional `unit.guidance` namespace in canonical schema:
  - `guidance.kind?: string`
  - `guidance.tags?: string[]`
- Writing/editor guidance displays now surface `guidance.kind` when present.

## Changed

- Validator adds warning-only checks for obviously bad guidance metadata shape:
  - guidance on non-theory/non-ethos units
  - blank `guidance.kind`
  - empty tag values
- Managed docs now document recommended (soft) `guidance.kind` vocabulary.
- Managed docs pack bumped to `1.10.5`.

## Story Agent Guidance

- Keep top-level `type` values (`theory`, `ethos`) stable.
- Use `guidance.kind` as the first-stop flexible classification layer.
- Treat recommended vocabulary as conventions, not hard limits.
