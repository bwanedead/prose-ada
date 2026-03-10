# ProsAda Protocol Rules

> **Managed by ProsAda tooling** · Version 1.12.2
> Durable engine protocol contract for story-repo agents.

---

## Purpose

This document is the non-AGENTS enforcement surface for engine protocol.
It remains stable even if AGENTS conventions evolve.

---

## Hard Rules

1. Do not convert engine limitations into permanent story-local schema policy.
2. Keep story-intent edits separate from engine workaround edits.
3. If engine behavior blocks a task, create a handoff note:
   - `prosada/docs/engine-handoffs/<yyyy-mm-dd>-<slug>.md`
4. Treat workarounds as temporary debt and remove after engine-native support lands.

---

## Canonical Defaults (until superseded by patch notes)

- Prose wiring:
  - If prose exists, set `narrative.textRef`.
  - Deterministic path: `<unitId>.md` under `prosada/units/`.
  - Optional beat-boundary marker syntax:
    - `[[[beat-id|Beat Name|start]]]`
    - `[[[beat-id|Beat Name|end]]]`
  - Lock directives use inline marker wrappers:
    - `[[[lock|KEEP|<lockId>|start]]] ... [[[lock|KEEP|<lockId>|end]]]`
    - `SOFT_KEEP`, `REWRITE`, `EXPLORE` use the same form.
  - Marker tokens are authoring metadata and should be scrubbed from reader/TTS/export output.
- Theory/ethos stability:
  - Always set both `doctrineStatus` and `mutationLock`.
  - Working guide default: `leaning` + `soft_locked`.
  - Approved doctrine default: `approved` + `hard_locked`.

---

## Escalation Format

Each handoff note should include:
- observed symptom
- expected behavior
- current workaround (if any)
- why workaround is temporary
- requested engine-level change

---

## Authority Order

When guidance conflicts:
1. Latest patch notes in `prosada/docs/patch-notes/`
2. This file (`PROTOCOL_RULES.md`)
3. `AGENT_START_HERE.md`
4. Local additions in `prosada/AGENTS.md`
