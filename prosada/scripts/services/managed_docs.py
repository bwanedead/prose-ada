"""
Managed Agent Docs — ProsAda Burst 11

Versioned string templates for the agent docs installed into each project's
/prosada/docs/ directory.

Design:
  - versioned docs pack with patch notes per release
  - Each file includes a managed-artifact header with DOCS_VERSION stamped in
  - Templates are Python string constants — statically defined, not dynamically
    generated from project state (keeps install/refresh stable and testable)
  - Checksums in tooling.json are computed from the rendered text bytes so
    staleness detection works correctly after a version bump

Adding a new doc: add a new entry to DOC_FILES and write its template below.
Bumping the version: increment DOCS_VERSION — all docs will be refreshed next heal.
"""

from __future__ import annotations

DOCS_VERSION = "1.10.9"
_DOCS_SUBDIR = "docs"

# ---------------------------------------------------------------------------
# Managed header (prepended to every doc file)
# ---------------------------------------------------------------------------

def _managed_header(filename: str) -> str:
    return f"""\
<!--
  MANAGED BY PROSADA TOOLING — do not edit manually.
  Version: {DOCS_VERSION}
  Source:  ProsAda app tooling pack
  Refresh: POST /v2/tooling/refresh  (or run scripts/check_tooling_health.py --heal)
  Warning: Local edits will be overwritten on the next tooling refresh.
-->

"""


# ---------------------------------------------------------------------------
# A. AGENT_START_HERE.md
# ---------------------------------------------------------------------------

_AGENT_START_HERE = """\
# ProsAda — Agent Start Here

> **Managed by ProsAda tooling** · Version {version}
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
  - Optional beat-boundary markers in prose:
    - `[[[beat-id|Beat Name|start]]]`
    - `[[[beat-id|Beat Name|end]]]`
    - keep markers in source prose; read viewers may hide tokens while preserving boundaries
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
"""


# ---------------------------------------------------------------------------
# B. FORMAT_CHEATSHEET.md
# ---------------------------------------------------------------------------

