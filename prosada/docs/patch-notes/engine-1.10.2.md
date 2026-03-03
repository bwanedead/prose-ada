# Patch Notes — engine-1.10.2

Date: 2026-03-03
Scope: layered `prosada/AGENTS.md` with preserved local additions

## Summary

This release moves local-guidance layering to `prosada/AGENTS.md` directly.
Tooling now refreshes engine-owned guidance at the top while preserving story
repo additions in a dedicated local section inside the same file.

## Added

- `prosada/AGENTS.md` managed write behavior:
  - managed engine guidance section (refreshed by tooling)
  - preserved local section header:
    - `Local Story Repo Additions (Preserved)`
- Legacy compatibility behavior:
  - if an existing `prosada/AGENTS.md` has no local-section marker, existing
    content is carried forward into the preserved local section.

## Changed

- Recommended precedence in story repos now includes `prosada/AGENTS.md` as the
  canonical merged engine+local contract file.
- Managed docs pack bumped to `1.10.2`.

## Story Agent Guidance

- Put project-specific rules in the local section of `prosada/AGENTS.md`.
- Do not edit managed docs to store local-only policy.
- Keep engine-protocol changes in app-repo patch notes/managed docs.
