# Patch Notes — engine-1.10.9

Date: 2026-03-06
Scope: provider-agnostic TTS cues + voices workflow

## Summary

This release expands TTS into a provider-agnostic protocol with audio-cue
adaptation control and resilient voice selection workflow.

## Added

- New endpoint:
  - `GET /v2/tts/voices` for provider voice discovery (`openai` static list,
    `elevenlabs` live account voices via API key)
- TTS cue mode:
  - `cueMode=flat` strips prose metadata markers before synthesis
  - `cueMode=emoted` adapts `[[[audio|...]]]` cues per provider/model
- ElevenLabs/OpenAI adapter behavior:
  - OpenAI: converts audio cues into delivery instructions
  - ElevenLabs `eleven_v3`: converts audio cues into inline expressive tags
  - ElevenLabs non-v3 models: cues become instruction hints with clean text
- Voice workflow upgrades:
  - voice finder search/load flow
  - saved voice favorites per provider
  - favorites persistence through workspace preferences + local fallback
- Character voice routing:
  - narrator + character voice assignment mapping
  - in-prose speaker markers route chunks to assigned voices and stitch playback

## Story Agent Guidance

- Keep prose clean and reader-first.
- Use hidden metadata markers for expressive intent:
  - `[[[audio|style=whisper|start]]]`
  - `[[[audio|emotion=excited|point]]]`
  - `[[[audio|style=whisper|end]]]`
- Use speaker markers for auto voice routing:
  - `[[[speaker|character-id|start]]]`
  - `[[[speaker|character-id|end]]]`
- Continue using beat markers (`[[[beat-...]]]`) for structural boundaries.
- Use `flat` mode for neutral pass listening and `emoted` mode for
  audiobook-preview listening.
