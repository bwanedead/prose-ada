# Patch Notes — engine-1.3.0

Date: 2026-02-28
Scope: tooling/runtime/docs + strict layout policy foundation

## Summary

This update introduces a strict schema-driven layout policy path while keeping
backward compatibility for existing projects.

## Added

- `layoutPolicy` support (`legacy-auto` | `strict-pins`)
- strict-pins readiness diagnostics:
  - API: `GET /v2/layout-readiness`
  - CLI: `python workspace_cli.py layout-readiness --repo-root <repo-root>`
- distributed standalone runtime for repo-local renderer:
  - `prosada/scripts/domain/`
  - `prosada/scripts/persistence/`
  - `prosada/scripts/services/`
- tooling refresh command:
  - `python workspace_cli.py refresh-tooling --repo-root <repo-root>`

## Changed

- strict policy enforcement is now available in validation/composition paths.
- new projects default to `settings.layoutPolicy = "legacy-auto"` for safe migration.
- managed tooling checks now include runtime package directory checksums.

## Why

Some projects observed timeline projection drift because auto-derived placement
was still active when explicit pins were absent. This release establishes the
contract path toward schema-authoritative positioning.

## Action Required (for strict mode)

1. Run readiness check.
2. Add required explicit pins to units (`view.canvas.layout`).
3. Flip manifest policy to `strict-pins` only after readiness passes.

## Safety Notes

- Tooling refresh updates managed assets only (`scripts/`, `docs/`, `tooling.json`).
- Story data files (`units/`, `registries/`, prose files) are not modified by tooling refresh.
