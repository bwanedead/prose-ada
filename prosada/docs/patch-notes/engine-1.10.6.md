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
