# Patch Notes — engine-1.8.0

Date: 2026-03-02
Scope: prose overlay artifacts (locks/variants/merge requests) + KEEP guardrail

## Summary

This release adds durable prose overlay artifacts and first-pass variant/merge
planning support, with hard KEEP-span protection during prose saves.

## Added

- New prose overlay endpoints:
  - `GET /v2/prose-overlay/{unitId}`
  - `POST /v2/prose-overlay/{unitId}`
- Overlay artifact storage under:
  - `prose_overlays/{unitId}.json`
- Overlay schema fields:
  - `locks[]`
  - `variants[]`
  - `mergeRequests[]`
  - `audio`
- Unit editor UI (phase-1):
  - lock directives from selected spans
  - variant creation from selected spans
  - merge request artifact creation from selected variants.

## Changed

- `POST /v2/prose/{unitId}` now enforces KEEP lock integrity:
  - unresolved KEEP spans block save with conflict response
  - resolved KEEP spans are re-anchored after successful save.

## Story Agent Guidance

- Use prose overlays for review directives and variant planning.
- Keep canonical prose clean; store revision control metadata in overlay artifacts.
