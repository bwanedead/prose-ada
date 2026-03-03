"""
Tooling Installer — ProsAda Burst 11

Manages installation of the ProsAda managed enablement pack into each project root:

    <prosadaRoot>/scripts/render_timeline.py       — renderer (copied from app source)
    <prosadaRoot>/scripts/check_tooling_health.py  — health checker (rendered from template)
    <prosadaRoot>/docs/AGENT_START_HERE.md         — agent orientation doc
    <prosadaRoot>/docs/FORMAT_CHEATSHEET.md        — schema reference
    <prosadaRoot>/docs/WORKFLOWS.md                — task recipes
    <prosadaRoot>/docs/PROTOCOL_RULES.md           — durable protocol contract
    <prosadaRoot>/docs/TOOLING.md                  — tooling reference
    <prosadaRoot>/tooling.json                     — v2 metadata + checksums

tooling.json v2 schema:
    {
        "toolingSchemaVersion": "2.0",
        "installedAt": "...",
        "capabilities": {
            "rendererPng": true,
            "rendererSvg": true,
            "semanticRefs": true
        },
        "tools": {
            "renderTimeline":     { "version": "...", "installedAt": "...", "scriptPath": "...", "checksum": "..." },
            "checkToolingHealth": { "version": "...", "installedAt": "...", "scriptPath": "...", "checksum": "..." }
        },
        "docs": {
            "AGENT_START_HERE.md":  { "version": "...", "installedAt": "...", "docPath": "...", "checksum": "..." },
            "FORMAT_CHEATSHEET.md": { ... },
            "WORKFLOWS.md":         { ... },
            "PROTOCOL_RULES.md":    { ... },
            "TOOLING.md":           { ... }
        }
    }

Backward compatibility:
    check_tooling_status() returns both the legacy flat shape (Burst 10) AND the
    new v2 nested shape (Burst 11) in a single dict.

    STATUS_PRESENT = "present" is kept as a backward-compat alias for STATUS_OK = "ok".
    The legacy "status" field at the top level uses STATUS_PRESENT when all assets are ok.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import tempfile
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

# ---------------------------------------------------------------------------
# Source paths
# ---------------------------------------------------------------------------

_BACKEND_DIR = Path(__file__).parent.parent
_SOURCE_RENDERER = _BACKEND_DIR / "render_timeline.py"
_SOURCE_DOMAIN_DIR = _BACKEND_DIR / "domain"
_SOURCE_PERSISTENCE_DIR = _BACKEND_DIR / "persistence"
_SOURCE_SERVICES_DIR = _BACKEND_DIR / "services"

TOOLING_SCHEMA_VERSION = "2.0"
_INSTALLED_RENDERER_NAME = "render_timeline.py"
_INSTALLED_HEALTH_SCRIPT_NAME = "check_tooling_health.py"
_SCRIPTS_SUBDIR = "scripts"
_TOOLING_FILE = "tooling.json"
_ROOT_AGENTS_FILE = "AGENTS.md"
_ROOT_AGENTS_LOCAL_HEADER = "## Local Story Repo Additions (Preserved)"

# ---------------------------------------------------------------------------
# Capabilities manifest
# ---------------------------------------------------------------------------

_CAPABILITIES = {
    "rendererPng": True,
    "rendererSvg": True,
    "semanticRefs": True,
    "standaloneRuntime": True,
}

# ---------------------------------------------------------------------------
# Status values
# ---------------------------------------------------------------------------

STATUS_OK = "ok"
STATUS_MISSING = "missing"
STATUS_STALE = "stale"

# Backward-compatibility alias — Burst 10 tests import and compare STATUS_PRESENT
STATUS_PRESENT = "present"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sha256(path: Path) -> str:
    """Compute SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _sha256_bytes(data: bytes) -> str:
    """Compute SHA-256 hex digest of bytes."""
    return hashlib.sha256(data).hexdigest()


def _sha256_tree(root: Path) -> str:
    """
    Compute a stable SHA-256 digest of a directory tree.

    Hash includes relative paths and file bytes for all *.py files.
    """
    h = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix not in {".py"}:
            continue
        rel = str(path.relative_to(root)).replace("\\", "/")
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        h.update(b"\0")
    return h.hexdigest()


