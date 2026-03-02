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
python prosada/scripts/render_timeline.py \
  --project prosada/ --out timeline.svg --format svg --sidecar

# Scope to one act
python prosada/scripts/render_timeline.py \
  --project prosada/ --out act1.png --scope act-01 --scale 60

# Semantic overlay — highlight events with any semantic refs
python prosada/scripts/render_timeline.py \
  --project prosada/ --out semantic.png --overlay semantic

# Semantic overlay — highlight a specific character
python prosada/scripts/render_timeline.py \
  --project prosada/ --out ada.png \
  --overlay semantic --semantic-kind char --semantic-id ada-lovelace

# Status overlay — tint events by narrative.status
python prosada/scripts/render_timeline.py \
  --project prosada/ --out status.png --overlay status

# Mood overlay — tint by presentation.moodTags[0]
python prosada/scripts/render_timeline.py \
  --project prosada/ --out mood.png --overlay mood

# Shot type overlay — tint + badge by presentation.shotType
python prosada/scripts/render_timeline.py \
  --project prosada/ --out shot.png --overlay shot

# Export projection JSON alongside render
python prosada/scripts/render_timeline.py \
  --project prosada/ --out timeline.png --projection-json projection.json

# Export prompt packets alongside render
python prosada/scripts/render_timeline.py \
  --project prosada/ --out timeline.png --prompt-export packets.json

# Prompt packets with image-concept profile
python prosada/scripts/render_timeline.py \
  --project prosada/ --out timeline.png \
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
| `/v2/prose/{unitId}`          | GET    | Read prose payload for one unit (`content`, `textRef`) |
| `/v2/prose/{unitId}`          | POST   | Write prose payload for one unit                       |
| `/v2/prose-assembled/{unitId}`| GET    | Read assembled prose projection + provenance segments  |
| `/v2/prose-overlay/{unitId}`  | GET    | Read prose overlay artifact (`locks`, `variants`, `audio`) |
| `/v2/prose-overlay/{unitId}`  | POST   | Write prose overlay artifact                               |
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

---

## Rollout Update Contract (for engine updates)

When ProsAda engine behavior changes, verify in this order:

1. Read latest patch note in `docs/patch-notes/`.
2. Refresh managed assets:
   - `python scripts/check_tooling_health.py --heal`
3. Re-check schema guidance in:
   - `AGENT_START_HERE.md`
   - `FORMAT_CHEATSHEET.md`
4. Re-run validation/doctor before continuing authoring.

Patch notes are the canonical changelog. If behavior differs from prior runs,
do not assume old docs/scripts still apply.
