# Engine Handoff — Beat Deletion vs Prose Reconciliation

## Observed Symptom

A beat unit was deleted structurally from `prosada/units/`, and the parent scene's
`children[]` list was updated correctly. However, the scene prose file still
contained the deleted beat's explicit prose span and beat markers.

Concrete case in this repo:
- `beat-02-lamp-lit-room-reveal` was removed from the canonical scene structure.
- `scene-01-false-morning-routine.json` was updated to remove the beat from
  `children[]`.
- The prose file still contained:
  - `[[[beat-02-lamp-lit-room-reveal|Lamp-Lit Room Reveal|start]]]`
  - the deleted beat's prose body
  - `[[[beat-02-lamp-lit-room-reveal|Lamp-Lit Room Reveal|end]]]`

This left the structure layer and prose layer out of sync until the prose span
was manually removed.

## Expected Behavior

When a beat with explicit prose markers is deleted structurally, the authoring
workflow should surface a prose-aware reconciliation step instead of silently
leaving orphaned beat prose behind.

Preferred behavior:
1. Detect matching beat markers in the prose file.
2. Ask the user what to do with the marked prose span.
3. Apply the selected resolution intentionally.

Suggested resolution options:
- remove the marked prose span entirely
- preserve the prose but strip beat markers and leave it unassigned
- preserve the prose as detached draft material flagged as orphaned
- cancel structural deletion if the user wants to keep the beat intact

## Local Workaround Applied

The beat was deleted structurally first, then the orphaned prose span was
manually removed from the markdown file in a separate edit.

## Why Workaround Is Temporary

Manual cleanup works, but it creates avoidable risk:
- prose and structure can drift without immediate visibility
- deleted beats can continue to exist in source prose unnoticed
- authors must remember to reconcile prose manually after structural operations

This is safe at a low level, but not robust or ergonomic for active drafting.

## Requested Engine-Level Fix

Add prose-aware beat reconciliation to structural beat deletion workflows.

At minimum:
- validation/doctor should warn when prose contains beat markers for units that
  no longer exist or are no longer children of the scene

Preferred UX:
- structural beat deletion should detect matching prose spans and offer an
  explicit resolution step before finalizing the edit

Important constraint:
- the engine should preserve the distinction between canonical structure and
  prose artifact content; the requested change is better reconciliation and
  visibility, not merging those layers into one.
