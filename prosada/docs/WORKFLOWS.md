# ProsAda Workflows

> **Managed by ProsAda tooling** · Version 1.4.0
> Recipe-style task guide for agents working with ProsAda projects.

---

## Create a new chapter unit

1. Choose a stable `unitId` (kebab-case, e.g. `chapter-02-the-signal`).
2. Create `units/chapter-02-the-signal.json`:

```json
{
  "schemaVersion": "2.0.0",
  "unitId": "chapter-02-the-signal",
  "type": "chapter",
  "title": "The Signal",
  "summary": "Ada intercepts an anomalous frequency.",
  "parentId": "act-01",
  "children": [],
  "narrative": {
    "status": "draft",
    "threadsAdvanced": [],
    "characters": [],
    "locations": [],
    "textRef": null
  },
  "view": { "canvas": { "x": null, "y": null, "collapsed": false } }
}
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
"narrative": { "threadsAdvanced": ["stream-yggdrasil-arc"] }
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
python prosada/scripts/render_timeline.py \
  --project prosada/ --out snapshot.png

# SVG
python prosada/scripts/render_timeline.py \
  --project prosada/ --out snapshot.svg --format svg

# With metadata sidecar
python prosada/scripts/render_timeline.py \
  --project prosada/ --out snapshot.png --sidecar

# Scope to a subtree
python prosada/scripts/render_timeline.py \
  --project prosada/ --out act1.png --scope act-01

# Filter to specific streams
python prosada/scripts/render_timeline.py \
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
{
  "sourceProjectId": "proj-abc123",
  "targetRepoRootPath": "/path/to/target/repo",
  "registerAndActivate": true
}
```

This copies all units/registries and installs the managed tooling pack at the target.

---

## Generate a projection payload

A projection payload is a normalized JSON document joining layout, unit metadata,
semantic refs, and execution stubs.

```bash
# Write projection JSON to file (repo-local CLI)
python prosada/scripts/render_timeline.py \
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
python prosada/scripts/render_timeline.py \
  --project prosada/ --out semantic.png --overlay semantic

# Semantic overlay — highlight events referencing a specific character
python prosada/scripts/render_timeline.py \
  --project prosada/ --out ada-refs.png \
  --overlay semantic --semantic-kind char --semantic-id ada-lovelace

# Status overlay — tint events by narrative.status (draft/review/locked)
python prosada/scripts/render_timeline.py \
  --project prosada/ --out status.png --overlay status

# Overlay + projection JSON in one command
python prosada/scripts/render_timeline.py \
  --project prosada/ --out out.png \
  --overlay semantic --projection-json projection.json
```

---

## Write a custom overlay script using projection JSON

1. Generate projection JSON:
```bash
python prosada/scripts/render_timeline.py \
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
{
  "unitId": "scene-the-anomaly",
  "narrative": { "status": "draft", "characters": ["ada"] },
  "presentation": {
    "shotType": "establishing",
    "moodTags": ["wonder", "unease"],
    "imagepromptHints": "observatory dome at night, stars visible, eerie blue glow",
    "lightingTags": ["natural", "backlit"]
  }
}
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
python prosada/scripts/render_timeline.py \
  --project prosada/ --out timeline.png --prompt-export packets.json

# With profile
python prosada/scripts/render_timeline.py \
  --project prosada/ --out timeline.png \
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
python prosada/scripts/render_timeline.py \
  --project prosada/ --out mood.png --overlay mood

# Shot type overlay — tint + badge by presentation.shotType
python prosada/scripts/render_timeline.py \
  --project prosada/ --out shot.png --overlay shot

# Combined: shot overlay + export projection JSON
python prosada/scripts/render_timeline.py \
  --project prosada/ --out shot.png \
  --overlay shot --projection-json projection.json
```

Mood tints: tense=red, wonder=blue, melancholy=purple, dread=dark-violet,
warmth=amber, mystery=slate-teal, hope=green, unease=muddy-gold.
Shot badges: EST / WID / AER / MED / CU / INS / POV / CUT.
Events with no presentation data are dimmed when any other event has data.