_FORMAT_CHEATSHEET = """\
# ProsAda Format Cheatsheet

> **Managed by ProsAda tooling** · Version {version}

---

## Unit Basics (units/*.json)

```json
{{
  "schemaVersion": "2.0.0",
  "unitId": "scene-the-anomaly",        // stable ID — never change
  "type": "scene",                       // series|book|act|sequence|chapter|connective|scene|beat|arc|theory|ethos|stream
  "title": "The Anomaly",
  "summary": "Ada detects the first echo.",
  "parentId": "chapter-01",             // null for root
  "children": [],                        // ordered child unitIds
  "links": [],                           // explicit unit relationships
  "narrative": {{
    "status": "draft",                   // draft|review|locked
    "threadsAdvanced": ["stream-A"],     // stream unitIds advanced here
    "characters": ["ada-id"],            // character registry IDs
    "locations": ["observatory-id"],
    "newInfo": "First echo detected.",
    "dripHook": "What caused the echo?",
    "payoffDelivered": null,
    "beautyHooks": null,
    "notes": "Research: Fermi paradox.",
    "textRef": "scene-the-anomaly.md"   // relative path to prose file
  }},
  "structure": {{
    "functions": ["setup", "investigation"],
    "cadenceRole": "rise",
    "effortLoad": "medium",
    "planningStatus": "leaning",
    "rewardTokens": [
      {{
        "type": "clue",
        "strength": 3,
        "description": "Ada observes a measurable sky inconsistency.",
        "threadRefs": ["stream-anomaly"]
      }}
    ],
    "cadenceEnvelope": {{
      "intensityPoints": [{{"x": 0.0, "y": 0.2}}, {{"x": 0.35, "y": 0.8}}],
      "frequencyTarget": "intermittent",
      "spacingTarget": "every_1_to_2_chapters",
      "planningStatus": "open"
    }},
    "modelUpdate": {{
      "before": "Likely perceptual glitch",
      "shift": "Possible external anomaly",
      "after": "Needs verification",
      "confidenceDelta": 1
    }}
  }},
  "guidance": {{
    "kind": "prose_brief",             // optional soft classification (theory/ethos focus)
    "tags": ["scene", "voice"]         // optional free-form tags
  }},
  "view": {{
    "canvas": {{
      "x": null, "y": null, "collapsed": false,
      "layout": null                     // or StreamLayout (see below)
    }}
  }}
}}
```

---

## Structure Enums (controlled vocabulary)

- `functions`: `setup` | `escalation` | `squeeze` | `release` | `payoff` | `climax` | `bridge` | `reversal` | `investigation` | `aftermath`
- `cadenceRole`: `rise` | `drop` | `plateau` | `spike` | `sustain` | `transition`
- `effortLoad`: `low` | `medium` | `high`
- `planningStatus`: `open` | `leaning` | `locked`
- `rewardTokens.type`: `clue` | `competence` | `contradiction` | `decision` | `atmosphere` | `emotional` | `model_update` | `reversal` | `humor` | `relational`
- `doctrineStatus`: `open` | `leaning` | `approved` (theory/ethos confidence)
- `mutationLock`: `mutable` | `soft_locked` | `hard_locked` (edit guardrail)

Planning rule:
- Treat planning metadata as non-canonical until `planningStatus = "locked"`.

---

## Guidance Taxonomy (optional, unit.guidance)

Soft classification metadata for guidance artifacts (primarily `theory`/`ethos`):

- `guidance.kind`: optional free-form label
- `guidance.tags[]`: optional free-form tags

Recommended `guidance.kind` values (conventions, not hard limits):
- `global_ethos`
- `scope_theory`
- `prose_brief`
- `revision_brief`
- `constraint`
- `checklist`
- `research_note`
- `spec`
- `prompt_scaffold`

Policy:
- keep top-level `type` stable and load-bearing
- use `guidance.kind` for flexible taxonomy needs first

---

## Unit Types

| Type       | Role                                              |
|------------|---------------------------------------------------|
| `series`   | Multi-book container (root of a series)           |
| `book`     | Single book (root of a book project)              |
| `act`      | Major structural division                         |
| `sequence` | Mid-level grouping                                |
| `chapter`  | Chapter-level unit                                |
| `connective` | Between-scene connective tissue (transition/bridge prose) |
| `scene`    | Scene — primary story beat container              |
| `beat`     | Sub-scene moment                                  |
| `arc`      | Character/thematic arc (cross-cutting)            |
| `theory`   | Reusable planning theory object (attach via links) |
| `ethos`    | Reusable writing/development ethos object (attach via links) |
| `stream`   | Parallel timeline/thread (no parentId, no children in hierarchy) |

---

## Stream Identity Rule

Streams are **separate root units** (type=`stream`, parentId=null).
A content unit is "in" a stream by including the stream's unitId in its
`narrative.threadsAdvanced` array — **not** via parentId.

```json
// scene unit:
"narrative": {{ "threadsAdvanced": ["stream-yggdrasil-arc"] }}

// stream unit:
{{ "unitId": "stream-yggdrasil-arc", "type": "stream", "parentId": null }}
```

Render ownership policy (app behavior):
- A unit renders on at most one stream lane by default.
- Owner stream = first valid stream ID in `threadsAdvanced[]`.
- Additional stream IDs are metadata (cross-stream semantics), not duplicate pills.
- Canvas bars/strip are scene-resolution by default; beat-level detail belongs in outline/prose surfaces.

---

## Layout Hints (view.canvas.layout)

Layout pins for canvas rendering. In `strict-pins`, these are required.

```json
"layout": {{
  "mode": "manual",               // "auto" = derived | "manual" = use start+span
  "coordinateMode": "absolute",   // "absolute" | "relative"
  "start": 3.0,                   // spine position (absolute) or fraction of parent (relative)
  "span": 2.0                     // width in spine units (absolute) or fraction (relative)
}}
```

**coordinateMode=absolute**: `start`/`span` are spine logical units (1 unit = 100px at default zoom).

**coordinateMode=relative**: `start`/`span` are fractions of the parent unit's resolved span.
  - `absStart = parentStart + start × parentSpan`
  - `absSpan  = span × parentSpan`

Policy notes:
- Root content units must use `absolute` in strict mode.
- Child content units must use `relative` in strict mode.
- Stream units must use `absolute` in strict mode.
- Missing/invalid pins are validation errors in strict mode.

---

## Semantic Reference Syntax

Inline annotations that link visible text to stable entity IDs:

```
VisibleText[[kind:entity-id]]
```

Examples:
```
Joey Valdez[[char:joey-valdez]] entered the diner.
The Arboros[[concept:arboros]] lattice shimmered.
Near Blueberry Pond[[location:blueberry-pond]], Ada looked up.
The red sigil[[symbol:red-sigil]] appeared.
```

Supported kinds → Registry file mapping:

| Kind       | Registry file           |
|------------|-------------------------|
| `char`     | `registries/characters.json` |
| `concept`  | `registries/concepts.json`   |
| `symbol`   | `registries/symbols.json`    |
| `location` | `registries/locations.json`  |
| `artifact` | `registries/artifacts.json`  |
| `thread`   | `registries/threads.json`    |
| `promise`  | `registries/promises.json`   |

---

## Registry Entry Format (registries/*.json)

```json
{{
  "schemaVersion": "2.0.0",
  "type": "characters",
  "entries": [
    {{
      "id": "joey-valdez",
      "name": "Joey Valdez",
      "description": "Diner regular, grounding confidant.",
      "color": "#e91e63"
    }}
  ]
}}
```

### Promise registry contract (`registries/promises.json`)

```json
{{
  "schemaVersion": "2.0.0",
  "type": "promises",
  "entries": [
    {{
      "id": "p-anomaly-nature-01",
      "name": "Nature of anomaly",
      "promiseType": "mystery",
      "planningStatus": "leaning",
      "openedAtUnitId": "chapter-01",
      "targetWindow": {{ "kind": "chapter_range", "from": 1, "to": 4 }},
      "state": "sharpened",
      "history": [
        {{ "unitId": "chapter-01", "transition": "opened" }},
        {{ "unitId": "chapter-02", "transition": "sharpened" }}
      ],
      "paidAtUnitId": null
    }}
  ]
}}
```

Promise enums:
- `promiseType`: `mystery` | `plot` | `character` | `thematic` | `symbolic`
- `history.transition`/`state`: `opened` | `sharpened` | `reframed` | `delayed` | `partially_paid` | `paid` | `inverted` | `abandoned`

---

## Presentation / Storyboard Metadata (optional, unit.presentation)

Add directorial/cinematic hints for image/video/storyboard workflows.
All fields are optional — existing units without this block are fully valid.

```json
"presentation": {{
  "shotType":     "establishing",   // establishing|wide|medium|closeup|insert|aerial|pov|cutaway
  "cameraAngle":  "low",            // eye-level|low|high|overhead|dutch
  "cameraMotion": "dolly",          // static|pan|tilt|dolly|handheld|push-in|pull-out|crane
  "framingNotes": "Hold on observatory dome as lights flicker.",
  "moodTags":     ["tense", "wonder"],
  "visualStyleTags": ["cinematic", "stark"],
  "lightingTags": ["natural", "backlit"],
  "colorPaletteTags": ["cool", "desaturated"],
  "focusSubjectIds": ["ada"],       // registry entity IDs that are visual focus
  "compositionNotes": "Ada in foreground, Yggdrasil lattice ghostly behind.",
  "blockingNotes": "Ada walks to telescope, turns as radio fires.",
  "imagePromptHints": "observatory interior, star charts, eerie blue light",
  "videoPromptHints": "slow dolly-in, ambient sound drops to silence",
  "continuityNotes": "Match lighting from prior chapter — moonlight through dome.",
  "extras": {{}}
}}
```

String fields are unconstrained — suggested values are documented but not enforced.
Omit any field you don't need. An empty `{{}}` block is valid.

See `WORKFLOWS.md` for authoring and export recipes.

---

## Links (unit-to-unit relationships)

```json
"links": [
  {{ "type": "merges-into",   "targetId": "stream-main" }},
  {{ "type": "branches-from", "targetId": "scene-origin" }},
  {{ "type": "payoffFor",     "targetId": "scene-setup-1" }},
  {{ "type": "setsUp",        "targetId": "scene-payoff-3" }},
  {{ "type": "dependsOn",     "targetId": "scene-prereq" }},
  {{ "type": "usesTheory",    "targetId": "theory-onboarding-low-friction" }},
  {{ "type": "usesEthos",     "targetId": "ethos-reader-trust-no-cheapness" }},
  {{ "type": "intersects",    "targetId": "stream-b" }}
]
```

Link semantic rules:
- `usesTheory` must target a `theory` unit.
- `usesEthos` must target an `ethos` unit.
- `merges-into` / `branches-from` / `intersects` are stream topology links and must connect `stream` units.
- `payoffFor` / `setsUp` / `dependsOn` are broader relationship links.

Guidance inheritance behavior (writing/editor surfaces):
- resolve `usesTheory`/`usesEthos` from current unit and ancestors up to root
- dedupe by target unit ID
- show provenance (direct vs inherited source scope)
"""


# ---------------------------------------------------------------------------
# C. WORKFLOWS.md
# ---------------------------------------------------------------------------

