"""
Workspace Registry — machine-local project list

Stores the list of known ProsAda project roots on this machine.
This file is machine-local and must NOT be committed to git.

Default location: backend/workspace-registry.json
(gitignored — see root .gitignore)

Registry schema v1.1:
    {
        "schemaVersion": "1.1",
        "activeProjectId": "<id or null>",
        "projects": [
            {
                "id": "proj-<uuid>",
                "displayName": "my-project",
                "sourceMode": "local" | "external",
                "repoRootPath": "/abs/path/to/repo",   // null for local projects
                "prosadaPath": "/abs/path/to/prosada",  // always set
                "lastOpenedAt": "2026-02-26T00:00:00Z",
                "isValid": true
            }
        ]
    }

Source modes:
    local    — prosada root lives inside app-managed local storage
               (~/.local/share/prosada/local-projects/<id>/)
    external — prosada root lives at <repoRoot>/prosada/ in a user-chosen
               folder; supports agent workflows and version-controlled repos
"""

import json
import os
import platform
import shutil
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional


SCHEMA_VERSION = "1.1"

# Canonical markers that must exist inside a valid prosada root
PROSADA_REQUIRED_MARKERS = ["manifest.json", "units", "registries"]

# Source modes
SOURCE_LOCAL = "local"
SOURCE_EXTERNAL = "external"


# ---------------------------------------------------------------------------
# Platform-appropriate local projects directory
# ---------------------------------------------------------------------------

def get_local_projects_dir() -> Path:
    """
    Return the machine-local directory where local projects are stored.

    Platform defaults:
        Linux/other: ~/.local/share/prosada/local-projects/
        macOS:       ~/Library/Application Support/prosada/local-projects/
        Windows:     %APPDATA%/prosada/local-projects/

    Backward compatibility:
        If a legacy prose-ada local-projects directory exists and the new
        prosada directory does not, continue using the legacy path.
    """
    system = platform.system()
    if system == "Darwin":
        app_support = Path.home() / "Library" / "Application Support"
        preferred_base = app_support / "prosada"
        legacy_base = app_support / "prose-ada"
    elif system == "Windows":
        appdata = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        preferred_base = appdata / "prosada"
        legacy_base = appdata / "prose-ada"
    else:
        data_home = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
        preferred_base = data_home / "prosada"
        legacy_base = data_home / "prose-ada"

    preferred_dir = preferred_base / "local-projects"
    legacy_dir = legacy_base / "local-projects"
    if legacy_dir.exists() and not preferred_dir.exists():
        return legacy_dir
    return preferred_dir


# ---------------------------------------------------------------------------
# Project entry
# ---------------------------------------------------------------------------

class ProjectEntry:
    def __init__(
        self,
        id: str,
        display_name: str,
        prosada_path: str,
        source_mode: str = SOURCE_EXTERNAL,
        repo_root_path: Optional[str] = None,
        last_opened_at: Optional[str] = None,
        is_valid: bool = False,
    ):
        self.id = id
        self.display_name = display_name
        self.source_mode = source_mode          # 'local' | 'external'
        self.repo_root_path = repo_root_path    # None for local projects
        self.prosada_path = prosada_path
        self.last_opened_at = last_opened_at
        self.is_valid = is_valid

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "displayName": self.display_name,
            "sourceMode": self.source_mode,
            "repoRootPath": self.repo_root_path,
            "prosadaPath": self.prosada_path,
            "lastOpenedAt": self.last_opened_at,
            "isValid": self.is_valid,
        }

    @staticmethod
    def from_dict(d: dict) -> "ProjectEntry":
        return ProjectEntry(
            id=d["id"],
            display_name=d["displayName"],
            source_mode=d.get("sourceMode", SOURCE_EXTERNAL),  # back-compat default
            repo_root_path=d.get("repoRootPath"),
            prosada_path=d["prosadaPath"],
            last_opened_at=d.get("lastOpenedAt"),
            is_valid=d.get("isValid", False),
        )


# ---------------------------------------------------------------------------
# Validation result
# ---------------------------------------------------------------------------

