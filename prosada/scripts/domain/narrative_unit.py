"""
Narrative Unit — v2 Domain Model

A NarrativeUnit is the single core primitive for the v2 data-first architecture.
Each unit lives in its own file on disk: project/units/{slug}.json

Ordering is determined by the parent's children[] list — never by a float position field.
Narrative content (canonical) is separated from view hints (UI projection).
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class UnitType(str, Enum):
    SERIES   = "series"
    BOOK     = "book"
    ACT      = "act"
    SEQUENCE = "sequence"
    CHAPTER  = "chapter"
    SCENE    = "scene"
    BEAT     = "beat"
    ARC      = "arc"
    STREAM   = "stream"


class UnitStatus(str, Enum):
    DRAFT  = "draft"
    REVIEW = "review"
    LOCKED = "locked"


class PlanningStatus(str, Enum):
    OPEN    = "open"
    LEANING = "leaning"
    LOCKED  = "locked"


class StructureFunction(str, Enum):
    SETUP         = "setup"
    ESCALATION    = "escalation"
    SQUEEZE       = "squeeze"
    RELEASE       = "release"
    PAYOFF        = "payoff"
    CLIMAX        = "climax"
    BRIDGE        = "bridge"
    REVERSAL      = "reversal"
    INVESTIGATION = "investigation"
    AFTERMATH     = "aftermath"


class CadenceRole(str, Enum):
    RISE       = "rise"
    DROP       = "drop"
    PLATEAU    = "plateau"
    SPIKE      = "spike"
    SUSTAIN    = "sustain"
    TRANSITION = "transition"


class EffortLoad(str, Enum):
    LOW    = "low"
    MEDIUM = "medium"
    HIGH   = "high"


class RewardTokenType(str, Enum):
    CLUE          = "clue"
    COMPETENCE    = "competence"
    CONTRADICTION = "contradiction"
    DECISION      = "decision"
    ATMOSPHERE    = "atmosphere"
    EMOTIONAL     = "emotional"
    MODEL_UPDATE  = "model_update"
    REVERSAL      = "reversal"
    HUMOR         = "humor"
    RELATIONAL    = "relational"


class PromiseType(str, Enum):
    MYSTERY   = "mystery"
    PLOT      = "plot"
    CHARACTER = "character"
    THEMATIC  = "thematic"
    SYMBOLIC  = "symbolic"


class PromiseTransition(str, Enum):
    OPENED         = "opened"
    SHARPENED      = "sharpened"
    REFRAMED       = "reframed"
    DELAYED        = "delayed"
    PARTIALLY_PAID = "partially_paid"
    PAID           = "paid"
    INVERTED       = "inverted"
    ABANDONED      = "abandoned"


class PromiseState(str, Enum):
    OPENED         = "opened"
    SHARPENED      = "sharpened"
    REFRAMED       = "reframed"
    DELAYED        = "delayed"
    PARTIALLY_PAID = "partially_paid"
    PAID           = "paid"
    INVERTED       = "inverted"
    ABANDONED      = "abandoned"


# ---------------------------------------------------------------------------
# Links — explicit unit-to-unit relationships
# ---------------------------------------------------------------------------

class LinkType(str, Enum):
    MERGES_INTO   = "merges-into"
    BRANCHES_FROM = "branches-from"
    INTERSECTS    = "intersects"
    PAYOFF_FOR    = "payoffFor"
    SETS_UP       = "setsUp"
    DEPENDS_ON    = "dependsOn"


class UnitLink(BaseModel):
    """A directed relationship from this unit to another unit."""
    model_config = ConfigDict(populate_by_name=True)

    type: LinkType
    target_id: str = Field(..., alias="targetId")
    label: Optional[str] = None


# ---------------------------------------------------------------------------
# View hints — UI projection only, not canonical narrative state
# ---------------------------------------------------------------------------

class StreamLayout(BaseModel):
    """
    Persisted layout hint for a unit's canvas span.

    Coordinates are spine-relative logical units (1 unit = RENDER_SCALE pixels at zoom=1).

    mode field:
        "auto"   → composer derives start+span from member positions (stream default).
        "manual" → start+span override the derived values; both must be present, span > 0.

    coordinateMode field:
        "absolute" (default) → start+span are absolute spine logical units.
        "relative"           → start+span are normalized fractions of the parent unit's
                               resolved span: [0..1] range recommended, but unclamped.
                               absStart = parentStart + start * parentSpan
                               absSpan  = span * parentSpan
                               Falls back to derived if parent unavailable or span <= 0.

    Future-compatible: additional coordinateMode values (e.g. "segment-relative") and
    explicit anchor references reserved for later bursts.
    """
    model_config = ConfigDict(populate_by_name=True)

    mode: str = "auto"
    coordinate_mode: str = Field(default="absolute", alias="coordinateMode")
    start: Optional[float] = None   # spine logical units (absolute) or fraction (relative)
    span: Optional[float] = None    # spine logical units (absolute) or fraction (relative), > 0


class CanvasHints(BaseModel):
    """Optional layout hints for the canvas visualizer."""
    x: Optional[float] = None
    y: Optional[float] = None
    collapsed: bool = False
    layout: Optional[StreamLayout] = None  # stream/thread span hint


class ViewNamespace(BaseModel):
    """Namespace for all UI projection hints. Agents should ignore this."""
    canvas: CanvasHints = Field(default_factory=CanvasHints)


# ---------------------------------------------------------------------------
# Narrative fields — canonical story data
# ---------------------------------------------------------------------------

class NarrativeFields(BaseModel):
    """
    Canonical narrative data for a unit.
    This is the story. Agents and humans edit this.
    """
    model_config = ConfigDict(populate_by_name=True)

    threads_advanced: List[str] = Field(
        default_factory=list,
        alias="threadsAdvanced",
        description="Thread IDs advanced in this unit"
    )
    characters: List[str] = Field(
        default_factory=list,
        description="Character IDs present or involved"
    )
    locations: List[str] = Field(
        default_factory=list,
        description="Location IDs"
    )
    new_info: Optional[str] = Field(
        default=None,
        alias="newInfo",
        description="New information introduced"
    )
    drip_hook: Optional[str] = Field(
        default=None,
        alias="dripHook",
        description="Curiosity hook created for future units"
    )
    payoff_delivered: Optional[str] = Field(
        default=None,
        alias="payoffDelivered",
        description="What payoff or resolution is delivered here"
    )
    beauty_hooks: Optional[str] = Field(
        default=None,
        alias="beautyHooks",
        description="Echoes, rhymes, tiling connections"
    )
    status: UnitStatus = Field(default=UnitStatus.DRAFT)
    text_ref: Optional[str] = Field(
        default=None,
        alias="textRef",
        description="Relative path to external .md prose file"
    )
    notes: Optional[str] = None


# ---------------------------------------------------------------------------
# Planning instrumentation — optional (non-canonical unless planningStatus=locked)
# ---------------------------------------------------------------------------

class RewardToken(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: RewardTokenType
    strength: int = Field(..., ge=1, le=5)
    description: str
    thread_refs: List[str] = Field(default_factory=list, alias="threadRefs")


class ModelUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    before: Optional[str] = None
    shift: Optional[str] = None
    after: Optional[str] = None
    confidence_delta: Optional[float] = Field(default=None, alias="confidenceDelta")


class CadencePoint(BaseModel):
    x: float
    y: float


class CadenceEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    intensity_points: List[CadencePoint] = Field(default_factory=list, alias="intensityPoints")
    frequency_target: Optional[str] = Field(default=None, alias="frequencyTarget")
    spacing_target: Optional[str] = Field(default=None, alias="spacingTarget")
    planning_status: Optional[PlanningStatus] = Field(default=None, alias="planningStatus")


class UnitStructure(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    functions: List[StructureFunction] = Field(default_factory=list)
    cadence_role: Optional[CadenceRole] = Field(default=None, alias="cadenceRole")
    effort_load: Optional[EffortLoad] = Field(default=None, alias="effortLoad")
    planning_status: Optional[PlanningStatus] = Field(default=None, alias="planningStatus")
    reward_tokens: List[RewardToken] = Field(default_factory=list, alias="rewardTokens")
    cadence_envelope: Optional[CadenceEnvelope] = Field(default=None, alias="cadenceEnvelope")
    model_update: Optional[ModelUpdate] = Field(default=None, alias="modelUpdate")


# ---------------------------------------------------------------------------
# Narrative Unit — the core primitive
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Presentation / storyboard metadata — creative directorial hints
# ---------------------------------------------------------------------------

class PresentationMetadata(BaseModel):
    """
    Optional creative/directorial metadata for a unit.

    This is the 'how to present it' layer — storyboard hints for image/video
    generation, cinematic planning, and prompt scaffolding workflows.

    All fields are optional. Missing or invalid values never break unit parsing.
    String fields are unconstrained (no strict enums) — creative freedom is
    more valuable than rigid validation at this layer.

    Namespace: unit.presentation  (top-level, alongside narrative and view)

    Suggested values (not enforced):
      shotType     : establishing | wide | medium | closeup | insert | aerial | pov | cutaway
      cameraAngle  : eye-level | low | high | overhead | dutch
      cameraMotion : static | pan | tilt | dolly | handheld | push-in | pull-out | crane
      moodTags     : tense | wonder | melancholy | dread | warmth | mystery | hope | unease
    """
    model_config = ConfigDict(populate_by_name=True)

    # --- Camera / framing ---
    shot_type: Optional[str] = Field(
        default=None, alias="shotType",
        description="Shot type: establishing|wide|medium|closeup|insert|aerial|pov|cutaway"
    )
    camera_angle: Optional[str] = Field(
        default=None, alias="cameraAngle",
        description="Camera angle: eye-level|low|high|overhead|dutch"
    )
    camera_motion: Optional[str] = Field(
        default=None, alias="cameraMotion",
        description="Camera motion: static|pan|tilt|dolly|handheld|push-in|pull-out|crane"
    )
    framing_notes: Optional[str] = Field(default=None, alias="framingNotes")

    # --- Tone / aesthetic ---
    mood_tags: List[str] = Field(
        default_factory=list, alias="moodTags",
        description="Mood tags: tense|wonder|melancholy|dread|warmth|mystery|hope|unease"
    )
    visual_style_tags: List[str] = Field(default_factory=list, alias="visualStyleTags")
    lighting_tags: List[str] = Field(
        default_factory=list, alias="lightingTags",
        description="Lighting: natural|dramatic|backlit|diffuse|noir|harsh|soft"
    )
    color_palette_tags: List[str] = Field(default_factory=list, alias="colorPaletteTags")

    # --- Composition / emphasis ---
    focus_subject_ids: List[str] = Field(
        default_factory=list, alias="focusSubjectIds",
        description="Registry entity IDs that are the visual focus of this scene"
    )
    composition_notes: Optional[str] = Field(default=None, alias="compositionNotes")
    blocking_notes: Optional[str] = Field(default=None, alias="blockingNotes")

    # --- Production / prompt scaffolding helpers ---
    image_prompt_hints: Optional[str] = Field(
        default=None, alias="imagePromptHints",
        description="Free-text hints for image generation prompts"
    )
    video_prompt_hints: Optional[str] = Field(
        default=None, alias="videoPromptHints",
        description="Free-text hints for video generation prompts"
    )
    continuity_notes: Optional[str] = Field(
        default=None, alias="continuityNotes",
        description="Notes for visual/narrative continuity with adjacent units"
    )

    # --- Generic extension ---
    extras: Dict[str, Any] = Field(
        default_factory=dict,
        description="Flexible key-value extension for custom metadata"
    )


class NarrativeUnit(BaseModel):
    """
    v2 Core Primitive: Narrative Unit

    A single composable chunk of story structure.
    Lives on disk as:  project/units/{slug}.json
    Prose lives at:    project/units/{slug}.md  (referenced by narrative.textRef)

    Identity:  unitId (stable, never changes even if the file is renamed)
    Ordering:  parent's children[] list (not a float position field)
    Hierarchy: parentId field (arbitrary depth)
    """
    model_config = ConfigDict(populate_by_name=True)

    schema_version: str = Field(
        default="2.0.0",
        alias="schemaVersion"
    )
    unit_id: str = Field(
        ...,
        alias="unitId",
        description="Stable internal ID — survives file renames"
    )
    type: UnitType
    title: str
    summary: str = ""

    parent_id: Optional[str] = Field(
        default=None,
        alias="parentId",
        description="unitId of the parent unit, or null for roots"
    )
    children: List[str] = Field(
        default_factory=list,
        description="Ordered list of child unitIds — this is the canonical ordering mechanism"
    )

    links: List[UnitLink] = Field(
        default_factory=list,
        description="Explicit relationships to other units (merges-into, branches-from, etc.)"
    )

    narrative: NarrativeFields = Field(default_factory=NarrativeFields)
    structure: Optional[UnitStructure] = Field(
        default=None,
        description=(
            "Optional planning instrumentation metadata. "
            "Planning-only unless planningStatus='locked'."
        ),
    )
    view: ViewNamespace = Field(default_factory=ViewNamespace)
    presentation: Optional[PresentationMetadata] = Field(
        default=None,
        description=(
            "Optional storyboard/directorial metadata. "
            "Additive — existing units without this field remain fully valid."
        )
    )