_WORKFLOWS = """\
# ProsAda Workflows

> **Managed by ProsAda tooling** · Version {version}
> Recipe-style task guide for agents working with ProsAda projects.

---

## Create a new chapter unit

1. Choose a stable `unitId` (kebab-case, e.g. `chapter-02-the-signal`).
2. Create `units/chapter-02-the-signal.json`:

```json
{{
  "schemaVersion": "2.0.0",
  "unitId": "chapter-02-the-signal",
  "type": "chapter",
  "title": "The Signal",
  "summary": "Ada intercepts an anomalous frequency.",
  "parentId": "act-01",
  "children": [],
  "narrative": {{
    "status": "draft",
    "threadsAdvanced": [],
    "characters": [],
    "locations": [],
    "textRef": null
  }},
  "view": {{ "canvas": {{ "x": null, "y": null, "collapsed": false }} }}
}}
```

3. Add `"chapter-02-the-signal"` to `act-01`'s `children[]` list in the act's JSON.
4. Validate: `GET /v2/validate`

---

## Create a new scene unit

Same as chapter, but `"type": "scene"` and parent is a chapter.
Set `"textRef": "scene-the-signal.md"` if prose exists.

---

## Prose wiring protocol (required)

When prose drafting starts for a chapter/scene/connective unit:

1. Set `narrative.textRef` deterministically to `<unitId>.md`.
2. Keep prose file under `prosada/units/`.
3. Create the prose file if missing before expecting prose surfaces to render.
4. If the engine/UI fails to wire this automatically, file an engine handoff
   note under `prosada/docs/engine-handoffs/` instead of inventing local path rules.
5. Optional beat boundaries inside scene prose can use explicit bookends:
   - `[[[beat-id|Beat Name|start]]]`
   - `[[[beat-id|Beat Name|end]]]`
6. Keep beat markers in source prose for machine readability; viewers may hide
   marker tokens while still exposing boundary context.

---

## Create a connective unit (between scenes)

Use connective units when you need narrative tissue between concrete scene units
(transition prose, bridge beats, montage glue, etc.).

1. Create a unit under the chapter with `"type": "connective"`.
2. Keep strict pin rules the same as any child content unit (relative manual pin in strict mode).
3. Add prose via `narrative.textRef` (for example `connective-ch01-bridge-01.md`).

---

## Create reusable theory/ethos units

Use `theory` and `ethos` as first-class reusable objects.

Recommended pattern:
1. Keep them top-level (no parent) so they stay reusable across scopes.
2. Attach them to story units with links:
   - `usesTheory` → target is a `theory` unit
   - `usesEthos`  → target is an `ethos` unit
   - writing surfaces resolve these links from current unit + ancestors (inherited guidance)
3. Store detailed rationale in `summary`, `narrative.notes`, and optional prose `textRef`.
4. Optionally classify guidance using soft taxonomy metadata:
   - `guidance.kind` (recommended examples: `scope_theory`, `prose_brief`, `checklist`)
   - `guidance.tags[]` for free-form labels
5. Set stability defaults explicitly:
   - working guide: `doctrineStatus: "leaning"`, `mutationLock: "soft_locked"`
   - approved doctrine: `doctrineStatus: "approved"`, `mutationLock: "hard_locked"`

---

## Engine limitation escalation (required)

If a task requires changing story data only to compensate for app/engine behavior:

1. Stop and isolate whether the issue is schema truth or engine policy.
2. If engine policy, do not normalize workaround edits as canonical protocol.
3. Log a handoff note in `prosada/docs/engine-handoffs/` with repro + requested fix.
4. Continue only with minimal temporary workaround needed to unblock writing.

---

## Assign a unit to a stream

1. Find the stream's `unitId` (e.g., `stream-yggdrasil-arc`).
2. In the scene/chapter unit, add to `narrative.threadsAdvanced`:

```json
"narrative": {{ "threadsAdvanced": ["stream-yggdrasil-arc"] }}
```

3. The stream unit itself does **not** need modification.
4. If multiple streams are listed, put the intended **owner stream first**.
   - Rendering uses first valid stream as lane owner by default.
   - Additional stream IDs remain metadata (no auto-duplicate lane pills).

---

## Add semantic references in prose/text fields

In any text field (`summary`, `notes`, `newInfo`, etc.):

```
Ada[[char:ada-lovelace]] noticed the lattice[[concept:arboros]]
near Blueberry Pond[[location:blueberry-pond]].
```

In prose `.md` files (via `textRef`), same syntax applies:

```markdown
The signal pulsed from deep within the Yggdrasil[[symbol:yggdrasil-network]].
```

Query all refs: `GET /v2/semantic-refs`
Filter by kind: `GET /v2/semantic-refs?kind=char`
Filter by scope: `GET /v2/semantic-refs?scope=chapter-02-the-signal`

---

## Render a timeline snapshot

From inside the project repo (using the managed script):

```bash
# PNG (default)
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out snapshot.png

# SVG
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out snapshot.svg --format svg

# With metadata sidecar
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out snapshot.png --sidecar

# Scope to a subtree
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out act1.png --scope act-01

# Filter to specific streams
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out stream.png --streams stream-yggdrasil-arc
```

Via the app backend endpoint:
```
GET /v2/render/timeline          → PNG
GET /v2/render/timeline/svg      → SVG
GET /v2/render/timeline?scope=act-01&scale=60
```

---

## Query semantic refs

```bash
# All refs
GET /v2/semantic-refs

# Filter by kind
GET /v2/semantic-refs?kind=char

# Filter by entity
GET /v2/semantic-refs?id=joey-valdez

# Scope to subtree
GET /v2/semantic-refs?scope=act-01
```

---

## Prose read/write API

```bash
# Load prose for one unit
GET /v2/prose/<unitId>

# Save prose for one unit
POST /v2/prose/<unitId>
# body: {{ "content": "...", "textRef": "optional/path.md" }}
```

Notes:
- Works for any selected scope/unit; if `textRef` is empty, the backend defaults to `<unitId>.md`.
- This updates prose content only; it does not bypass staged schema commit rules.

---

## Check and refresh ProsAda tooling

```bash
# Check tooling health (from inside the repo)
python prosada/scripts/check_tooling_health.py

# Refresh managed scripts + docs (from inside the repo)
python prosada/scripts/check_tooling_health.py --heal

# Via the app backend
GET  /v2/tooling/status
POST /v2/tooling/refresh
```

---

## Validate project integrity

```
GET /v2/validate
```

Returns a list of issues (missing parents, orphaned units, etc.) with suggested fixes.

Strict readiness (before enabling strict-pins):

```
GET /v2/layout-readiness
```

This reports exactly which units are missing/invalid for strict pin policy.

---

## Strict pin migration workflow

If your project still uses `legacy-auto`, migrate in this order:

1. Generate strict readiness report.
2. Generate pins from current resolved layout (dry-run first).
3. Apply migration.
4. Re-run strict readiness.
5. Flip manifest policy to `strict-pins`.

App-repo CLI commands (run from the ProsAda app backend repository):

```bash
python workspace_cli.py layout-readiness --repo-root "<story-repo>"
python workspace_cli.py migrate-pins --repo-root "<story-repo>"
python workspace_cli.py migrate-pins --repo-root "<story-repo>" --apply
```

---

## Export/promote a local project to a repo

Via the app backend:
```
POST /workspace/export
{{
  "sourceProjectId": "proj-abc123",
  "targetRepoRootPath": "/path/to/target/repo",
  "registerAndActivate": true
}}
```

This copies all units/registries and installs the managed tooling pack at the target.

---

## Generate a projection payload

A projection payload is a normalized JSON document joining layout, unit metadata,
semantic refs, and execution stubs.

```bash
# Write projection JSON to file (repo-local CLI)
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out timeline.png --projection-json projection.json

# Via the app backend
GET /v2/projection/timeline
GET /v2/projection/timeline?scope=act-01
GET /v2/projection/timeline?kind=char&id=ada-lovelace
```

---

## Render with an overlay

Overlays visually highlight specific data in the rendered timeline.

```bash
# Semantic overlay — highlight events with any semantic refs
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out semantic.png --overlay semantic

# Semantic overlay — highlight events referencing a specific character
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out ada-refs.png \\
  --overlay semantic --semantic-kind char --semantic-id ada-lovelace

# Status overlay — tint events by narrative.status (draft/review/locked)
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out status.png --overlay status

# Overlay + projection JSON in one command
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out out.png \\
  --overlay semantic --projection-json projection.json
```

---

## Write a custom overlay script using projection JSON

1. Generate projection JSON:
```bash
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out /dev/null --projection-json proj.json
```

2. Read `proj.json` in your script. Each event in `events[]` has:
   - `eventId`, `unitId`, `title`, `status`, `start`, `span`, `laneId`
   - `semantic.refCount`, `semantic.byKind`, `semantic.entityIds`
   - `execution.hasExecution`, `execution.runCount`
   - `presentation.moodTags`, `presentation.shotType`, etc. (null if not authored)

3. Example: find all events referencing a specific entity:
```python
import json
proj = json.load(open("proj.json"))
target = "ada-lovelace"
hits = [
    ev["title"] for ev in proj["events"]
    if target in ev["semantic"].get("entityIds", [])
]
print("Events referencing", target, hits)
```

---

## Author presentation metadata on scenes

Add a `presentation` block to any unit JSON for storyboard/image/video hints:

```json
{{
  "unitId": "scene-the-anomaly",
  "narrative": {{ "status": "draft", "characters": ["ada"] }},
  "presentation": {{
    "shotType": "establishing",
    "moodTags": ["wonder", "unease"],
    "imagepromptHints": "observatory dome at night, stars visible, eerie blue glow",
    "lightingTags": ["natural", "backlit"]
  }}
}}
```

All fields are optional. Omit any you don't need.

---

## Generate storyboard prompt packets

Prompt packets join narrative + semantic + presentation context into structured
JSON for image/video generation workflows.

```bash
# Full packets (storyboard-basic profile, all fields)
GET /v2/export/prompt-packets

# Image-concept profile (emphasizes presentation + visual fields)
GET /v2/export/prompt-packets?profile=image-concept

# Narrative-summary profile (emphasizes hooks + payoffs)
GET /v2/export/prompt-packets?profile=narrative-summary

# Scoped to an act
GET /v2/export/prompt-packets?scope=act-01

# Via CLI (writes JSON to file)
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out timeline.png --prompt-export packets.json

# With profile
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out timeline.png \\
  --prompt-export packets.json --prompt-profile image-concept
```

Each packet contains:
  - `unitId`, `type`, `title`, `summary`
  - `narrative` (status, dripHook, payoffDelivered, newInfo, characters, locations)
  - `presentation` (full storyboard metadata or null)
  - `semantic` (refCount, byKind, entityIds)
  - `registrySlices` (character/location details)
  - `context` (parentId, parentTitle, siblingIndex, scopePath)

---

## Render with a presentation overlay

```bash
# Mood overlay — tint events by presentation.moodTags[0]
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out mood.png --overlay mood

# Shot type overlay — tint + badge by presentation.shotType
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out shot.png --overlay shot

# Combined: shot overlay + export projection JSON
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out shot.png \\
  --overlay shot --projection-json projection.json
```

Mood tints: tense=red, wonder=blue, melancholy=purple, dread=dark-violet,
warmth=amber, mystery=slate-teal, hope=green, unease=muddy-gold.
Shot badges: EST / WID / AER / MED / CU / INS / POV / CUT.
Events with no presentation data are dimmed when any other event has data.
"""


