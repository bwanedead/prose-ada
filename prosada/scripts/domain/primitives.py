"""
Legacy Graph Projection Primitives (Canvas Compatibility)

These models are not the canonical persisted story schema.
Canonical story authoring lives in backend/domain/narrative_unit.py.
This file remains as a projection/adapter contract for legacy graph/canvas paths.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

# --- Enums ---

class TimelineType(str, Enum):
    LINEAR = "linear"
    BRANCHING = "branching"
    PARALLEL = "parallel"
    CONVERGENT = "convergent"

class EventType(str, Enum):
    BEAT = "beat"
    SCENE = "scene"
    CHAPTER_BREAK = "chapter_break"
    CONVERGENCE = "convergence"

class ThreadType(str, Enum):
    CHARACTER = "character"
    MYSTERY = "mystery"
    PLOT = "plot"
    THEME = "theme"
    OTHER = "other"

class CheckpointType(str, Enum):
    MILESTONE = "milestone"
    TONAL_SHIFT = "tonal_shift"
    CLIMAX = "climax"
    OTHER = "other"

class KnowledgeStateEnum(str, Enum):
    UNKNOWN = "unknown"
    SUSPECTED = "suspected"
    KNOWN = "known"
    FALSE_BELIEF = "false_belief"

# --- Primitives ---

class Character(BaseModel):
    """
    Primitive 4: Character
    Entity participating in the story.
    """
    id: str = Field(..., description="Unique ID")
    name: str
    archetype: Optional[str] = None
    color: str = "#CCCCCC"

class KnowledgeState(BaseModel):
    """
    Primitive 5: Knowledge / Information State
    Tracks who knows what and when.
    """
    model_config = ConfigDict(populate_by_name=True)

    subject_id: str = Field(..., alias="subjectId", description="Character ID or 'reader'")
    fact_id: str = Field(..., alias="factId", description="ID of the fact/event known")
    state: KnowledgeStateEnum = Field(default=KnowledgeStateEnum.UNKNOWN)
    acquired_at_event_id: Optional[str] = Field(default=None, alias="acquiredAtEventId")

class Timeline(BaseModel):
    """
    Primitive 1: Timeline / Continuum
    A narrative axis that supports arbitrary branching/merging.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Unique ID (e.g., 'tl_main')")
    name: str = Field(..., description="Human-readable name")
    description: Optional[str] = None
    type: TimelineType = Field(default=TimelineType.LINEAR)
    parent_id: Optional[str] = Field(default=None, alias="parentId", description="Parent timeline ID if branched")

    # Position and visual metadata
    position: float = Field(default=0.0, description="Absolute world position")
    duration: float = Field(default=1.0, description="Timeline span in world units")
    lane_id: int = Field(default=0, alias="laneId", description="Vertical visual stack order")
    is_visible: bool = Field(default=True, alias="isVisible")

class StoryEvent(BaseModel):
    """
    Primitive 2: Event / Node
    An atomic unit of narrative change.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Unique ID (e.g., 'ev_001')")
    title: str
    summary: Optional[str] = None
    description: Optional[str] = None

    # Positioning
    position: float = Field(..., description="Global narrative order index")
    relative_position: float = Field(default=0.0, alias="relativePosition", description="Position relative to parent start")
    duration: float = Field(default=1.0, description="Relative visual duration/weight")

    # Graph Connections
    timeline_id: str = Field(..., alias="timelineId", description="Primary timeline location")
    attached_to_id: Optional[str] = Field(default=None, alias="attachedToId")
    lane_id: Optional[int] = Field(default=None, alias="laneId")
    related_thread_ids: List[str] = Field(default_factory=list, alias="relatedThreadIds", description="Threads affected by this event")
    character_ids: List[str] = Field(default_factory=list, alias="characterIds", description="Characters present/involved")

    # Knowledge Updates
    knowledge_updates: List[KnowledgeState] = Field(default_factory=list, alias="knowledgeUpdates", description="Knowledge state changes occurring here")

    # Meta
    type: EventType = Field(default=EventType.BEAT)
    is_resolved: bool = Field(default=False, alias="isResolved")

class Thread(BaseModel):
    """
    Primitive 3: Thread / Arc
    Continuity of concern across events.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Unique ID (e.g., 'th_hero_arc')")
    name: str
    description: Optional[str] = None
    type: ThreadType = Field(default=ThreadType.OTHER)
    color: str = Field(default="#888888", description="Hex color code")
    is_visible: bool = Field(default=True, alias="visible")

    # Positioning
    timeline_id: str = Field(default="", alias="timelineId")
    position: float = 0.0
    duration: float = 1.0
    lane_id: int = Field(default=0, alias="laneId")

    # Narrative lineage
    birth_origin_id: Optional[str] = Field(default=None, alias="birthOriginId")
    merge_target_id: Optional[str] = Field(default=None, alias="mergeTargetId")
    origin_thread_id: Optional[str] = Field(default=None, alias="originThreadId")
    target_thread_id: Optional[str] = Field(default=None, alias="targetThreadId")
    parent_thread_id: Optional[str] = Field(default=None, alias="parentThreadId")

    related_character_ids: List[str] = Field(default_factory=list, alias="relatedCharacterIds")


class Checkpoint(BaseModel):
    """
    Primitive 6: Checkpoint
    Milestones or marker beats attached to a timeline/thread.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Unique checkpoint ID")
    name: str
    description: Optional[str] = None
    position: float = Field(..., description="Absolute world position")
    relative_position: float = Field(default=0.0, alias="relativePosition")

    parent_type: str = Field(..., alias="parentType", description="'timeline' or 'thread'")
    parent_id: str = Field(..., alias="parentId")

    type: CheckpointType = Field(default=CheckpointType.OTHER)
    color: Optional[str] = None
    
class StoryGraph(BaseModel):
    """
    The complete story topology.
    """
    timelines: Dict[str, Timeline] = Field(default_factory=dict)
    events: Dict[str, StoryEvent] = Field(default_factory=dict)
    threads: Dict[str, Thread] = Field(default_factory=dict)
    checkpoints: Dict[str, Checkpoint] = Field(default_factory=dict)
    characters: Dict[str, Character] = Field(default_factory=dict)