def _read_version_from_file(script_path: Path, constant: str = "RENDERER_VERSION") -> Optional[str]:
    """
    Read a VERSION constant from a script file via regex.
    Defaults to RENDERER_VERSION; pass constant= to read other version constants.
    Returns None if not found or unreadable.
    """
    try:
        text = script_path.read_text(encoding="utf-8", errors="ignore")
        m = re.search(
            rf'^{re.escape(constant)}\s*=\s*["\']([^"\']+)["\']',
            text, re.MULTILINE
        )
        if m:
            return m.group(1)
    except OSError:
        pass
    return None


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _load_tooling_json(project_dir: Path) -> dict:
    path = project_dir / _TOOLING_FILE
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _save_tooling_json(project_dir: Path, data: dict) -> None:
    """Atomic write of tooling.json."""
    path = project_dir / _TOOLING_FILE
    fd, tmp = tempfile.mkstemp(dir=project_dir, prefix=".tooling.", suffix=".tmp")
    tmp_path = Path(tmp)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        tmp_path.replace(path)
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise


def _check_asset(project_dir: Path, rel_path: str, stored_checksum: Optional[str]) -> Tuple[str, bool]:
    """
    Check a single managed asset on disk.

    Returns (status, checksum_match):
        status        — STATUS_OK | STATUS_MISSING | STATUS_STALE
        checksum_match — True if file matches stored checksum (or no checksum recorded)
    """
    full_path = project_dir / rel_path
    if not full_path.exists():
        return STATUS_MISSING, False
    if stored_checksum is None:
        return STATUS_OK, True  # no checksum recorded — legacy, treat as ok
    if full_path.is_dir():
        actual = _sha256_tree(full_path)
    else:
        actual = _sha256(full_path)
    match = actual == stored_checksum
    return (STATUS_OK if match else STATUS_STALE), match


def _extract_local_agents_tail(existing: str) -> str:
    """
    Preserve the local story-owned tail from an existing AGENTS.md file.

    If the canonical local header exists, keep only content below it.
    If no header exists, preserve entire existing file as legacy local content.
    """
    if not existing.strip():
        return ""
    marker = f"{_ROOT_AGENTS_LOCAL_HEADER}\n"
    idx = existing.find(marker)
    if idx >= 0:
        tail = existing[idx + len(marker):].lstrip("\r\n")
        return tail
    return "### Imported Legacy Local Content\n\n" + existing.strip() + "\n"


def _render_root_agents(docs_version: str, existing: str = "") -> str:
    """
    Build prosada/AGENTS.md with a managed top section and preserved local tail.
    """
    local_tail = _extract_local_agents_tail(existing)
    managed = f"""# AGENTS.md

## Managed Engine Guidance
- Source: ProsAda tooling pack
- Version: {docs_version}
- Scope: engine-wide behavior/protocol expectations for this story workspace

## Rules
1. Follow `docs/AGENT_START_HERE.md` for orientation.
2. Use `docs/PROTOCOL_RULES.md` for durable engine protocol contracts.
3. Use `docs/WORKFLOWS.md` for task workflows and canonical conventions.
3. Check `docs/patch-notes/` before introducing new local schema conventions.
4. If behavior appears engine-limited, log an engine handoff note under:
   `docs/engine-handoffs/<yyyy-mm-dd>-<slug>.md`.

---

{_ROOT_AGENTS_LOCAL_HEADER}

> This section is story-repo-owned and preserved across tooling refreshes.
> Add local operational rules, reviewer gates, and project-specific constraints here.
"""
    if local_tail.strip():
        return managed.rstrip() + "\n\n" + local_tail.rstrip() + "\n"
    return managed.rstrip() + "\n\n_Add local repo-specific agent rules below._\n"