# ---------------------------------------------------------------------------
# D. PROTOCOL_RULES.md
# ---------------------------------------------------------------------------

_PROTOCOL_RULES = """\
# ProsAda Protocol Rules

> **Managed by ProsAda tooling** · Version {version}
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
"""


# ---------------------------------------------------------------------------
# E. TOOLING.md
# ---------------------------------------------------------------------------

_TOOLING = """\
# ProsAda Tooling Reference

> **Managed by ProsAda tooling** · Version {version}

---

## Managed scripts under prosada/scripts/

| Script                    | Purpose                                      |
|---------------------------|----------------------------------------------|
| `render_timeline.py`      | Render timeline snapshot (PNG/SVG + sidecar) |
| `check_tooling_health.py` | Check/refresh managed tooling in this repo   |
| `domain/`                 | Managed standalone runtime package           |
| `persistence/`            | Managed standalone runtime package           |
| `services/`               | Managed standalone runtime package           |

These are **managed copies** installed by ProsAda. Do not edit them manually —
they will be overwritten on the next tooling refresh.

---

## render_timeline.py — CLI Reference

```bash
python prosada/scripts/render_timeline.py [options]

Required:
  --project PATH    Path to prosada/ directory

Output:
  --out PATH        Output file (default: timeline.png)
  --format FORMAT   png (default) or svg
  --sidecar         Write a JSON metadata sidecar alongside --out

Filters:
  --scope UNIT_ID   Only render subtree of this unit
  --streams IDs              Comma-separated stream unitIds to include
  --status STATUS            draft | review | locked

Overlays (Burst 12+13):
  --overlay MODE             semantic | status | mood | shot
  --semantic-kind KIND       char | concept | symbol | location | artifact | thread
  --semantic-id ENTITY       Entity ID to highlight (e.g. ada-lovelace)
  --projection-json PATH     Write projection payload JSON to this path

Prompt export (Burst 13):
  --prompt-export PATH       Write prompt packet export JSON to this path
  --prompt-profile PROFILE   storyboard-basic (default) | image-concept | narrative-summary

Rendering:
  --scale N                  Pixels per spine unit (default: 80)
  --width N                  Total image width in pixels (auto if omitted)
  --title TEXT               Title text overlay on the image
```

Examples:
```bash
# Full timeline, PNG
python prosada/scripts/render_timeline.py --project prosada/ --out timeline.png

# SVG with sidecar
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out timeline.svg --format svg --sidecar

# Scope to one act
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out act1.png --scope act-01 --scale 60

# Semantic overlay — highlight events with any semantic refs
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out semantic.png --overlay semantic

# Semantic overlay — highlight a specific character
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out ada.png \\
  --overlay semantic --semantic-kind char --semantic-id ada-lovelace

# Status overlay — tint events by narrative.status
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out status.png --overlay status

# Mood overlay — tint by presentation.moodTags[0]
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out mood.png --overlay mood

# Shot type overlay — tint + badge by presentation.shotType
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out shot.png --overlay shot

# Export projection JSON alongside render
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out timeline.png --projection-json projection.json

# Export prompt packets alongside render
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out timeline.png --prompt-export packets.json

# Prompt packets with image-concept profile
python prosada/scripts/render_timeline.py \\
  --project prosada/ --out timeline.png \\
  --prompt-export packets.json --prompt-profile image-concept
```

Exit codes: `0` success · `1` project not found · `2` no content

---

## check_tooling_health.py — CLI Reference

```bash
python prosada/scripts/check_tooling_health.py [options]

  --project PATH    Path to prosada/ dir (default: auto-detect from script location)
  --heal            Reinstall stale or missing managed assets
  --json            Output status as JSON (for agent parsing)
```

Exit codes: `0` all OK · `1` missing or stale assets detected

Examples:
```bash
# Check status
python prosada/scripts/check_tooling_health.py

# Heal (reinstall stale assets)
python prosada/scripts/check_tooling_health.py --heal

# Machine-readable JSON output
python prosada/scripts/check_tooling_health.py --json
```

Patch notes are distributed in:

```text
prosada/docs/patch-notes/
```

---

## tooling.json — What it tracks

`prosada/tooling.json` is the machine-readable tooling metadata file.

```json
{{
  "toolingSchemaVersion": "2.0",
  "installedAt": "<ISO timestamp of first install>",
  "capabilities": {{
    "rendererPng": true,
    "rendererSvg": true,
    "semanticRefs": true
  }},
  "tools": {{
    "renderTimeline":      {{ "version": "...", "installedAt": "...", "scriptPath": "...", "checksum": "..." }},
    "checkToolingHealth":  {{ "version": "...", "installedAt": "...", "scriptPath": "...", "checksum": "..." }}
  }},
  "docs": {{
    "AGENT_START_HERE.md": {{ "version": "...", "installedAt": "...", "docPath": "...", "checksum": "..." }},
    "FORMAT_CHEATSHEET.md": {{ ... }},
    "WORKFLOWS.md":         {{ ... }},
    "PROTOCOL_RULES.md":    {{ ... }},
    "TOOLING.md":           {{ ... }}
  }}
}}
```

Staleness is detected by comparing the stored checksum (SHA-256) of each
managed asset against the file currently on disk. A mismatch means the file
has been modified or is from an older version.

---

## App backend endpoints

| Endpoint                      | Method | Description                                      |
|-------------------------------|--------|--------------------------------------------------|
| `/v2/tooling/status`          | GET    | Full status for all managed assets               |
| `/v2/tooling/refresh`         | POST   | Reinstall all managed assets                     |
| `/v2/layout-readiness`        | GET    | Strict-pins readiness diagnostics                |
| `/v2/projection/timeline`     | GET    | Projection payload JSON (layout+semantic+presentation) |
| `/v2/export/prompt-packets`   | GET    | Structured prompt packets for image/video workflows |
| `/v2/prose/{unitId}`          | GET    | Read prose payload for one unit (`content`, `textRef`) |
| `/v2/prose/{unitId}`          | POST   | Write prose payload for one unit                       |
| `/v2/prose-assembled/{unitId}`| GET    | Read assembled prose projection + provenance segments  |
| `/v2/prose-overlay/{unitId}`  | GET    | Read prose overlay artifact (`locks`, `variants`, `audio`) |
| `/v2/prose-overlay/{unitId}`  | POST   | Write prose overlay artifact                               |
| `/v2/tts/config`              | GET    | Read TTS voices/formats/defaults + key availability        |
| `/v2/tts/voices`              | GET    | List provider voices (OpenAI static, ElevenLabs live)      |
| `/v2/tts/api-key`             | POST   | Save provider API key to project-scoped machine keyring     |
| `/v2/tts/api-key`             | DELETE | Remove provider API key from project-scoped keyring         |
| `/v2/tts/speak`               | POST   | Generate one TTS chunk with `cueMode` (`flat`/`emoted`)     |
| `/v2/render/timeline`         | GET    | Render PNG snapshot                              |
| `/v2/render/timeline/svg`     | GET    | Render SVG snapshot                              |
| `/v2/semantic-refs`           | GET    | Query semantic entity references                 |
| `/v2/validate`                | GET    | Validate project integrity                       |

---

## Note on managed vs user-authored files

Only files under `prosada/scripts/` and `prosada/docs/` are managed.
The following are **never touched** by tooling refresh:
- repo-root `AGENTS.md` and any non-`prosada/` docs/process files
- `prosada/units/*.json` — your story structure
- `prosada/registries/*.json` — your story bible
- `prosada/manifest.json` — your project root config

Special case:
- `prosada/AGENTS.md` is managed in a layered way:
  - managed top section is refreshed by tooling
  - local section (`Local Story Repo Additions`) is preserved
- Any prose `.md` files

---

## Rollout Update Contract (for engine updates)

When ProsAda engine behavior changes, verify in this order:

1. Read latest patch note in `docs/patch-notes/`.
2. Refresh managed assets:
   - `python scripts/check_tooling_health.py --heal`
3. Re-check schema guidance in:
   - `AGENT_START_HERE.md`
   - `PROTOCOL_RULES.md`
   - `FORMAT_CHEATSHEET.md`
4. Re-run validation/doctor before continuing authoring.

Patch notes are the canonical changelog. If behavior differs from prior runs,
do not assume old docs/scripts still apply.
"""


