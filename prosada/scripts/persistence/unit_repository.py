"""
Unit Repository — v2 Persistence Layer

Reads and writes individual NarrativeUnit files from the project/ folder.
Each unit is its own JSON file. The filename is a human-readable label;
the stable identity is the unitId field inside the file.

Project structure:
    project/
        manifest.json
        units/
            book-01-prose-ada.json
            act-01-the-signal.json
            scene-the-anomaly.json
            scene-the-anomaly.md     <- prose content (external)
        registries/
            characters.json
            locations.json
            threads.json
            ...
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime, timezone

from domain.narrative_unit import NarrativeUnit
from domain.v2_registry import RegistryFile, RegistryType


class UnitRepository:
    """
    v2 repository for NarrativeUnit files.

    Filename ↔ identity contract:
      - Filename is a human-readable label (e.g., scene-the-anomaly.json)
      - unitId inside the file is the stable address used in cross-references
      - On load, the repo scans all *.json files in units/ and builds an index:
        { unitId -> filepath }
      - Renames are safe: unitId inside the file never changes

    The cached index is rebuilt on load_all_units() and lazily on first access.
    Call invalidate_index() if external tools modify the units/ folder.
    """

    SCHEMA_VERSION = "2.0.0"

    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)
        self.units_dir = self.project_dir / "units"
        self.registries_dir = self.project_dir / "registries"
        self._unit_index: Optional[Dict[str, Path]] = None

    # ------------------------------------------------------------------
    # Manifest
    # ------------------------------------------------------------------

    def load_manifest(self) -> dict:
        """Load project/manifest.json. Returns empty dict if not found."""
        path = self.project_dir / "manifest.json"
        if not path.exists():
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_manifest(self, manifest: dict) -> None:
        """Save project/manifest.json."""
        self.project_dir.mkdir(parents=True, exist_ok=True)
        path = self.project_dir / "manifest.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

    # ------------------------------------------------------------------
    # Unit index
    # ------------------------------------------------------------------

    def _build_index(self) -> Dict[str, Path]:
        """
        Scan units/ and build { unitId: filepath } mapping.
        Files that are missing a unitId or are malformed JSON are skipped.
        """
        index: Dict[str, Path] = {}
        if not self.units_dir.exists():
            return index
        for path in sorted(self.units_dir.glob("*.json")):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                unit_id = data.get("unitId")
                if unit_id:
                    index[unit_id] = path
            except (json.JSONDecodeError, OSError):
                pass  # Malformed or unreadable file — skip silently
        return index

    def _get_index(self, force_rebuild: bool = False) -> Dict[str, Path]:
        if self._unit_index is None or force_rebuild:
            self._unit_index = self._build_index()
        return self._unit_index

    def invalidate_index(self) -> None:
        """Force the next access to rebuild the unit index from disk."""
        self._unit_index = None

    # ------------------------------------------------------------------
    # Units — read
    # ------------------------------------------------------------------

    def load_unit(self, unit_id: str) -> Optional[NarrativeUnit]:
        """Load a single unit by its unitId. Returns None if not found."""
        path = self._get_index().get(unit_id)
        if not path or not path.exists():
            return None
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return NarrativeUnit(**data)

    def load_all_units(self) -> Dict[str, NarrativeUnit]:
        """
        Load every unit in units/.
        Returns { unitId: NarrativeUnit }.
        Always rebuilds the index so callers see fresh disk state.
        """
        index = self._get_index(force_rebuild=True)
        units: Dict[str, NarrativeUnit] = {}
        for unit_id, path in index.items():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                units[unit_id] = NarrativeUnit(**data)
            except Exception:
                pass  # Malformed unit — skip, don't crash the full load
        return units

    # ------------------------------------------------------------------
    # Units — write
    # ------------------------------------------------------------------

    def save_unit(self, unit: NarrativeUnit) -> Path:
        """
        Save a unit to its file using an atomic write (temp file + os.replace).

        If the unit already has a known file in the index, write there (preserving
        any human-chosen filename). Otherwise create a new file named after unitId.

        Atomicity guarantee: os.replace() is POSIX-atomic (rename syscall). A
        crashed write leaves the old file intact; it never produces a half-written
        target. This is the per-file guarantee. Cross-file atomicity (all-or-nothing
        for a batch) is not provided here; ops callers must treat a failed batch
        as a signal to re-run /v2/validate and repair.
        """
        self.units_dir.mkdir(parents=True, exist_ok=True)
        index = self._get_index()
        path = index.get(unit.unit_id)
        if not path:
            path = self.units_dir / f"{unit.unit_id}.json"

        data = unit.model_dump(by_alias=True)

        # Write to a temp file in the same directory, then rename atomically.
        # Same-directory placement ensures rename stays on the same filesystem.
        fd, tmp_path_str = tempfile.mkstemp(
            dir=path.parent, suffix=".tmp", prefix=f".{unit.unit_id}."
        )
        tmp_path = Path(tmp_path_str)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            tmp_path.replace(path)   # atomic on POSIX; overwrites target if exists
        except Exception:
            tmp_path.unlink(missing_ok=True)
            raise

        # Keep index current
        index[unit.unit_id] = path
        return path

    def delete_unit(self, unit_id: str) -> bool:
        """Delete a unit file. Returns True if the file existed and was deleted."""
        index = self._get_index()
        path = index.get(unit_id)
        if path and path.exists():
            path.unlink()
            del index[unit_id]
            return True
        return False

    # ------------------------------------------------------------------
    # Registries
    # ------------------------------------------------------------------

    def load_registry(self, registry_type: RegistryType) -> Optional[RegistryFile]:
        """Load project/registries/{type}.json. Returns None if not found."""
        path = self.registries_dir / f"{registry_type.value}.json"
        if not path.exists():
            return None
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return RegistryFile(**data)

    def save_registry(self, registry: RegistryFile) -> None:
        """Save project/registries/{type}.json."""
        self.registries_dir.mkdir(parents=True, exist_ok=True)
        path = self.registries_dir / f"{registry.type.value}.json"
        data = registry.model_dump(by_alias=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_all_registries(self) -> Dict[str, RegistryFile]:
        """Load all registry files that exist. Returns { type_string: RegistryFile }."""
        result: Dict[str, RegistryFile] = {}
        for registry_type in RegistryType:
            rf = self.load_registry(registry_type)
            if rf is not None:
                result[registry_type.value] = rf
        return result

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
