"""
Registry Models — v2

Story bible entries: characters, locations, threads, artifacts, symbols, concepts.
Each type lives in its own file: project/registries/{type}.json

Unit files reference registry entries by id.
Freeform string IDs are allowed during drafting — normalization into a proper
registry entry can happen later without breaking anything.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class RegistryType(str, Enum):
    CHARACTERS = "characters"
    LOCATIONS  = "locations"
    THREADS    = "threads"
    ARTIFACTS  = "artifacts"
    SYMBOLS    = "symbols"
    CONCEPTS   = "concepts"
    PROMISES   = "promises"


class RegistryEntry(BaseModel):
    """A single entry in a story-bible registry."""
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Stable ID used as a reference key in unit files")
    name: str
    description: Optional[str] = None
    notes: Optional[str] = None
    color: Optional[str] = None

    # Type-specific optional fields (sparse schema — only relevant fields populated)
    archetype: Optional[str] = None   # characters
    type: Optional[str] = None        # locations, threads, etc.
    # promise contracts (promises registry)
    promise_type: Optional[str] = Field(default=None, alias="promiseType")
    planning_status: Optional[str] = Field(default=None, alias="planningStatus")
    opened_at_unit_id: Optional[str] = Field(default=None, alias="openedAtUnitId")
    target_window: Optional[dict] = Field(default=None, alias="targetWindow")
    state: Optional[str] = None
    history: Optional[list] = None
    paid_at_unit_id: Optional[str] = Field(default=None, alias="paidAtUnitId")


class RegistryFile(BaseModel):
    """
    A single registry file, e.g. project/registries/characters.json

    schema_version lets us migrate gracefully if the schema evolves.
    """
    model_config = ConfigDict(populate_by_name=True)

    schema_version: str = Field(default="2.0.0", alias="schemaVersion")
    type: RegistryType
    entries: List[RegistryEntry] = Field(default_factory=list)