# ---------------------------------------------------------------------------
# E. Patch Notes
# ---------------------------------------------------------------------------

_PATCH_NOTES_INDEX = """\
# ProsAda Patch Notes

> **Managed by ProsAda tooling** · Version {version}

This folder contains versioned engine/tooling update notes distributed into
external repos so local agents can detect behavior changes quickly.

Latest entries:

- `engine-1.10.9.md` — provider-agnostic TTS adapters: live voice discovery, saved voice favorites, and `flat` vs `emoted` cue mode
- `engine-1.10.8.md` — OpenAI TTS workflow: project-scoped keyring keys, beat-marker scrubbing, chunked playback controls
- `engine-1.10.7.md` — explicit beat prose bookend markers (`start`/`end`) + parser compatibility guidance
- `engine-1.10.6.md` — scene-resolution bars + optional prose beat-boundary marker convention (`[[[beat-id|Beat Name]]]`)
- `engine-1.10.5.md` — optional guidance taxonomy namespace (`guidance.kind`, `guidance.tags`) for theory/ethos units
- `engine-1.10.4.md` — canonical schema contract cleanup, semantic link validation, and inherited guidance resolution
- `engine-1.10.3.md` — protocol rules doc (`PROTOCOL_RULES.md`) added as non-AGENTS enforcement surface
- `engine-1.10.2.md` — layered `prosada/AGENTS.md` (managed top + preserved local additions)
- `engine-1.10.1.md` — local append hook for AGENT_START_HERE (`AGENT_START_HERE.local.md`)
- `engine-1.10.0.md` — drift-prevention protocol, prose wiring convention, theory lock default guidance
- `engine-1.9.0.md` — assembled prose projection with boundary overlays and segment-to-unit edit routing
- `engine-1.8.1.md` — deterministic KEEP resolution, lock confidence metadata, merge-request KEEP conflict guard
- `engine-1.8.0.md` — prose overlay artifacts (locks/variants/merge requests) + KEEP guardrail
- `engine-1.7.0.md` — theory lock semantics + prose pagination overlay (phase-1)
- `engine-1.6.0.md` — reusable theory/ethos unit primitives + attachment links
- `engine-1.5.0.md` — connective units + prose editing workflow surfaces
- `engine-1.4.0.md` — planning instrumentation schema + rollout update contract
- `engine-1.3.1.md` — stream owner-lane rendering policy + interaction sanity
- `engine-1.3.0.md` — strict-pins foundation + distributed runtime improvements
"""


