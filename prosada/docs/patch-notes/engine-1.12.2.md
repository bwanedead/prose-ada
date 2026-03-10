# Patch Notes — engine-1.12.2

Date: 2026-03-10
Scope: beat deletion vs prose-marker reconciliation safety

## Summary

This release hardens beat deletion so structural changes do not silently drift
from prose marker content in parent scene prose files.

## Added

- `DELETE /v2/unit/{unitId}` now accepts:
  - `beatProsePolicy=cancel` (default)
  - `beatProsePolicy=remove_span`
  - `beatProsePolicy=strip_markers`
  - `beatProsePolicy=keep_orphaned`
- Default-safe behavior for beat delete:
  - if parent prose contains beat markers for the target beat and policy is
    `cancel`, deletion is blocked with explicit reconciliation diagnostics.

## Changed

- Reconciliation writes are now failure-safe:
  - prose rewrites are staged/applied before structural deletion
  - if prose write fails, structural delete is not applied
  - if structural phase fails after prose rewrite, engine attempts rollback of
    prose + structure snapshots
- Delete safety tests now cover:
  - `keep_orphaned`
  - invalid `beatProsePolicy`
  - failed prose-write path (must keep structure intact)

## Story Agent Guidance

- On beat deletion, choose explicit prose reconciliation policy instead of
  assuming marker cleanup.
- Use `strip_markers` to keep prose body, `remove_span` to remove marker-wrapped
  body, and `keep_orphaned` only when intentionally preserving detached draft text.

## Compatibility Notes

- No canonical schema migration required.
- This is an operation-policy hardening update; story data model is unchanged.
