# Patch Notes — engine-1.11.0

Date: 2026-03-08
Scope: inherited guidance governance stack protocol + integrity hardening rollout

## Summary

This release formalizes guidance stack resolution as an engine-level derived
protocol and tightens integrity behavior across validation, doctor, and safe
mutation seams.

## Added

- Guidance governance endpoint:
  - `GET /v2/guidance-stack/{unitId}`
- Deterministic stack semantics:
  - inherited vs local applicability
  - attachment provenance by scope
  - explicit ordering contract metadata
- Guidance stack protocol coverage in backend tests.

## Changed

- Delete semantics:
  - `/v2/unit/{unitId}` now performs safe structural delete for in-tree leaves
    (with parent cleanup), while still blocking destructive deletes
    (root, descendants, inbound references).
- Validation/doctor diagnostics:
  - malformed/corrupt unit load diagnostics are surfaced in core integrity
    surfaces (`/v2/validate`, `/v2/doctor`) in addition to project load.
- Renderer dependency behavior:
  - renderer-backed endpoints fail explicitly when optional renderer deps are
    unavailable (instead of crashing import/route execution).

## Story Agent Guidance

- Treat guidance as inherited governance, not a scene-local brief convention.
- Attach reusable `theory`/`ethos` artifacts explicitly at intended scopes.
- Resolve applicable guidance through `/v2/guidance-stack/{unitId}` instead of
  guessing from one local file.
- Continue using canonical units/registries as source of truth; guidance stack
  is derived at read-time (not persisted).

## Compatibility Notes

- No canonical story schema migration required.
- Existing projects in `legacy-auto` remain supported.
- If renderer dependencies are absent locally, rendering endpoints may return
  dependency-related failures until tooling/runtime is restored.