class ValidationResult:
    def __init__(
        self,
        valid: bool,
        missing_markers: List[str],
        parse_errors: List[str],
        schema_version: Optional[str] = None,
        project_id: Optional[str] = None,
        project_name: Optional[str] = None,
    ):
        self.valid = valid
        self.missing_markers = missing_markers
        self.parse_errors = parse_errors
        self.schema_version = schema_version
        self.project_id = project_id
        self.project_name = project_name

    def to_dict(self) -> dict:
        return {
            "valid": self.valid,
            "missingMarkers": self.missing_markers,
            "parseErrors": self.parse_errors,
            "schemaVersion": self.schema_version,
            "projectId": self.project_id,
            "projectName": self.project_name,
        }


# ---------------------------------------------------------------------------
# Validation + initialization helpers (standalone)
# ---------------------------------------------------------------------------

def validate_prosada_root(prosada_path: Path) -> ValidationResult:
    """
    Validate whether a given path contains a valid ProsAda project root.

    A valid root requires manifest.json, units/, registries/.
    Returns a structured ValidationResult.
    """
    missing: List[str] = []
    parse_errors: List[str] = []
    schema_version: Optional[str] = None
    project_id: Optional[str] = None
    project_name: Optional[str] = None

    for marker in PROSADA_REQUIRED_MARKERS:
        if not (prosada_path / marker).exists():
            missing.append(marker)

    manifest_path = prosada_path / "manifest.json"
    if manifest_path.exists():
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            schema_version = manifest.get("schemaVersion")
            project_id = manifest.get("projectId")
            project_name = manifest.get("name")
        except json.JSONDecodeError as e:
            parse_errors.append(f"manifest.json: {e}")
        except OSError as e:
            parse_errors.append(f"manifest.json unreadable: {e}")

    valid = len(missing) == 0 and len(parse_errors) == 0
    return ValidationResult(
        valid=valid,
        missing_markers=missing,
        parse_errors=parse_errors,
        schema_version=schema_version,
        project_id=project_id,
        project_name=project_name,
    )


def initialize_prosada_root(prosada_path: Path, display_name: Optional[str] = None) -> None:
    """
    Create a minimal ProsAda project structure at the given path.
    Creates manifest.json (seed), units/, registries/, and installs managed tooling.
    Does not overwrite an existing manifest.json.
    """
    prosada_path.mkdir(parents=True, exist_ok=True)
    (prosada_path / "units").mkdir(exist_ok=True)
    (prosada_path / "registries").mkdir(exist_ok=True)

    manifest_path = prosada_path / "manifest.json"
    if not manifest_path.exists():
        project_id = f"project-{uuid.uuid4().hex[:8]}"
        manifest = {
            "schemaVersion": "2.0.0",
            "projectId": project_id,
            "name": display_name or prosada_path.parent.name,
            "root": None,
            "createdAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "settings": {
                "layoutPolicy": "legacy-auto",
            },
        }
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

    # Install managed tooling scripts (renderer + tooling.json metadata)
    try:
        from services.tooling_installer import install_tooling
        install_tooling(prosada_path)
    except Exception:
        pass  # tooling install is best-effort; never block project creation


def export_prosada_to(source_prosada: Path, target_prosada: Path) -> None:
    """
    Copy a prosada project from source to target.

    Copies manifest.json, all files in units/, all files in registries/.
    Creates target dirs as needed. Does NOT recursively copy subdirs
    (prose .md files referenced by textRef are currently left in place
    and callers should handle them separately if needed).

    Raises FileExistsError if target_prosada/manifest.json already exists
    — callers must explicitly remove it first if overwrite is intended.
    """
    target_prosada.mkdir(parents=True, exist_ok=True)
    target_units = target_prosada / "units"
    target_regs = target_prosada / "registries"
    target_units.mkdir(exist_ok=True)
    target_regs.mkdir(exist_ok=True)

    manifest_src = source_prosada / "manifest.json"
    manifest_dst = target_prosada / "manifest.json"
    if manifest_dst.exists():
        raise FileExistsError(f"Target already has manifest.json: {manifest_dst}")
    if manifest_src.exists():
        shutil.copy2(manifest_src, manifest_dst)

    for f in (source_prosada / "units").glob("*.json"):
        shutil.copy2(f, target_units / f.name)
    for f in (source_prosada / "units").glob("*.md"):
        shutil.copy2(f, target_units / f.name)
    for f in (source_prosada / "registries").glob("*.json"):
        shutil.copy2(f, target_regs / f.name)

    # Install / refresh managed tooling scripts at the target
    try:
        from services.tooling_installer import install_tooling
        install_tooling(target_prosada)
    except Exception:
        pass  # tooling install is best-effort; never block export


