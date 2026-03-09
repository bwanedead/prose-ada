"""
Legacy Timeline Service (Projection Path)

Manages the legacy in-memory graph used by compatibility canvas workflows.
Canonical persisted story authoring uses NarrativeUnit services/endpoints.
"""

from typing import Dict, List, Optional
from domain.primitives import StoryGraph, Timeline, StoryEvent, Thread, EventType, Character, ThreadType

class TimelineService:
    def __init__(self):
        self.graph = StoryGraph()
        # In a real app, load from persistence here

    def create_timeline(self, name: str, lane_id: int = 0) -> Timeline:
        import uuid
        tl_id = f"tl_{uuid.uuid4().hex[:8]}"
        timeline = Timeline(id=tl_id, name=name, lane_id=lane_id)
        self.graph.timelines[tl_id] = timeline
        return timeline

    def add_event(self, title: str, timeline_id: str, position: float) -> StoryEvent:
        import uuid
        ev_id = f"ev_{uuid.uuid4().hex[:8]}"
        event = StoryEvent(
            id=ev_id,
            title=title,
            position=position,
            timeline_id=timeline_id
        )
        self.graph.events[ev_id] = event
        return event

    def add_character(self, name: str, color: str = "#CCCCCC") -> Character:
        import uuid
        char_id = f"c_{uuid.uuid4().hex[:8]}"
        character = Character(id=char_id, name=name, color=color)
        self.graph.characters[char_id] = character
        return character

    def add_thread(self, name: str, color: str) -> Thread:
        import uuid
        th_id = f"th_{uuid.uuid4().hex[:8]}"
        thread = Thread(id=th_id, name=name, color=color, type=ThreadType.OTHER)
        self.graph.threads[th_id] = thread
        return thread

    def get_full_graph(self) -> dict:
        return self.graph.model_dump(by_alias=True)
