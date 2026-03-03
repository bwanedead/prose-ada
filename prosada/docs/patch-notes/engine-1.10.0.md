# Patch Notes — engine-1.10.0

Date: 2026-03-03
Scope: story-repo drift prevention protocol + prose wiring/theory defaults guidance

## Summary

This release formalizes a required protocol for story agents: do not encode
engine limitations as story-local conventions. It also standardizes interim
defaults for prose path wiring and theory lock semantics.

## Added

- Managed docs protocol sections:
  - drift prevention and engine escalation contract
  - required handoff-note path in story repos:
    - `prosada/docs/engine-handoffs/<yyyy-mm-dd>-<slug>.md`
- Workflow guidance for deterministic prose wiring:
  - set `narrative.textRef` to `<unitId>.md`
  - keep prose files in `prosada/units/`
- Workflow guidance for explicit theory/ethos defaults:
  - working guide: `leaning` + `soft_locked`
  - approved doctrine: `approved` + `hard_locked`

## Changed

- Managed docs pack bumped to `1.10.0`.
- Patch notes index now includes this protocol release.

## Story Agent Guidance

- If a behavior gap appears engine-owned, escalate via handoff note and patch notes.
- Keep local workaround edits minimal and temporary.
- Remove temporary workaround patterns after corresponding engine fixes land.
