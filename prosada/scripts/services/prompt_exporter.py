"""
Prompt Packet Exporter — ProsAda Burst 13

Converts ProsAda project units + presentation metadata into structured
prompt-ready packets for downstream image/video/storyboarding workflows.

No external API calls. Pure structured output (JSON packets).

Profiles
--------
storyboard-basic  (default)
    All fields included: narrative, timeline, semantic, presentation,
    registry slices, and parent context. Full packet for any workflow.

image-concept
    Emphasizes visual/compositional fields:
      - presentation.moodTags, .imagePromptHints, .visualStyleTags, .lightingTags
      - semantic.entityIds + registry name lookups
    Minimizes: timeline details, narrative hooks

narrative-summary
    Emphasizes narrative hooks and intent:
      - narrative.dripHook, .payoffDelivered, .newInfo, .beautyHooks
      - semantic ref counts
    Minimizes: presentation/camera data, registry detail

Invocation surfaces
-------------------
  GET /v2/export/prompt-packets              (app backend)
  render_timeline.py --prompt-export PATH   (repo-local CLI flag)
  prosada/scripts/prosada_export_prompts.py  (project-local tooling script)
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

PACKET_VERSION = "1.0.0"

_VALID_PROFILES = ("storyboard-basic", "image-concept", "narrative-summary")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _scope_path(unit_id: str, units: Dict) -> List[str]:
    """Build ancestor chain from root to this unit (not including unit itself)."""
    path: List[str] = []
    visited: Set[str] = set()
    current_id = units.get(unit_id, None)
    parent_id = current_id.parent_id if current_id else None
    while parent_id and parent_id not in visited:
        visited.add(parent_id)
        path.insert(0, parent_id)
        parent = units.get(parent_id)
        parent_id = parent.parent_id if parent else None
    return path


def _sibling_index(unit_id: str, parent_id: Optional[str], units: Dict) -> int:
    """Return 0-based sibling index of unit_id in its parent's children list."""
    if not parent_id:
        return 0
    parent = units.get(parent_id)
    if not parent or not parent.children:
        return 0
    try:
        return parent.children.index(unit_id)
    except ValueError:
        return 0


def _presentation_dict(unit: Any) -> Optional[Dict]:
    """Return serialized presentation metadata or None if absent."""
    if unit is None or unit.presentation is None:
        return None
    return unit.presentation.model_dump(by_alias=True)


def _narrative_dict(unit: Any) -> Dict:
    """Build narrative summary dict from a NarrativeUnit."""
    if unit is None or unit.narrative is None:
        return {
            "status": "draft",
            "dripHook": None,
            "payoffDelivered": None,
            "newInfo": None,
            "beautyHooks": None,
            "characters": [],
            "locations": [],
            "threadsAdvanced": [],
        }
    nar = unit.narrative
    status = nar.status
    if hasattr(status, "value"):
        status = status.value
    return {
        "status": str(status),
        "dripHook": nar.drip_hook,
        "payoffDelivered": nar.payoff_delivered,
        "newInfo": nar.new_info,
        "beautyHooks": nar.beauty_hooks,
        "characters": list(nar.characters or []),
        "locations": list(nar.locations or []),
        "threadsAdvanced": list(nar.threads_advanced or []),
    }


def _registry_slices(
    unit: Any,
    registries_raw: Dict,
    semantic_entity_ids: List[str],
) -> Dict[str, List[Dict]]:
    """
    Build minimal registry slices relevant to this unit.
    Includes: characters/locations from unit.narrative, plus any semantic entity IDs.
    """
    char_ids: Set[str] = set()
    loc_ids: Set[str] = set()
    if unit and unit.narrative:
        char_ids.update(unit.narrative.characters or [])
        loc_ids.update(unit.narrative.locations or [])

    # Also include focus subjects from presentation
    if unit and unit.presentation:
        char_ids.update(unit.presentation.focus_subject_ids or [])

    slices: Dict[str, List[Dict]] = {}
    chars = registries_raw.get("characters", {}).get("entries", [])
    locs = registries_raw.get("locations", {}).get("entries", [])

    if char_ids:
        slices["characters"] = [e for e in chars if e.get("id") in char_ids]
    if loc_ids:
        slices["locations"] = [e for e in locs if e.get("id") in loc_ids]

    return slices


