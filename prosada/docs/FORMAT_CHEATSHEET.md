# ProsAda Format Cheatsheet

> **Managed by ProsAda tooling** · Version 1.9.0

---

## Unit Basics (units/*.json)

```json
{
  "schemaVersion": "2.0.0",
  "unitId": "scene-the-anomaly",        // stable ID — never change
  "type": "scene",                       // series|book|act|sequence|chapter|connective|scene|beat|arc|theory|ethos|stream
  "title": "The Anomaly",
  "summary": "Ada detects the first echo.",
  "parentId": "chapter-01",             // null for root
  "children": [],                        // ordered child unitIds
  "links": [],                           // explicit unit relationships
  "narrative": {
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
  },
  "structure": {
    "functions": ["setup", "investigation"],
    "cadenceRole": "rise",
    "effortLoad": "medium",
    "planningStatus": "leaning",
    "rewardTokens": [
      {
        "type": "clue",
        "strength": 3,
        "description": "Ada observes a measurable sky inconsistency.",
        "threadRefs": ["stream-anomaly"]
      }
    ],
    "cadenceEnvelope": {
      "intensityPoints": [{"x": 0.0, "y": 0.2}, {"x": 0.35, "y": 0.8}],
      "frequencyTarget": "intermittent",
      "spacingTarget": "every_1_to_2_chapters",
      "planningStatus": "open"
    },
    "modelUpdate": {
      "before": "Likely perceptual glitch",
      "shift": "Possible external anomaly",
      "after": "Needs verification",
      "confidenceDelta": 1
    }
  },
  "view": {
    "canvas": {
      "x": null, "y": null, "collapsed": false,
      "layout": null                     // or StreamLayout (see below)
    }
  }
}
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
"narrative": { "threadsAdvanced": ["stream-yggdrasil-arc"] }

// stream unit:
{ "unitId": "stream-yggdrasil-arc", "type": "stream", "parentId": null }
```

Render ownership policy (app behavior):
- A unit renders on at most one stream lane by default.
- Owner stream = first valid stream ID in `threadsAdvanced[]`.
- Additional stream IDs are metadata (cross-stream semantics), not duplicate pills.

---

## Layout Hints (view.canvas.layout)

Layout pins for canvas rendering. In `strict-pins`, these are required.

```json
"layout": {
  "mode": "manual",               // "auto" = derived | "manual" = use start+span
  "coordinateMode": "absolute",   // "absolute" | "relative"
  "start": 3.0,                   // spine position (absolute) or fraction of parent (relative)
  "span": 2.0                     // width in spine units (absolute) or fraction (relative)
}
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
{
  "schemaVersion": "2.0.0",
  "type": "characters",
  "entries": [
    {
      "id": "joey-valdez",
      "name": "Joey Valdez",
      "description": "Diner regular, grounding confidant.",
      "color": "#e91e63"
    }
  ]
}
```

### Promise registry contract (`registries/promises.json`)

```json
{
  "schemaVersion": "2.0.0",
  "type": "promises",
  "entries": [
    {
      "id": "p-anomaly-nature-01",
      "name": "Nature of anomaly",
      "promiseType": "mystery",
      "planningStatus": "leaning",
      "openedAtUnitId": "chapter-01",
      "targetWindow": { "kind": "chapter_range", "from": 1, "to": 4 },
      "state": "sharpened",
      "history": [
        { "unitId": "chapter-01", "transition": "opened" },
        { "unitId": "chapter-02", "transition": "sharpened" }
      ],
      "paidAtUnitId": null
    }
  ]
}
```

Promise enums:
- `promiseType`: `mystery` | `plot` | `character` | `thematic` | `symbolic`
- `history.transition`/`state`: `opened` | `sharpened` | `reframed` | `delayed` | `partially_paid` | `paid` | `inverted` | `abandoned`

---

## Presentation / Storyboard Metadata (optional, unit.presentation)

Add directorial/cinematic hints for image/video/storyboard workflows.
All fields are optional — existing units without this block are fully valid.

```json
"presentation": {
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
  "extras": {}
}
```

String fields are unconstrained — suggested values are documented but not enforced.
Omit any field you don't need. An empty `{}` block is valid.

See `WORKFLOWS.md` for authoring and export recipes.

---

## Links (unit-to-unit relationships)

```json
"links": [
  { "type": "merges-into",   "targetId": "stream-main" },
  { "type": "branches-from", "targetId": "scene-origin" },
  { "type": "payoffFor",     "targetId": "scene-setup-1" },
  { "type": "setsUp",        "targetId": "scene-payoff-3" },
  { "type": "dependsOn",     "targetId": "scene-prereq" },
  { "type": "usesTheory",    "targetId": "theory-onboarding-low-friction" },
  { "type": "usesEthos",     "targetId": "ethos-reader-trust-no-cheapness" },
  { "type": "intersects",    "targetId": "stream-b" }
]
```
