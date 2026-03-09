# Patch Notes — engine-1.12.1

Date: 2026-03-09
Scope: inline prose lock marker protocol + lock overlay reliability

## Summary

This release formalizes lock directives as prose-local inline markers and
clarifies that lock overlays are derived from marker state, not detached offset
records.

## Added / Clarified

- Inline lock marker protocol:
  - `[[[lock|KEEP|<lockId>|start]]] ... [[[lock|KEEP|<lockId>|end]]]`
  - same wrapper form for `SOFT_KEEP`, `REWRITE`, `EXPLORE`
- Prose lock handling expectation:
  - UI assignment/reassignment/clear operations mutate inline markers.
  - lock overlay spans are derived from marker-bearing prose content.
- Reader-surface scrubbing expectation:
  - marker tokens are authoring metadata and should be removed from
    prose-view/TTS/export outputs.

## Story Agent Guidance

- Treat lock directives as local prose boundaries, not detached index-only data.
- When lock state changes, preserve marker integrity (`start`/`end` pairs).
- Do not author custom lock syntax variants outside this protocol.

## Compatibility Notes

- No canonical schema migration required.
- Existing prose overlay endpoints remain supported; lock span payloads are
  derived from marker state during app workflows.
