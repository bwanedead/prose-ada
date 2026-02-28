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

DOCS_VERSION = "1.3.0"
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
  "type": "scene",                       // series|book|act|sequence|chapter|scene|beat|arc|stream
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
  "view": {{
    "canvas": {{
      "x": null, "y": null, "collapsed": false,
      "layout": null                     // or StreamLayout (see below)
    }}
  }}
}}
```

---

## Unit Types

| Type       | Role                                              |
|------------|---------------------------------------------------|
| `series`   | Multi-book container (root of a series)           |
| `book`     | Single book (root of a book project)              |
| `act`      | Major structural division                         |
| `sequence` | Mid-level grouping                                |
| `chapter`  | Chapter-level unit                                |
| `scene`    | Scene — primary story beat container              |
| `beat`     | Sub-scene moment                                  |
| `arc`      | Character/thematic arc (cross-cutting)            |
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
  {{ "type": "intersects",    "targetId": "stream-b" }}
]
```
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

## Assign a unit to a stream

1. Find the stream's `unitId` (e.g., `stream-yggdrasil-arc`).
2. In the scene/chapter unit, add to `narrative.threadsAdvanced`:

```json
"narrative": {{ "threadsAdvanced": ["stream-yggdrasil-arc"] }}
```

3. The stream unit itself does **not** need modification.

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
# D. TOOLING.md
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
| `/v2/render/timeline`         | GET    | Render PNG snapshot                              |
| `/v2/render/timeline/svg`     | GET    | Render SVG snapshot                              |
| `/v2/semantic-refs`           | GET    | Query semantic entity references                 |
| `/v2/validate`                | GET    | Validate project integrity                       |

---

## Note on managed vs user-authored files

Only files under `prosada/scripts/` and `prosada/docs/` are managed.
The following are **never touched** by tooling refresh:
- `prosada/units/*.json` — your story structure
- `prosada/registries/*.json` — your story bible
- `prosada/manifest.json` — your project root config
- Any prose `.md` files
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

- `engine-1.3.0.md` — strict-pins foundation + distributed runtime improvements
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
    ("TOOLING.md", _TOOLING),
    ("patch-notes/README.md", _PATCH_NOTES_INDEX),
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
