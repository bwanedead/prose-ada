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
