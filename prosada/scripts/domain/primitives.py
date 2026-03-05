"""
Legacy Graph Projection Primitives (Canvas Compatibility)

These models are not the canonical persisted story schema.
Canonical story authoring lives in backend/domain/narrative_unit.py.
This file remains as a projection/adapter contract for legacy graph/canvas paths.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

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
    subject_id: str = Field(..., description="Character ID or 'reader'")
    fact_id: str = Field(..., description="ID of the fact/event known")
    state: KnowledgeStateEnum = Field(default=KnowledgeStateEnum.UNKNOWN)
    acquired_at_event_id: Optional[str] = None

class Timeline(BaseModel):
    """
    Primitive 1: Timeline / Continuum
    A narrative axis that supports arbitrary branching/merging.
    """
    id: str = Field(..., description="Unique ID (e.g., 'tl_main')")
    name: str = Field(..., description="Human-readable name")
    type: TimelineType = Field(default=TimelineType.LINEAR)
    parent_id: Optional[str] = Field(default=None, description="Parent timeline ID if branched")
    root_event_id: Optional[str] = Field(default=None, description="Event ID where this timeline originates")
    
    # Visual/Meta
    lane_id: int = Field(default=0, description="Vertical visual stack order")
    is_visible: bool = Field(default=True)

class StoryEvent(BaseModel):
    """
    Primitive 2: Event / Node
    An atomic unit of narrative change.
    """
    id: str = Field(..., description="Unique ID (e.g., 'ev_001')")
    title: str
    summary: str = ""
    
    # Positioning
    position: float = Field(..., description="Global narrative order index")
    duration: float = Field(default=1.0, description="Relative visual duration/weight")
    
    # Graph Connections
    timeline_id: str = Field(..., description="Primary timeline location")
    related_thread_ids: List[str] = Field(default_factory=list, description="Threads affected by this event")
    character_ids: List[str] = Field(default_factory=list, description="Characters present/involved")
    
    # Knowledge Updates
    knowledge_updates: List[KnowledgeState] = Field(default_factory=list, description="Knowledge state changes occurring here")

    # Meta
    type: EventType = Field(default=EventType.BEAT)
    is_resolved: bool = Field(default=False)
    
    # Fluid Layout State (Optional persistence)
    x: Optional[float] = None
    y: Optional[float] = None

class Thread(BaseModel):
    """
    Primitive 3: Thread / Arc
    Continuity of concern across events.
    """
    id: str = Field(..., description="Unique ID (e.g., 'th_hero_arc')")
    name: str
    type: ThreadType = Field(default=ThreadType.OTHER)
    color: str = Field(default="#888888", description="Hex color code")
    is_visible: bool = Field(default=True)
    
    # Relationships
    parent_thread_id: Optional[str] = None
    related_character_ids: List[str] = Field(default_factory=list)
    
class StoryGraph(BaseModel):
    """
    The complete story topology.
    """
    timelines: Dict[str, Timeline] = Field(default_factory=dict)
    events: Dict[str, StoryEvent] = Field(default_factory=dict)
    threads: Dict[str, Thread] = Field(default_factory=dict)
    characters: Dict[str, Character] = Field(default_factory=dict)
