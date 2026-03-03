# Patch Notes — engine-1.10.1

Date: 2026-03-03
Scope: managed AGENT_START_HERE local appendix preservation

## Summary

This release adds a clean layering mechanism so story repos can keep local
agent guidance while still receiving managed engine updates.

## Added

- Tooling refresh append hook for:
  - `prosada/docs/AGENT_START_HERE.local.md`
- During install/refresh, managed `AGENT_START_HERE.md` now appends the local
  file content at the bottom under a labeled unmanaged section.

## Changed

- Managed docs updated with explicit layering guidance and precedence:
  1. repo-root `AGENTS.md`
  2. `prosada/docs/AGENT_START_HERE.md` (+ local appendix)
  3. other managed workflow docs and patch notes
- Managed docs pack bumped to `1.10.1`.

## Story Agent Guidance

- Put repo-specific ProsAda additions in:
  - `prosada/docs/AGENT_START_HERE.local.md`
- Avoid editing managed templates directly for local-only policy notes.
