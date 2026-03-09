# Patch Notes — engine-1.12.0

Date: 2026-03-08
Scope: canonical story guidance document stack protocol

## Summary

This release adds a document-facing guidance protocol so story agents can
resolve a clean, deterministic reading stack for any unit without mixing in
governed story units or operational engine docs.

## Added

- New endpoint:
  - `GET /v2/guidance-doc-stack/{unitId}`
- New managed script:
  - `prosada/scripts/resolve_guidance_doc_stack.py --unit-id <unitId>`
  - supports `--json` and `--prefer-local`
- Document stack semantics:
  - canonical story guidance docs only
  - wrapper/doc de-duplication
  - artifact fallback when no `narrative.textRef` exists
  - deterministic ordering + attachment provenance

## Clarifications

- Structural and document-facing layers are distinct:
  - `/v2/guidance-stack/{unitId}` = structural/provenance governance
  - `/v2/guidance-doc-stack/{unitId}` = canonical readable guidance corpus
- Story guidance stack excludes operational docs:
  - `AGENTS.md`, managed workflow docs, protocol docs, patch notes

## Compatibility Notes

- No canonical schema migration required.
- Existing guidance links (`usesTheory`, `usesEthos`) remain the attachment
  mechanism; document stack is derived at read-time.
