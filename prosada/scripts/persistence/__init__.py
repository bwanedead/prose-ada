"""
Persistence Layer

Loading, saving, and migrating repo-local state.
"""

# v2 persistence (implemented)
from .unit_repository import UnitRepository

# Legacy persistence (repository.py depends on domain models not yet implemented)
#   StoryRepository -> backend/persistence/repository.py

__all__ = ["UnitRepository"]
