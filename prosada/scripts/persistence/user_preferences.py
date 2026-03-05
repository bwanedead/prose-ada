from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


class UserPreferencesStore:
    """
    Machine-local user preferences for app UI behavior.
    Stored as JSON outside story repos to keep presentation prefs separate
    from canonical story schema/content.
    """

    def __init__(self, path: Path):
        self.path = path

    def load(self) -> Dict[str, Any]:
        if not self.path.exists():
            return {}
        try:
            raw = self.path.read_text(encoding="utf-8")
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return parsed
            return {}
        except Exception:
            return {}

    def save(self, payload: Dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.path.with_suffix(f"{self.path.suffix}.tmp")
        tmp_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
        tmp_path.replace(self.path)

    def get_section(self, section: str) -> Dict[str, Any]:
        prefs = self.load()
        value = prefs.get(section)
        return value if isinstance(value, dict) else {}

    def set_section(self, section: str, value: Dict[str, Any]) -> Dict[str, Any]:
        prefs = self.load()
        prefs[section] = value
        self.save(prefs)
        return value