def _install_runtime_packages(scripts_dir: Path) -> dict:
    """
    Install standalone runtime packages used by render_timeline.py.

    Managed runtime dirs:
      scripts/domain/
      scripts/persistence/
      scripts/services/
    """
    runtime_sources = {
        "domain": _SOURCE_DOMAIN_DIR,
        "persistence": _SOURCE_PERSISTENCE_DIR,
        "services": _SOURCE_SERVICES_DIR,
    }

    runtime_meta: dict = {}
    for name, source_dir in runtime_sources.items():
        if not source_dir.exists():
            continue
        target_dir = scripts_dir / name
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(
            source_dir,
            target_dir,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
        )
        runtime_meta[name] = {
            "version": _read_version_from_file(_SOURCE_RENDERER) or "unknown",
            "installedAt": _now_iso(),
            "scriptPath": f"{_SCRIPTS_SUBDIR}/{name}",
            "checksum": _sha256_tree(target_dir),
        }

    return runtime_meta


# ---------------------------------------------------------------------------
# Public API — Install
# ---------------------------------------------------------------------------

def install_tooling(project_dir: Path) -> dict:
    """
    Install the full ProsAda managed enablement pack into a project root.

    Creates/overwrites:
        scripts/render_timeline.py
        scripts/check_tooling_health.py
        docs/AGENT_START_HERE.md
        docs/FORMAT_CHEATSHEET.md
        docs/WORKFLOWS.md
        docs/PROTOCOL_RULES.md
        docs/TOOLING.md
        docs/patch-notes/*.md
        tooling.json  (v2 schema)

    Safe to call multiple times — always overwrites with the current app version.
    Returns the tooling.json dict written.
    """
    if not _SOURCE_RENDERER.exists():
        # App source not found — skip gracefully (e.g. running from installed copy)
        return {}

    from services.managed_health_script import HEALTH_SCRIPT_VERSION, SCRIPT_CONTENT
    from services.managed_docs import DOC_FILES, DOCS_VERSION, render_doc, get_docs_subdir

    now = _now_iso()
    existing = _load_tooling_json(project_dir)
    first_installed_at = existing.get("installedAt", now)

    # --- scripts/ directory ---
    scripts_dir = project_dir / _SCRIPTS_SUBDIR
    scripts_dir.mkdir(parents=True, exist_ok=True)

    # Install renderer (copied from app source)
    renderer_dst = scripts_dir / _INSTALLED_RENDERER_NAME
    shutil.copy2(_SOURCE_RENDERER, renderer_dst)
    renderer_checksum = _sha256(renderer_dst)
    renderer_version = _read_version_from_file(renderer_dst) or "unknown"

    # Install health script (rendered from template — already formatted)
    health_dst = scripts_dir / _INSTALLED_HEALTH_SCRIPT_NAME
    health_dst.write_text(SCRIPT_CONTENT, encoding="utf-8")
    health_checksum = _sha256(health_dst)

    # Install standalone runtime package dirs required by render script
    runtime_meta = _install_runtime_packages(scripts_dir)

    # --- docs/ directory ---
    docs_dir = project_dir / get_docs_subdir()
    docs_dir.mkdir(parents=True, exist_ok=True)

    docs_meta: dict = {}
    for filename, template in DOC_FILES:
        rendered = render_doc(template)
        doc_dst = docs_dir / filename
        doc_dst.parent.mkdir(parents=True, exist_ok=True)
        doc_dst.write_text(rendered, encoding="utf-8")
        doc_checksum = _sha256(doc_dst)
        docs_meta[filename] = {
            "version": DOCS_VERSION,
            "installedAt": now,
            "docPath": f"{get_docs_subdir()}/{filename}",
            "checksum": doc_checksum,
        }

    # --- root AGENTS.md (managed top + preserved local tail) ---
    root_agents_path = project_dir / _ROOT_AGENTS_FILE
    existing_agents = ""
    if root_agents_path.exists():
        try:
            existing_agents = root_agents_path.read_text(encoding="utf-8")
        except OSError:
            existing_agents = ""
    root_agents_rendered = _render_root_agents(DOCS_VERSION, existing_agents)
    root_agents_path.write_text(root_agents_rendered, encoding="utf-8")

    # --- tooling.json v2 ---
    data = {
        "toolingSchemaVersion": TOOLING_SCHEMA_VERSION,
        "installedAt": first_installed_at,
        "capabilities": dict(_CAPABILITIES),
        "tools": {
            "renderTimeline": {
                "version": renderer_version,
                "installedAt": now,
                "scriptPath": f"{_SCRIPTS_SUBDIR}/{_INSTALLED_RENDERER_NAME}",
                "checksum": renderer_checksum,
            },
            "checkToolingHealth": {
                "version": HEALTH_SCRIPT_VERSION,
                "installedAt": now,
                "scriptPath": f"{_SCRIPTS_SUBDIR}/{_INSTALLED_HEALTH_SCRIPT_NAME}",
                "checksum": health_checksum,
            },
            **{
                f"{name}Runtime": meta
                for name, meta in runtime_meta.items()
            },
        },
        "docs": docs_meta,
    }
    _save_tooling_json(project_dir, data)
    return data


