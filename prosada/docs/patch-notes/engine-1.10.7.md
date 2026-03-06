# Patch Notes — engine-1.10.7

Date: 2026-03-06
Scope: explicit prose beat-boundary bookend semantics

## Summary

This update formalizes beat markers in prose as explicit start/end bookends so
sub-scene boundaries are unambiguous for agents and tools.

## Changed

- Recommended marker contract now uses explicit boundaries:
  - `[[[beat-id|Beat Name|start]]]`
  - `[[[beat-id|Beat Name|end]]]`
- Parser compatibility guidance:
  - markers without boundary suffix are treated as legacy point markers
  - new bookend syntax is preferred for deterministic range parsing
- Managed docs pack bumped to `1.10.7`.

## Story Agent Guidance

- For new beat annotations, always write paired `start` + `end` markers with
  the same beat ID.
- Keep existing legacy markers only as transitional data; migrate when touched.
