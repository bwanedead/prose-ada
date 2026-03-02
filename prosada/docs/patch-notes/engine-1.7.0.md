# Patch Notes — engine-1.7.0

Date: 2026-03-02
Scope: theory lock semantics + prose pagination overlay (phase-1)

## Summary

This release introduces explicit theory/ethos stability semantics and adds
prose pagination overlay controls in the editor for page-feel review.

## Added

- Theory/ethos structure fields:
  - `doctrineStatus`: `open` | `leaning` | `approved`
  - `mutationLock`: `mutable` | `soft_locked` | `hard_locked`
- Hard-lock save guardrail:
  - hard-locked theory/ethos units reject normal save requests unless explicit override is used.
- Prose editor controls:
  - overlay mode selector (phase-1 scaffold)
  - pagination profile selector (`document`, `paperback`)
  - page-mode viewer with visible page boundaries and computed page numbers.

## Story Agent Guidance

- Use `doctrineStatus` for confidence/approval.
- Use `mutationLock` to control editability independent of doctrine confidence.
- For stable doctrine objects, set `mutationLock: "hard_locked"` after approval.
