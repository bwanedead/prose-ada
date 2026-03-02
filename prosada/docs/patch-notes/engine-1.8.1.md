# Patch Notes — engine-1.8.1

Date: 2026-03-02
Scope: prose lock/merge safety hardening

## Summary

This release hardens KEEP lock resolution and merge-request validation so prose
revision workflows fail safely when anchors drift or conflict.

## Added

- Deterministic KEEP lock resolution outcomes:
  - explicit failure reasons (`TEXT_EMPTY`, `TEXT_NOT_FOUND`, `ANCHOR_MISMATCH`, `AMBIGUOUS_MATCH`)
  - ambiguous matches now fail instead of guessing.
- Per-lock resolution metadata persisted after save:
  - `resolvedBy` (`index` | `anchors` | `unique_text`)
  - `resolutionConfidence` (`high` | `degraded`)
  - `lastResolvedAt`
  - `ambiguityCount`
- Save response warnings:
  - `KEEP_REANCHORED_DEGRADED` when fallback re-anchoring is used.

## Changed

- `POST /v2/prose-overlay/{unitId}` now rejects merge requests that overlap
  KEEP lock ranges (`MERGE_REQUEST_KEEP_CONFLICT`).
- `POST /v2/prose/{unitId}` now validates merge-request/KEEP overlap before write.
- Unit editor now:
  - blocks merge-request creation when selected range overlaps KEEP spans
  - surfaces degraded KEEP re-anchor warnings after save
  - displays lock resolution metadata in the lock list.

## Story Agent Guidance

- Treat degraded KEEP warnings as review-required signals.
- Re-anchor or adjust locks when ambiguity conflicts are reported.
- Keep merge regions carved around hard KEEP spans.
