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
