# Patch Notes — engine-1.10.3

Date: 2026-03-03
Scope: protocol resilience via managed `PROTOCOL_RULES.md`

## Summary

This release adds a dedicated managed protocol document so engine enforcement
does not depend on AGENTS conventions alone.

## Added

- New managed doc:
  - `prosada/docs/PROTOCOL_RULES.md`
- `AGENT_START_HERE.md` now points to `PROTOCOL_RULES.md` for durable protocol
  and escalation requirements.

## Changed

- Managed docs pack bumped to `1.10.3`.
- Patch notes index updated with this release.

## Story Agent Guidance

- Continue using layered `prosada/AGENTS.md` for local project rules.
- Treat `PROTOCOL_RULES.md` as canonical engine protocol contract.
