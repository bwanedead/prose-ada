# Patch Notes — engine-1.5.0

Date: 2026-03-02
Scope: connective unit support + prose editing/read APIs + editor UX policy

## Summary

This update formalizes connective narrative units and improves prose editing
workflows so prose can be accessed directly from selected units/scope.

## Added

- New content unit type: `connective`
  - intended for between-scene narrative tissue (bridges/transitions/montage glue)
  - supported by validator/composer/frontend type filters.
- Prose API endpoints:
  - `GET /v2/prose/{unitId}`
  - `POST /v2/prose/{unitId}`
- Unit editor prose-first UX:
  - prose view/edit modes
  - larger prose workspace modal
  - schema artifact moved to collapsible advanced section.

## Changed

- Managed docs now include connective authoring guidance and prose API usage.
- Docs/version pack bumped to `1.5.0`.

## Why

Story authoring needs two complementary layers:
- canonical schema structure (units/registries/pins)
- literal prose drafting at unit/scope level

This release reduces friction between those layers without coupling external
story repos to frontend runtime code.

## Story Agent Guidance

- You can begin creating `type: "connective"` units where between-scene prose is needed.
- Keep strict pin rules unchanged: connective is still a child content unit.
- Use `narrative.textRef` for prose files exactly like scenes/chapters.
- No migration is required for existing units; this is additive.