# ---------------------------------------------------------------------------
# Public API — Check
# ---------------------------------------------------------------------------

def check_tooling_status(project_dir: Path) -> dict:
    """
    Check the status of all managed assets in a project.

    Returns a dict combining:
      - New v2 nested structure: overall + scripts{} + docs{}
      - Legacy (v1) flat fields for backward compatibility with Burst 10 tests:
        status, installedVersion, sourceVersion, checksum, checksumMatch

    v2 fields:
        {
            "overall": "ok" | "missing" | "stale",
            "scripts": {
                "renderTimeline":     { "status": ..., "installedVersion": ..., "sourceVersion": ..., "checksumMatch": bool },
                "checkToolingHealth": { "status": ..., "installedVersion": ..., "sourceVersion": ..., "checksumMatch": bool },
            },
            "docs": {
                "AGENT_START_HERE.md": { "status": ..., "installedVersion": ..., "sourceVersion": ..., "checksumMatch": bool },
                ...
            },
        }

    Legacy flat fields (renderTimeline-focused, for Burst 10 backward compat):
        "status":           "present" | "missing" | "stale"
        "installedVersion": renderer installed version (or None)
        "sourceVersion":    renderer source version (or None)
        "checksum":         renderer actual on-disk checksum (or None)
        "checksumMatch":    renderer checksum match bool
    """
    from services.managed_health_script import HEALTH_SCRIPT_VERSION
    from services.managed_docs import DOC_FILES, DOCS_VERSION, get_docs_subdir

    tooling_data = _load_tooling_json(project_dir)
    tools_meta = tooling_data.get("tools", {})
    docs_meta_stored = tooling_data.get("docs", {})

    source_renderer_version = (
        _read_version_from_file(_SOURCE_RENDERER) if _SOURCE_RENDERER.exists() else None
    )

    # --- scripts ---
    scripts_result: dict = {}

    # renderTimeline
    rt_meta = tools_meta.get("renderTimeline", {})
    rt_rel = rt_meta.get("scriptPath", f"{_SCRIPTS_SUBDIR}/{_INSTALLED_RENDERER_NAME}")
    rt_status, rt_checksum_match = _check_asset(project_dir, rt_rel, rt_meta.get("checksum"))
    rt_installed_version = rt_meta.get("version") or _read_version_from_file(project_dir / rt_rel)
    # Version mismatch also triggers stale
    if rt_status == STATUS_OK and source_renderer_version and rt_installed_version != source_renderer_version:
        rt_status = STATUS_STALE
    scripts_result["renderTimeline"] = {
        "status": rt_status,
        "installedVersion": rt_installed_version,
        "sourceVersion": source_renderer_version,
        "checksumMatch": rt_checksum_match,
    }

    # checkToolingHealth
    hs_meta = tools_meta.get("checkToolingHealth", {})
    hs_rel = hs_meta.get("scriptPath", f"{_SCRIPTS_SUBDIR}/{_INSTALLED_HEALTH_SCRIPT_NAME}")
    hs_status, hs_checksum_match = _check_asset(project_dir, hs_rel, hs_meta.get("checksum"))
    hs_installed_version = hs_meta.get("version")
    if hs_status == STATUS_OK and hs_installed_version != HEALTH_SCRIPT_VERSION:
        hs_status = STATUS_STALE
    scripts_result["checkToolingHealth"] = {
        "status": hs_status,
        "installedVersion": hs_installed_version,
        "sourceVersion": HEALTH_SCRIPT_VERSION,
        "checksumMatch": hs_checksum_match,
    }

    # Runtime package dirs (standalone renderer dependencies)
    runtime_source_dirs = {
        "domainRuntime": _SOURCE_DOMAIN_DIR,
        "persistenceRuntime": _SOURCE_PERSISTENCE_DIR,
        "servicesRuntime": _SOURCE_SERVICES_DIR,
    }
    for tool_name, src_dir in runtime_source_dirs.items():
        meta = tools_meta.get(tool_name, {})
        rel = meta.get("scriptPath", f"{_SCRIPTS_SUBDIR}/{tool_name.replace('Runtime', '').lower()}")
        status_val, checksum_ok = _check_asset(project_dir, rel, meta.get("checksum"))
        source_checksum = _sha256_tree(src_dir) if src_dir.exists() else None
        installed_version = meta.get("version")
        if status_val == STATUS_OK and source_checksum and meta.get("checksum") != source_checksum:
            status_val = STATUS_STALE
        scripts_result[tool_name] = {
            "status": status_val,
            "installedVersion": installed_version,
            "sourceVersion": _read_version_from_file(_SOURCE_RENDERER) if _SOURCE_RENDERER.exists() else None,
            "checksumMatch": checksum_ok,
        }

    # --- docs ---
    docs_result: dict = {}
    for filename, _ in DOC_FILES:
        doc_meta = docs_meta_stored.get(filename, {})
        doc_rel = doc_meta.get("docPath", f"{get_docs_subdir()}/{filename}")
        doc_status, doc_checksum_match = _check_asset(project_dir, doc_rel, doc_meta.get("checksum"))
        doc_installed_version = doc_meta.get("version")
        if doc_status == STATUS_OK and doc_installed_version != DOCS_VERSION:
            doc_status = STATUS_STALE
        docs_result[filename] = {
            "status": doc_status,
            "installedVersion": doc_installed_version,
            "sourceVersion": DOCS_VERSION,
            "checksumMatch": doc_checksum_match,
        }

    # --- overall ---
    all_statuses = (
        [v["status"] for v in scripts_result.values()]
        + [v["status"] for v in docs_result.values()]
    )
    if STATUS_MISSING in all_statuses:
        overall = STATUS_MISSING
    elif STATUS_STALE in all_statuses:
        overall = STATUS_STALE
    else:
        overall = STATUS_OK

    # Legacy flat "status": uses STATUS_PRESENT ("present") when ok, for Burst 10 compat
    legacy_status = STATUS_PRESENT if overall == STATUS_OK else overall

    # Legacy "checksum" — actual on-disk checksum of renderer (or None if missing)
    rt_actual_checksum: Optional[str] = None
    rt_full_path = project_dir / rt_rel
    if rt_full_path.exists():
        rt_actual_checksum = _sha256(rt_full_path)

    return {
        # v2 structure
        "overall": overall,
        "scripts": scripts_result,
        "docs": docs_result,
        # v1 backward-compat flat fields (renderTimeline-focused)
        "status": legacy_status,
        "installedVersion": rt_installed_version,
        "sourceVersion": source_renderer_version,
        "checksum": rt_actual_checksum,
        "checksumMatch": rt_checksum_match,
    }


# ---------------------------------------------------------------------------
# Public API — Refresh
# ---------------------------------------------------------------------------

def refresh_tooling(project_dir: Path) -> dict:
    """
    Reinstall the full managed enablement pack and update tooling.json.

    Idempotent: safe to call when already up-to-date.
    Returns { refreshed, before, after, tooling }.
    """
    before = check_tooling_status(project_dir)
    tooling_data = install_tooling(project_dir)
    after = check_tooling_status(project_dir)
    return {
        "refreshed": True,
        "before": before,
        "after": after,
        "tooling": tooling_data,
    }
