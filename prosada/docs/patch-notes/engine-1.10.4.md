# Patch Notes — engine-1.10.4

Date: 2026-03-05
Scope: canonical schema contract cleanup + semantic link validation + inherited guidance resolution

## Summary

This release removes stale schema guidance, hardens link semantics, and makes
theory/ethos guidance inheritance explicit in writing/editor surfaces.

## Added

- Validator semantic checks for unit links:
  - `usesTheory` target must be `theory` (warning when mismatched)
  - `usesEthos` target must be `ethos` (warning when mismatched)
  - `merges-into` / `branches-from` / `intersects` require `stream` source+target (error on mismatch)
- Writing/editor guidance resolution now includes ancestor inheritance with
  provenance (direct vs inherited source scope).

## Changed

- Managed docs now state canonical schema as `NarrativeUnit` and describe
  legacy graph primitives as projection compatibility shapes.
- Managed docs now document semantic link rules and inherited guidance behavior.
- Managed docs pack bumped to `1.10.4`.

## Story Agent Guidance

- Treat `usesTheory`/`usesEthos` as typed links, not generic pointers.
- Use top-down doctrine linking at higher scopes; descendants now inherit guidance
  in writing/editor views without link duplication.
- Do not rely on stale `execution` namespace references unless reintroduced by a
  later schema patch note.