_PATCH_NOTES_ENGINE_160 = """\
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
"""


_PATCH_NOTES_ENGINE_170 = """\
# Patch Notes — engine-1.7.0

Date: 2026-03-02
Scope: theory lock semantics + prose pagination overlay (phase-1)

## Summary

This release introduces explicit theory/ethos stability semantics and adds
prose pagination overlay controls in the editor for page-feel review.

## Added

- Theory/ethos structure fields:
  - `doctrineStatus`: `open` | `leaning` | `approved`
  - `mutationLock`: `mutable` | `soft_locked` | `hard_locked`
- Hard-lock save guardrail:
  - hard-locked theory/ethos units reject normal save requests unless explicit override is used.
- Prose editor controls:
  - overlay mode selector (phase-1 scaffold)
  - pagination profile selector (`document`, `paperback`)
  - page-mode viewer with visible page boundaries and computed page numbers.

## Story Agent Guidance

- Use `doctrineStatus` for confidence/approval.
- Use `mutationLock` to control editability independent of doctrine confidence.
- For stable doctrine objects, set `mutationLock: "hard_locked"` after approval.
"""


_PATCH_NOTES_ENGINE_180 = """\
# Patch Notes — engine-1.8.0

Date: 2026-03-02
Scope: prose overlay artifacts (locks/variants/merge requests) + KEEP guardrail

## Summary

This release adds durable prose overlay artifacts and first-pass variant/merge
planning support, with hard KEEP-span protection during prose saves.

## Added

- New prose overlay endpoints:
  - `GET /v2/prose-overlay/{unitId}`
  - `POST /v2/prose-overlay/{unitId}`
- Overlay artifact storage under:
  - `prose_overlays/{unitId}.json`
- Overlay schema fields:
  - `locks[]`
  - `variants[]`
  - `mergeRequests[]`
  - `audio`
- Unit editor UI (phase-1):
  - lock directives from selected spans
  - variant creation from selected spans
  - merge request artifact creation from selected variants.

## Changed

- `POST /v2/prose/{unitId}` now enforces KEEP lock integrity:
  - unresolved KEEP spans block save with conflict response
  - resolved KEEP spans are re-anchored after successful save.

## Story Agent Guidance

- Use prose overlays for review directives and variant planning.
- Keep canonical prose clean; store revision control metadata in overlay artifacts.
"""


_PATCH_NOTES_ENGINE_181 = """\
# Patch Notes — engine-1.8.1

Date: 2026-03-02
Scope: prose lock/merge safety hardening

## Summary

This release hardens KEEP lock resolution and merge-request validation so prose
revision workflows fail safely when anchors drift or conflict.

## Added

- Deterministic KEEP lock resolution outcomes:
  - explicit failure reasons (`TEXT_EMPTY`, `TEXT_NOT_FOUND`, `ANCHOR_MISMATCH`, `AMBIGUOUS_MATCH`)
  - ambiguous matches now fail instead of guessing.
- Per-lock resolution metadata persisted after save:
  - `resolvedBy` (`index` | `anchors` | `unique_text`)
  - `resolutionConfidence` (`high` | `degraded`)
  - `lastResolvedAt`
  - `ambiguityCount`
- Save response warnings:
  - `KEEP_REANCHORED_DEGRADED` when fallback re-anchoring is used.

## Changed

- `POST /v2/prose-overlay/{unitId}` now rejects merge requests that overlap
  KEEP lock ranges (`MERGE_REQUEST_KEEP_CONFLICT`).
- `POST /v2/prose/{unitId}` now validates merge-request/KEEP overlap before write.
- Unit editor now:
  - blocks merge-request creation when selected range overlaps KEEP spans
  - surfaces degraded KEEP re-anchor warnings after save
  - displays lock resolution metadata in the lock list.

## Story Agent Guidance

- Treat degraded KEEP warnings as review-required signals.
- Re-anchor or adjust locks when ambiguity conflicts are reported.
- Keep merge regions carved around hard KEEP spans.
"""


_PATCH_NOTES_ENGINE_1105 = """\
# Patch Notes — engine-1.10.5

Date: 2026-03-05
Scope: soft guidance taxonomy namespace for theory/ethos units

## Summary

This release adds a lightweight, optional taxonomy layer for guidance artifacts
without expanding top-level unit types.

## Added

- Optional `unit.guidance` namespace in canonical schema:
  - `guidance.kind?: string`
  - `guidance.tags?: string[]`
- Writing/editor guidance displays now surface `guidance.kind` when present.

## Changed

- Validator adds warning-only checks for obviously bad guidance metadata shape:
  - guidance on non-theory/non-ethos units
  - blank `guidance.kind`
  - empty tag values
- Managed docs now document recommended (soft) `guidance.kind` vocabulary.
- Managed docs pack bumped to `1.10.5`.

## Story Agent Guidance

- Keep top-level `type` values (`theory`, `ethos`) stable.
- Use `guidance.kind` as the first-stop flexible classification layer.
- Treat recommended vocabulary as conventions, not hard limits.
"""


