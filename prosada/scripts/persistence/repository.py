"""
Story Repository

Handles loading and saving story data from/to JSON files.
"""

import json
from pathlib import Path
from typing import List, Dict, Any

from ..domain import Thread, Scene, Spine, Registry, Book


class StoryRepository:
    """
    Repository for loading and persisting story data.

    Data is stored in repo-local JSON files with stable IDs.
    """

    def __init__(self, data_dir: Path):
        """
        Initialize repository with data directory path.

        Args:
            data_dir: Path to data/ directory
        """
        self.data_dir = Path(data_dir)
        self.spine_dir = self.data_dir / "spine"
        self.scenes_dir = self.data_dir / "scenes"
        self.threads_dir = self.data_dir / "threads"
        self.registries_dir = self.data_dir / "registries"

    def load_spine(self) -> Spine:
        """Load spine from JSON"""
        spine_path = self.spine_dir / "spine.json"

        if not spine_path.exists():
            # Return empty spine
            return Spine(book=Book(
                id="B01",
                title="Untitled",
                summary="",
                acts=[]
            ))

        with open(spine_path, 'r') as f:
            data = json.load(f)

        return Spine(**data['spine'])

    def save_spine(self, spine: Spine) -> None:
        """Save spine to JSON"""
        spine_path = self.spine_dir / "spine.json"
        spine_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "schemaVersion": "1.0.0",
            "spine": spine.model_dump(),
            "metadata": {
                "lastModified": self._get_timestamp()
            }
        }

        with open(spine_path, 'w') as f:
            json.dump(data, f, indent=2)

    def load_threads(self) -> List[Thread]:
        """Load all threads from JSON"""
        threads_path = self.threads_dir / "threads.json"

        if not threads_path.exists():
            return []

        with open(threads_path, 'r') as f:
            data = json.load(f)

        return [Thread(**thread_data) for thread_data in data.get('threads', [])]

    def save_threads(self, threads: List[Thread]) -> None:
        """Save threads to JSON"""
        threads_path = self.threads_dir / "threads.json"
        threads_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "schemaVersion": "1.0.0",
            "threads": [thread.model_dump() for thread in threads],
            "metadata": {
                "lastModified": self._get_timestamp()
            }
        }

        with open(threads_path, 'w') as f:
            json.dump(data, f, indent=2)

    def load_scenes(self) -> List[Scene]:
        """Load all scenes from JSON"""
        scenes_path = self.scenes_dir / "scenes.json"

        if not scenes_path.exists():
            return []

        with open(scenes_path, 'r') as f:
            data = json.load(f)

        return [Scene(**scene_data) for scene_data in data.get('scenes', [])]

    def save_scenes(self, scenes: List[Scene]) -> None:
        """Save scenes to JSON"""
        scenes_path = self.scenes_dir / "scenes.json"
        scenes_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "schemaVersion": "1.0.0",
            "scenes": [scene.model_dump() for scene in scenes],
            "metadata": {
                "lastModified": self._get_timestamp()
            }
        }

        with open(scenes_path, 'w') as f:
            json.dump(data, f, indent=2)

    def load_registry(self) -> Registry:
        """Load registry from JSON"""
        registry_path = self.registries_dir / "registries.json"

        if not registry_path.exists():
            return Registry()

        with open(registry_path, 'r') as f:
            data = json.load(f)

        return Registry(**data.get('registries', {}))

    def save_registry(self, registry: Registry) -> None:
        """Save registry to JSON"""
        registry_path = self.registries_dir / "registries.json"
        registry_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "schemaVersion": "1.0.0",
            "registries": registry.model_dump(),
            "metadata": {
                "lastModified": self._get_timestamp()
            }
        }

        with open(registry_path, 'w') as f:
            json.dump(data, f, indent=2)

    def _get_timestamp(self) -> str:
        """Get current ISO timestamp"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"
