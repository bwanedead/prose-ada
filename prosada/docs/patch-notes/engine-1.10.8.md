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