_PATCH_NOTES_ENGINE_1106 = """\
# Patch Notes — engine-1.10.6

Date: 2026-03-06
Scope: sub-scene beat boundary ergonomics across bars/outline/prose

## Summary

This release keeps high-level bars readable while preserving sub-scene beat
boundary detail in outline and prose workflows.

## Added

- Optional prose beat-boundary marker convention:
  - `[[[beat-id|Beat Name]]]`
- Writing/editor surfaces can show beat-boundary context from prose markers.

## Changed

- Canvas stream/spine bars and beat strip now default to scene-resolution
  presentation (beat-level pills are hidden there).
- Outline supports expansion/collapse so beat units are visible when expanded
  under scenes.
- Read-oriented prose surfaces may hide marker tokens while preserving boundary
  context metadata.
- Managed docs pack bumped to `1.10.6`.

## Story Agent Guidance

- Use beat markers when sub-scene boundaries in prose need machine-readable
  anchors.
- Keep marker syntax stable (`[[[id|label]]]`) for parser interoperability.
- Hidden markers in read view are display behavior only, not source deletion.
"""


_PATCH_NOTES_ENGINE_1107 = """\
# Patch Notes — engine-1.10.7

Date: 2026-03-06
Scope: explicit prose beat-boundary bookend semantics

## Summary

This update formalizes beat markers in prose as explicit start/end bookends so
sub-scene boundaries are unambiguous for agents and tools.

## Changed

- Recommended marker contract now uses explicit boundaries:
  - `[[[beat-id|Beat Name|start]]]`
  - `[[[beat-id|Beat Name|end]]]`
- Parser compatibility guidance:
  - markers without boundary suffix are treated as legacy point markers
  - new bookend syntax is preferred for deterministic range parsing
- Managed docs pack bumped to `1.10.7`.

## Story Agent Guidance

- For new beat annotations, always write paired `start` + `end` markers with
  the same beat ID.
- Keep existing legacy markers only as transitional data; migrate when touched.
"""


_PATCH_NOTES_ENGINE_1108 = """\
# Patch Notes — engine-1.10.8

Date: 2026-03-06
Scope: OpenAI TTS integration for prose workflows

## Summary

This release adds app-level text-to-speech for prose editing/review with
project-scoped API key storage and safe chunked playback orchestration.

## Added

- Backend TTS endpoints:
  - `GET /v2/tts/config`
  - `POST /v2/tts/api-key`
  - `DELETE /v2/tts/api-key`
  - `POST /v2/tts/speak`
- Per-project key isolation:
  - OpenAI API keys are stored in machine keyring slots scoped by active
    project ID (so keys do not collide across story projects).
- Beat marker sanitation:
  - `POST /v2/tts/speak` strips prose beat markers (`[[[...]]]`) before sending
    text to OpenAI.
- Frontend prose surfaces:
  - voice selector, speed control, format selector, optional instructions
  - listen selection / listen unit / listen scope controls
  - pause, resume, stop controls
  - prefetch chunk orchestration for longer prose playback

## Story Agent Guidance

- Keep beat markers in source prose for machine readability; TTS playback now
  scrubs them automatically.
- Keep requests chunked; do not attempt single-call full-manuscript synthesis.
"""


_PATCH_NOTES_ENGINE_1109 = """\
# Patch Notes — engine-1.10.9

Date: 2026-03-06
Scope: provider-agnostic TTS cues + voices workflow

## Summary

This release expands TTS into a provider-agnostic protocol with audio-cue
adaptation control and resilient voice selection workflow.

## Added

- New endpoint:
  - `GET /v2/tts/voices` for provider voice discovery (`openai` static list,
    `elevenlabs` live account voices via API key)
- TTS cue mode:
  - `cueMode=flat` strips prose metadata markers before synthesis
  - `cueMode=emoted` adapts `[[[audio|...]]]` cues per provider/model
- ElevenLabs/OpenAI adapter behavior:
  - OpenAI: converts audio cues into delivery instructions
  - ElevenLabs `eleven_v3`: converts audio cues into inline expressive tags
  - ElevenLabs non-v3 models: cues become instruction hints with clean text
- Voice workflow upgrades:
  - voice finder search/load flow
  - saved voice favorites per provider
  - favorites persistence through workspace preferences + local fallback
- Character voice routing:
  - narrator + character voice assignment mapping
  - in-prose speaker markers route chunks to assigned voices and stitch playback

## Story Agent Guidance

- Keep prose clean and reader-first.
- Use hidden metadata markers for expressive intent:
  - `[[[audio|style=whisper|start]]]`
  - `[[[audio|emotion=excited|point]]]`
  - `[[[audio|style=whisper|end]]]`
- Use speaker markers for auto voice routing:
  - `[[[speaker|character-id|start]]]`
  - `[[[speaker|character-id|end]]]`
- Continue using beat markers (`[[[beat-...]]]`) for structural boundaries.
- Use `flat` mode for neutral pass listening and `emoted` mode for
  audiobook-preview listening.
"""


_PATCH_NOTES_ENGINE_1104 = """\
# Patch Notes — engine-1.10.4

Date: 2026-03-05
Scope: canonical schema contract cleanup + semantic link validation + inherited guidance resolution

## Summary

This release removes stale schema guidance, hardens link semantics, and makes
theory/ethos guidance inheritance explicit in writing/editor surfaces.

## Added

- Validator semantic checks for unit links:
  - `usesTheory` target must be `theory` (warning when mismatched)
  - `usesEthos` target must be `ethos` (warning when mismatched)
  - `merges-into` / `branches-from` / `intersects` require `stream` source+target (error on mismatch)
- Writing/editor guidance resolution now includes ancestor inheritance with
  provenance (direct vs inherited source scope).

## Changed

- Managed docs now state canonical schema as `NarrativeUnit` and describe
  legacy graph primitives as projection compatibility shapes.
- Managed docs now document semantic link rules and inherited guidance behavior.
- Managed docs pack bumped to `1.10.4`.

## Story Agent Guidance

- Treat `usesTheory`/`usesEthos` as typed links, not generic pointers.
- Use top-down doctrine linking at higher scopes; descendants now inherit guidance
  in writing/editor views without link duplication.
- Do not rely on stale `execution` namespace references unless reintroduced by a
  later schema patch note.
"""


_PATCH_NOTES_ENGINE_1103 = """\
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
"""


_PATCH_NOTES_ENGINE_1102 = """\
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
"""


_PATCH_NOTES_ENGINE_1101 = """\
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
"""


_PATCH_NOTES_ENGINE_1100 = """\
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
"""