# ---------------------------------------------------------------------------
# WorkspaceRegistry
# ---------------------------------------------------------------------------

class WorkspaceRegistry:
    """
    Persists the machine-local list of known ProsAda projects.

    Supports both local (app-managed storage) and external (user-chosen
    repo root) projects as first-class equal entries.

    Registry file: <backend_dir>/workspace-registry.json (gitignored).
    """

    def __init__(self, registry_path: Path):
        self.registry_path = Path(registry_path)

    # ------------------------------------------------------------------
    # Load / save
    # ------------------------------------------------------------------

    def _load(self) -> dict:
        if not self.registry_path.exists():
            return {
                "schemaVersion": SCHEMA_VERSION,
                "activeProjectId": None,
                "projects": [],
            }
        with open(self.registry_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data: dict) -> None:
        fd, tmp = tempfile.mkstemp(
            dir=self.registry_path.parent,
            suffix=".tmp",
            prefix=".workspace-registry.",
        )
        tmp_path = Path(tmp)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            tmp_path.replace(self.registry_path)
        except Exception:
            tmp_path.unlink(missing_ok=True)
            raise

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------

    def list_projects(self) -> List[ProjectEntry]:
        data = self._load()
        return [ProjectEntry.from_dict(p) for p in data.get("projects", [])]

    def get_active_project_id(self) -> Optional[str]:
        return self._load().get("activeProjectId")

    def get_active_project(self) -> Optional[ProjectEntry]:
        data = self._load()
        active_id = data.get("activeProjectId")
        if not active_id:
            return None
        for p in data.get("projects", []):
            if p["id"] == active_id:
                return ProjectEntry.from_dict(p)
        return None

    def get_project(self, project_id: str) -> Optional[ProjectEntry]:
        data = self._load()
        for p in data.get("projects", []):
            if p["id"] == project_id:
                return ProjectEntry.from_dict(p)
        return None

    # ------------------------------------------------------------------
    # Create local project
    # ------------------------------------------------------------------

    def create_local_project(self, display_name: str) -> ProjectEntry:
        """
        Create a new local project in app-managed storage and register it.

        The project gets its own directory at:
            <local_projects_dir>/<project-id>/

        The project is NOT activated automatically — call activate_project().
        """
        local_dir = get_local_projects_dir()
        project_id = f"proj-{uuid.uuid4().hex[:8]}"
        prosada_path = local_dir / project_id

        initialize_prosada_root(prosada_path, display_name)
        validation = validate_prosada_root(prosada_path)

        entry = ProjectEntry(
            id=project_id,
            display_name=display_name,
            source_mode=SOURCE_LOCAL,
            repo_root_path=None,
            prosada_path=str(prosada_path),
            last_opened_at=None,
            is_valid=validation.valid,
        )
        data = self._load()
        data.setdefault("projects", []).append(entry.to_dict())
        self._save(data)
        return entry

    # ------------------------------------------------------------------
    # Add external project
    # ------------------------------------------------------------------

    def add_project(
        self, repo_root_path: str, display_name: Optional[str] = None
    ) -> "ProjectEntry":
        """
        Add an external project to the registry by its repo root path.

        Validates the <repoRoot>/prosada/ folder.
        Raises ValueError if already registered.
        """
        data = self._load()
        repo_root = Path(repo_root_path).resolve()
        prosada_path = repo_root / "prosada"

        for existing in data.get("projects", []):
            if existing.get("repoRootPath") and Path(existing["repoRootPath"]).resolve() == repo_root:
                raise ValueError(
                    f"Project at '{repo_root_path}' is already registered (id={existing['id']})"
                )

        validation = validate_prosada_root(prosada_path)
        entry = ProjectEntry(
            id=f"proj-{uuid.uuid4().hex[:8]}",
            display_name=display_name or repo_root.name,
            source_mode=SOURCE_EXTERNAL,
            repo_root_path=str(repo_root),
            prosada_path=str(prosada_path),
            last_opened_at=None,
            is_valid=validation.valid,
        )
        data.setdefault("projects", []).append(entry.to_dict())
        self._save(data)
        return entry

    # ------------------------------------------------------------------
    # Remove
    # ------------------------------------------------------------------

    def remove_project(self, project_id: str) -> bool:
        """Remove a project entry. Returns True if it existed."""
        data = self._load()
        before = len(data.get("projects", []))
        data["projects"] = [p for p in data.get("projects", []) if p["id"] != project_id]
        if len(data["projects"]) == before:
            return False
        if data.get("activeProjectId") == project_id:
            data["activeProjectId"] = None
        self._save(data)
        return True

    # ------------------------------------------------------------------
    # Activate
    # ------------------------------------------------------------------

    def activate_project(self, project_id: str) -> "ProjectEntry":
        """
        Set a project as active. Re-validates and updates lastOpenedAt.
        Raises KeyError if project_id is not found.
        """
        data = self._load()
        found = None
        for p in data.get("projects", []):
            if p["id"] == project_id:
                found = p
                break
        if found is None:
            raise KeyError(f"Project '{project_id}' not found in registry")

        prosada_path = Path(found["prosadaPath"])
        validation = validate_prosada_root(prosada_path)
        found["isValid"] = validation.valid
        found["lastOpenedAt"] = (
            datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        )
        data["activeProjectId"] = project_id
        self._save(data)
        return ProjectEntry.from_dict(found)

    # ------------------------------------------------------------------
    # Export local → external
    # ------------------------------------------------------------------

    def export_local_to_external(
        self,
        source_project_id: str,
        target_repo_root: str,
        overwrite: bool = False,
    ) -> "ProjectEntry":
        """
        Export a local project's prosada folder into an external repo root.

        Creates <targetRoot>/prosada/ by copying all files from the local
        project's prosada root.

        overwrite=False (default): raises FileExistsError if a valid prosada
            already exists at the target. Safe default.
        overwrite=True: removes the existing manifest.json first so the copy
            proceeds. Use only on explicit user confirmation.

        Does NOT modify the source project. Returns a new ProjectEntry for
        the exported external project (not yet added to registry — caller decides).
        """
        source_entry = self.get_project(source_project_id)
        if source_entry is None:
            raise KeyError(f"Source project '{source_project_id}' not found")
        if source_entry.source_mode != SOURCE_LOCAL:
            raise ValueError("Only local projects can be exported via this method")

        target_root = Path(target_repo_root).resolve()
        target_prosada = target_root / "prosada"

        # Guard: check existing target
        existing = validate_prosada_root(target_prosada)
        if existing.valid and not overwrite:
            raise FileExistsError(
                f"A valid ProsAda project already exists at {target_prosada}. "
                "Pass overwrite=True to replace it."
            )
        if overwrite and (target_prosada / "manifest.json").exists():
            (target_prosada / "manifest.json").unlink()

        export_prosada_to(Path(source_entry.prosada_path), target_prosada)

        # Build a ProjectEntry for the exported project (caller registers it)
        new_entry = ProjectEntry(
            id=f"proj-{uuid.uuid4().hex[:8]}",
            display_name=source_entry.display_name,
            source_mode=SOURCE_EXTERNAL,
            repo_root_path=str(target_root),
            prosada_path=str(target_prosada),
            last_opened_at=None,
            is_valid=validate_prosada_root(target_prosada).valid,
        )
        return new_entry

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def refresh_validation(self, project_id: str) -> ValidationResult:
        """Re-run validation for a project and update its isValid flag."""
        data = self._load()
        for p in data.get("projects", []):
            if p["id"] == project_id:
                result = validate_prosada_root(Path(p["prosadaPath"]))
                p["isValid"] = result.valid
                self._save(data)
                return result
        raise KeyError(f"Project '{project_id}' not found")
