# ProsAda — Agent Start Here

> **Managed by ProsAda tooling** · Version 1.3.0
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

## Done Checklist (high-level)

After making changes, verify:
- [ ] `manifest.json` root pointer is correct
- [ ] All `parentId` + `children[]` references are consistent
- [ ] No orphaned units (units not reachable from root)
- [ ] Semantic refs use valid `kind:entity-id` pairs (run `/v2/semantic-refs`)
- [ ] Tooling is current (`python scripts/check_tooling_health.py`)

See `FORMAT_CHEATSHEET.md` for schema details.
See `WORKFLOWS.md` for task recipes.
See `TOOLING.md` for renderer and tooling usage.