_PATCH_NOTES_ENGINE_190 = """\
# Patch Notes — engine-1.9.0

Date: 2026-03-02
Scope: assembled prose boundary overlays + provenance-safe edit routing (phase-1)

## Summary

This release adds assembled prose projection for any scope unit (scene/chapter/act/book)
with explicit segment provenance and safe unit-local edit routing from assembled view.

## Added

- New API endpoint:
  - `GET /v2/prose-assembled/{unitId}`
- Assembled prose response includes:
  - `assembledText`
  - `segments[]` with `unitId`, `start`, `end`, title/type, word/page stats
  - scope-level word/page totals
- Unit editor overlay mode `Unit Boundaries` now renders:
  - boundary cards per source segment
  - segment metadata (type/title/range/word/pages)
  - per-segment `Open Unit` action for provenance-safe editing.

## Changed

- Assembled prose is projection-only and read-only in boundary mode.
- Editing from assembled context routes to a single underlying unit editor
  (`Open Unit`) instead of cross-boundary direct mutation.

## Story Agent Guidance

- Use assembled boundary mode for chapter/act pacing review and provenance checks.
- Continue authoring prose canon in unit-local files (`narrative.textRef`).
- Treat assembled view as inspection/navigation, not as canonical write surface.
"""


_PATCH_NOTES_ENGINE_150 = """\
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
"""


_PATCH_NOTES_ENGINE_140 = """\
# Patch Notes — engine-1.4.0

Date: 2026-02-28
Scope: planning instrumentation + docs rollout discipline

## Summary

This release adds optional planning instrumentation primitives to unit schema
and standardizes rollout protocol so schema/docs/tooling stay in sync.

## Added

- Optional `unit.structure` planning block:
  - `functions[]`, `cadenceRole`, `effortLoad`, `planningStatus`
  - typed `rewardTokens[]` (type, strength, description, threadRefs)
  - optional `cadenceEnvelope`
  - optional `modelUpdate`
- Controlled vocab enums for planning fields (documented in cheatsheet).
- Promise registry support:
  - canonical source: `registries/promises.json`
  - typed promise metadata (`promiseType`, target window, state/history)
- Doctor read-only planning warnings:
  - high-effort units without rewards
  - missing promise openers
  - expired chapter-range windows with no movement
  - long chapter runs without reward tokens or promise transitions
  - stream cadence envelopes with no mapped activity

## Changed

- Managed docs now include rollout update protocol guidance.
- External docs pack version bumped to `1.4.0`.

## Why

Story planning needs explicit support for cadence, reward scheduling, and
promise/payoff tracking without forcing immediate canon lock-in.

## Story Agent Guidance

- Use planning metadata as exploratory unless `planningStatus = "locked"`.
- Keep promise contracts in `registries/promises.json` (single canonical location).
- Use typed reward/promise vocab from the cheatsheet to keep doctor diagnostics reliable.
"""


_PATCH_NOTES_ENGINE_131 = """\
# Patch Notes — engine-1.3.1

Date: 2026-02-28
Scope: timeline readability + ownership semantics clarification

## Summary

This update reduces outline/timeline clutter by switching event rendering to a
single-lane ownership policy for stream-affiliated units.

## Changed

- Content events now render on one lane only:
  - If `threadsAdvanced[]` has valid stream IDs, owner = first valid stream ID.
  - Otherwise event renders on spine lane.
- Additional stream memberships remain metadata (`relatedThreadIds`) and do not
  auto-spawn duplicate event pills across multiple stream lanes.
- Default label behavior is now hover-first in the app for cleaner timelines.
- Timeline baseline interaction hitbox was narrowed to reduce selection blocking.

## Why

Previous behavior rendered one copy per stream membership, causing repeated
labels/pills and visual ambiguity in dense outlines.

## Story Agent Guidance

- Keep schema drafting the same (strict pins + hierarchy rules unchanged).
- When assigning multiple streams to a unit, put intended owner first in
  `narrative.threadsAdvanced[]`.
- Use additional stream IDs intentionally for cross-stream semantics, not
  expecting duplicate rendered pills.
"""


_PATCH_NOTES_ENGINE_130 = """\
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
"""


# ---------------------------------------------------------------------------
# Doc file registry
# ---------------------------------------------------------------------------

# Ordered list of (filename, template_string) pairs.
# Add new docs here to have them installed and tracked automatically.
DOC_FILES: list[tuple[str, str]] = [
    ("AGENT_START_HERE.md", _AGENT_START_HERE),
    ("FORMAT_CHEATSHEET.md", _FORMAT_CHEATSHEET),
    ("WORKFLOWS.md", _WORKFLOWS),
    ("PROTOCOL_RULES.md", _PROTOCOL_RULES),
    ("TOOLING.md", _TOOLING),
    ("patch-notes/README.md", _PATCH_NOTES_INDEX),
    ("patch-notes/engine-1.10.9.md", _PATCH_NOTES_ENGINE_1109),
    ("patch-notes/engine-1.10.8.md", _PATCH_NOTES_ENGINE_1108),
    ("patch-notes/engine-1.10.7.md", _PATCH_NOTES_ENGINE_1107),
    ("patch-notes/engine-1.10.6.md", _PATCH_NOTES_ENGINE_1106),
    ("patch-notes/engine-1.10.5.md", _PATCH_NOTES_ENGINE_1105),
    ("patch-notes/engine-1.10.4.md", _PATCH_NOTES_ENGINE_1104),
    ("patch-notes/engine-1.10.3.md", _PATCH_NOTES_ENGINE_1103),
    ("patch-notes/engine-1.10.2.md", _PATCH_NOTES_ENGINE_1102),
    ("patch-notes/engine-1.10.1.md", _PATCH_NOTES_ENGINE_1101),
    ("patch-notes/engine-1.10.0.md", _PATCH_NOTES_ENGINE_1100),
    ("patch-notes/engine-1.9.0.md", _PATCH_NOTES_ENGINE_190),
    ("patch-notes/engine-1.8.1.md", _PATCH_NOTES_ENGINE_181),
    ("patch-notes/engine-1.8.0.md", _PATCH_NOTES_ENGINE_180),
    ("patch-notes/engine-1.7.0.md", _PATCH_NOTES_ENGINE_170),
    ("patch-notes/engine-1.6.0.md", _PATCH_NOTES_ENGINE_160),
    ("patch-notes/engine-1.5.0.md", _PATCH_NOTES_ENGINE_150),
    ("patch-notes/engine-1.4.0.md", _PATCH_NOTES_ENGINE_140),
    ("patch-notes/engine-1.3.1.md", _PATCH_NOTES_ENGINE_131),
    ("patch-notes/engine-1.3.0.md", _PATCH_NOTES_ENGINE_130),
]


def render_doc(template: str) -> str:
    """Render a doc template, injecting the current DOCS_VERSION and managed header."""
    # The template itself already contains the version in the header line.
    # We just do a simple .format() substitution for {version}.
    try:
        return template.format(version=DOCS_VERSION)
    except (KeyError, ValueError):
        # Fallback: return as-is if format fails (shouldn't happen with well-formed templates)
        return template


def get_docs_subdir() -> str:
    return _DOCS_SUBDIR