def _apply_profile(packet: Dict, profile: str) -> Dict:
    """
    Trim packet fields based on the requested profile.

    storyboard-basic: return as-is (full packet)
    image-concept: drop detailed narrative hooks; emphasize presentation + semantic
    narrative-summary: drop presentation camera fields; emphasize narrative hooks
    """
    if profile == "storyboard-basic":
        return packet

    if profile == "image-concept":
        # Keep: unitId, type, title, summary, presentation, semantic.entityIds, registrySlices
        # Strip: narrative hooks detail (keep status/characters/threads), timeline detail
        nar = packet.get("narrative", {})
        packet["narrative"] = {
            "status": nar.get("status"),
            "characters": nar.get("characters", []),
            "locations": nar.get("locations", []),
            "threadsAdvanced": nar.get("threadsAdvanced", []),
        }
        # Emphasize presentation — keep full block if present
        # Simplify semantic to just entity IDs
        sem = packet.get("semantic", {})
        packet["semantic"] = {
            "entityIds": sem.get("entityIds", []),
            "byKind": sem.get("byKind", {}),
            "refCount": sem.get("refCount", 0),
        }
        # Simplify context
        ctx = packet.get("context", {})
        packet["context"] = {"parentId": ctx.get("parentId"), "parentTitle": ctx.get("parentTitle")}
        return packet

    if profile == "narrative-summary":
        # Keep: narrative hooks in full, semantic counts
        # Strip: presentation camera/framing detail (keep mood only); timeline minimal
        pres = packet.get("presentation") or {}
        if pres:
            packet["presentation"] = {
                "moodTags": pres.get("moodTags", []),
                "imagePromptHints": pres.get("imagePromptHints"),
            }
        # Simplify timeline
        tl = packet.get("timeline", {})
        packet["timeline"] = {"start": tl.get("start"), "span": tl.get("span")}
        # Simplify registry to name only
        slices = packet.get("registrySlices", {})
        packet["registrySlices"] = {
            k: [{"id": e["id"], "name": e.get("name", e["id"])} for e in v]
            for k, v in slices.items()
        }
        return packet

    return packet


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def export_prompt_packets(
    project_dir: Path,
    *,
    profile: str = "storyboard-basic",
    scope: Optional[str] = None,
    streams: Optional[List[str]] = None,
    status: Optional[str] = None,
) -> Dict:
    """
    Export structured prompt packets for a ProsAda project.

    Each packet is a self-contained JSON document joining unit narrative,
    timeline placement, semantic refs, presentation metadata, and registry
    slices — everything needed for image/video/storyboard prompt generation.

    Parameters
    ----------
    project_dir : Path to prosada project directory (contains manifest.json)
    profile     : Export profile: storyboard-basic | image-concept | narrative-summary
    scope       : Optional unitId to scope to a subtree
    streams     : Optional stream IDs to filter to
    status      : Optional narrative.status filter (draft|review|locked)

    Returns
    -------
    dict : JSON-serializable prompt packet export

    Raises
    ------
    FileNotFoundError : manifest.json not found
    ValueError        : no units found, or invalid profile
    """
    if profile not in _VALID_PROFILES:
        raise ValueError(f"Invalid profile '{profile}'. Valid: {_VALID_PROFILES}")

    # Ensure backend is importable
    _backend = Path(__file__).parent.parent
    if str(_backend) not in sys.path:
        sys.path.insert(0, str(_backend))

    from persistence.unit_repository import UnitRepository
    from domain.v2_registry import RegistryType
    from services.canvas_layout_composer import CanvasLayoutComposer
    from services.projection_builder import (
        _collect_subtree_ids,
        _filter_canvas_by_scope,
        _filter_canvas_by_streams,
        _filter_canvas_by_status,
        _build_semantic_by_unit,
        _unit_id_from_event_id,
        build_projection,
    )

    if not (project_dir / "manifest.json").exists():
        raise FileNotFoundError(f"No manifest.json in {project_dir}")

    repo = UnitRepository(project_dir)
    manifest = repo.load_manifest()
    units = repo.load_all_units()

    if not units:
        raise ValueError(f"No units found in {project_dir / 'units'}")

    # Load registries
    registries_raw: Dict[str, Any] = {}
    for rt in RegistryType:
        rf = repo.load_registry(rt)
        if rf is not None:
            registries_raw[rt.value] = rf.model_dump(by_alias=True)

    # Build projection to get layout + semantic data (reuse projection infrastructure)
    projection = build_projection(
        project_dir,
        scope=scope,
        streams=streams,
        status=status,
    )

    # Build event index from projection
    event_by_unit: Dict[str, Dict] = {}
    for ev in projection.get("events", []):
        uid = ev.get("unitId", "")
        if uid not in event_by_unit:
            event_by_unit[uid] = ev

    # Get project ID from manifest
    project_id = getattr(manifest, "project_id", None) or getattr(manifest, "name", "unknown")
    if hasattr(project_id, "__str__"):
        project_id = str(project_id)

    # Build packets — one per projected event (one per unique unit in projection)
    seen_unit_ids: Set[str] = set()
    packets: List[Dict] = []

    for ev in projection.get("events", []):
        uid = ev.get("unitId", "")
        if uid in seen_unit_ids:
            continue
        seen_unit_ids.add(uid)

        unit = units.get(uid)

        # Get semantic summary from projection event
        sem = ev.get("semantic", {
            "refCount": 0, "byKind": {}, "entityIds": [], "unresolvedCount": 0
        })

        # Get parent info
        parent_id = unit.parent_id if unit else None
        parent_unit = units.get(parent_id) if parent_id else None
        parent_title = parent_unit.title if parent_unit else None

        # Timeline info from projection event
        timeline = {
            "start": ev.get("start", 0.0),
            "span": ev.get("span", 1.0),
            "laneId": ev.get("laneId", 0),
            "threadIds": ev.get("threadIds", []),
        }

        # Presentation metadata
        pres = _presentation_dict(unit)

        # Registry slices
        reg_slices = _registry_slices(unit, registries_raw, sem.get("entityIds", []))

        # Context
        scope_path = _scope_path(uid, units)
        sibling_idx = _sibling_index(uid, parent_id, units)

        packet: Dict = {
            "packetId": f"pkt-{uid}",
            "unitId": uid,
            "type": ev.get("type", ""),
            "title": ev.get("title", ""),
            "summary": ev.get("summary", ""),
            "timeline": timeline,
            "narrative": _narrative_dict(unit),
            "presentation": pres,
            "semantic": sem,
            "registrySlices": reg_slices,
            "context": {
                "parentId": parent_id,
                "parentTitle": parent_title,
                "siblingIndex": sibling_idx,
                "scopePath": scope_path,
            },
        }

        # Apply profile trimming
        packet = _apply_profile(packet, profile)
        packets.append(packet)

    return {
        "packetVersion": PACKET_VERSION,
        "profile": profile,
        "generatedAt": _now_iso(),
        "filters": {
            "scope": scope,
            "streams": streams,
            "status": status,
        },
        "summary": {
            "packetCount": len(packets),
            "projectId": project_id,
        },
        "packets": packets,
    }
