# ProsAda — Agent Start Here

> **Managed by ProsAda tooling** · Version 1.10.4
> Refresh: `python scripts/check_tooling_health.py` · `POST /v2/tooling/refresh`

---

## What is /prosada/?

`/prosada/` is the canonical intent-graph workspace for this project.
It stores the **story structure and intent** in structured JSON units, separate
from prose files (`.md`). The app and agents read/write here.

**Canonical data lives in /prosada/ — not in prose files.**
Prose files (`.md`) are referenced by units but are not the source of structure.

---

## File Structure

```
prosada/
  manifest.json          ← project root pointer + metadata
  units/                 ← one JSON file per narrative unit
  registries/            ← characters, locations, symbols, concepts, …
  scripts/               ← managed tooling scripts + standalone runtime packages
  docs/                  ← this directory — managed agent documentation
  tooling.json           ← tooling version + checksum metadata
```

---

## Canonical vs Derived Data

| What                      | Where                        | Editable? |
|---------------------------|------------------------------|-----------|
| Unit structure (acts, scenes, beats) | `units/*.json`    | ✅ Yes     |
| Character/location registry          | `registries/*.json` | ✅ Yes   |
| Canvas layout hints                  | `units/*.json` → `view.canvas` | ✅ Yes |
| Storyboard / presentation hints      | `units/*.json` → `presentation` | ✅ Yes |
| Prose text                           | `units/*.md` (via textRef)  | ✅ Yes  |
| Canvas render output                 | `scripts/render_timeline.py` output | ❌ Derived |
| Prompt packet export                 | `GET /v2/export/prompt-packets` output | ❌ Derived |
| Managed scripts/docs                 | `scripts/`, `docs/`         | ❌ Managed |

---

## Project Modes

ProsAda supports two project modes — the canonical `/prosada/` structure is
**identical** in both. Only the storage location differs:

- **local** — stored in app-managed `~/.local/share/prosada/local-projects/`
- **external** — stored at `<repoRoot>/prosada/` inside a version-controlled repo

Agents working inside a repo with `/prosada/` always use the **external** layout.

---

## Ownership Boundary (App vs Story Repo)

- The **app repo** (`prosada-app`) owns render/composition policy and UI behavior.
- The **story repo** owns canonical schema/content under `prosada/`.

When behavior changes in visualization policy (for example stream ownership
rendering), story agents should consult patch notes before changing schema.

---

## Local AGENTS Layering (Required)

- ProsAda tooling guidance is installed under `prosada/docs/` (managed).
- Repo-root `AGENTS.md` remains story-repo-owned and may contain local rules.
- Tooling refresh does not overwrite repo-root `AGENTS.md`.
- ProsAda root `AGENTS.md` is installed with:
  - a managed engine guidance section (updated on refresh)
  - a preserved local section (`Local Story Repo Additions`) that keeps local edits.
- Recommended precedence for agents in story repos:
  1. local repo `AGENTS.md`
  2. `prosada/AGENTS.md` (managed top + preserved local tail)
  3. `prosada/docs/PROTOCOL_RULES.md`
  4. `prosada/docs/WORKFLOWS.md` and patch notes

Use local `AGENTS.md` for repo-specific process, and managed docs for
engine/protocol contracts.

---

## Drift Prevention Protocol (Required)

If behavior appears blocked by an engine limitation, do **not** solve it by
inventing story-local schema conventions or repo-only policy docs.

Required response:

1. Keep canonical story intent edits separate from engine workaround edits.
2. Record an engine handoff note under:
   - `prosada/docs/engine-handoffs/<yyyy-mm-dd>-<slug>.md`
3. Include:
   - observed symptom
   - expected behavior
   - local workaround applied (if any)
   - why workaround is temporary
   - requested engine-level fix
4. Treat local workaround as temporary debt to remove after engine update.

Goal: avoid drift between story repos and ProsAda engine behavior.

---

## Canonical Interim Conventions (until superseded by patch notes)

Use these defaults consistently across story repos:

- Prose wiring:
  - If a chapter/scene/connective has prose, set `narrative.textRef`.
  - Use deterministic path: `<unitId>.md` under `prosada/units/`.
  - Do not invent repo-specific folder/filename heuristics.
- Theory/ethos stability fields:
  - Always set both `doctrineStatus` and `mutationLock`.
  - Working guidance default: `leaning` + `soft_locked`.
  - Approved doctrine default: `approved` + `hard_locked`.

---

## Layout Policy (Important)

Manifest controls layout behavior:

- `legacy-auto` (default): pins are optional; composer may derive layout.
- `strict-pins`: pins are required and treated as authoritative.

Strict pin contract (v1):
- Root content unit (`book`/`series`): manual + `coordinateMode: "absolute"`
- Child content units (`act/chapter/scene/...`): manual + `coordinateMode: "relative"`
- Stream units: manual + `coordinateMode: "absolute"`

Use strict readiness diagnostics before switching a project:
- API: `GET /v2/layout-readiness`

---

## Safe Editing Principles

1. **Preserve `unitId` values** — they are stable cross-references. Never change them.
2. **Use `children[]` for ordering** — sibling order is the parent's `children` list.
3. **Edit `narrative.*` for story content** — `view.*` is for UI hints only.
4. **Keep `parentId` consistent** with the parent's `children[]` list.
5. **Use semantic ref syntax** for inline entity links: `Text[[kind:entity-id]]`
6. **Run validation after edits**: `GET /v2/validate` or check manifests.

---

## Planning Instrumentation (Phase 1)

Units may include optional `structure` planning metadata for cadence/reward design.
This is a planning layer, not canonical plot truth unless:

- `structure.planningStatus = "locked"`

Use statuses intentionally:
- `open`    → exploratory / unstable
- `leaning` → preferred current direction
- `locked`  → canonical planning contract

Canonical promise contracts should live in:
- `registries/promises.json`

Keep promise history stateful (`opened`, `sharpened`, `reframed`, `delayed`,
`partially_paid`, `paid`, `inverted`, `abandoned`) so diagnostics can track movement.

Reusable planning primitives:
- `type: "theory"` and `type: "ethos"` are first-class reusable units.
- Recommended: keep them top-level and attach to scope units via links
  (`usesTheory`, `usesEthos`) instead of duplicating the same notes repeatedly.

---

## Done Checklist (high-level)

After making changes, verify:
- [ ] `manifest.json` root pointer is correct
- [ ] All `parentId` + `children[]` references are consistent
- [ ] No orphaned units (units not reachable from root)
- [ ] Semantic refs use valid `kind:entity-id` pairs (run `/v2/semantic-refs`)
- [ ] Tooling is current (`python scripts/check_tooling_health.py`)

See `FORMAT_CHEATSHEET.md` for schema details.
See `PROTOCOL_RULES.md` for durable engine protocol/enforcement rules.
See `WORKFLOWS.md` for task recipes.
See `TOOLING.md` for renderer and tooling usage.
