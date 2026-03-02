# Patch Notes — engine-1.6.0

Date: 2026-03-02
Scope: reusable theory/ethos units + explicit attachment link semantics

## Summary

This release introduces two first-class reusable unit types so planning guidance
can be authored once and attached across multiple scopes.

## Added

- Unit types:
  - `theory`
  - `ethos`
- New link types:
  - `usesTheory`
  - `usesEthos`

## Changed

- Strict-pins validation excludes non-canvas reference units (theory/ethos).
- Canvas composer excludes theory/ethos from rendered interval composition.
- Managed docs now include reusable reference-unit authoring guidance.
- Docs/version pack bumped to `1.6.0`.

## Story Agent Guidance

- Create theory/ethos as reusable objects (recommended top-level/root).
- Attach them to scenes/chapters/acts via links, not via duplicated prose.
- Keep strict pin drafting unchanged for timeline/content units.
