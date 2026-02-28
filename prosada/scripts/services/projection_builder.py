"""
Projection Builder — ProsAda Burst 12

Builds a normalized projection scene graph / analysis payload for a ProsAda project.

This is the canonical "overlay-ready" representation that joins:
  - Resolved layout intervals (from CanvasLayoutComposer)
  - Unit metadata (type, title, narrative.status, links)
  - Semantic reference summaries (from semantic_ref_parser)
  - Execution summaries (per-unit; stub returns empty when no execution data)
  - Registry slices (relevant entities only)

Consumed by:
  - GET /v2/projection/timeline  (backend endpoint)
  - render_timeline.py --projection-json  (CLI)
  - Renderer overlay infrastructure (semantic + status overlays)
  - Custom agent scripts in project repos

--------------------------------------------------------------------
Projection Payload Schema  (projectionVersion "1.0.0")
--------------------------------------------------------------------
{
  "meta": {
    "projectionVersion": "1.0.0",
    "projectDir": "...",
    "generatedAt": "...",
    "filters": {
      "scope": null,
      "streams": null,
      "status": null,
      "semanticKind": null,
      "semanticEntityId": null
    }
  },
  "bounds": {
    "minStart": 0.0,
    "maxEnd": 8.0,
    "laneCount": 3,
    "eventCount": 12
  },
  "lanes": [
    { "laneId": 0, "label": "ProsAda", "type": "spine",  "color": "#4a4a6a" },
    { "laneId": 1, "label": "Yggdrasil Arc", "type": "stream", "color": "#e91e63" }
  ],
  "threads": [
    {
      "threadId": "stream-yggdrasil-arc",
      "label":    "Yggdrasil Arc",
      "type":     "plot",
      "color":    "#e91e63",
      "start":    1.0,
      "span":     6.0,
      "laneId":   1,
      "mergeTargetId":  null,
      "birthOriginId":  null
    }
  ],
  "events": [
    {
      "eventId":     "ev-chapter-01",     // canvas event id
      "unitId":      "chapter-01",        // source NarrativeUnit id
      "type":        "chapter",
      "title":       "The Anomaly",
      "status":      "draft",             // narrative.status value
      "start":       1.0,                 // resolved spine position
      "span":        2.0,                 // resolved span (duration)
      "laneId":      0,
      "isResolved":  false,               // narrative.status == locked
      "threadIds":   ["stream-yggdrasil-arc"],
      "characterIds": ["ada-lovelace"],
      "summary":     "Ada detects the first echo.",
      "links":       [{"type": "setsUp", "targetId": "scene-payoff"}],
      "layoutMode":  "auto",              // "auto" | "absolute" | "relative"
      "semantic": {
        "refCount":      3,
        "byKind":        { "char": 2, "concept": 1 },
        "entityIds":     ["ada-lovelace", "arboros"],
        "unresolvedCount": 0
      },
      "execution": {
        "runCount":        0,
        "artifactCount":   0,
        "hasExecution":    false,
        "latestRunStatus": null
      },
      "presentation": null               // Forward-compat slot.
                                         // Future bursts may populate with:
                                         // { "shotType": "establishing",
                                         //   "pan": "right", "tone": "tense" }
    }
  ],
  "units": {
    "chapter-01": {
      "unitId": "chapter-01",
      "type": "chapter",
      "title": "The Anomaly",
      "status": "draft",
      "parentId": "act-01"
    }
  },
  "semantic": {
    "totalRefs":      15,
    "byKind":         { "char": 8, "concept": 5, "symbol": 2 },
    "unresolvedCount": 0,
    "byEntity": {
      "char:ada-lovelace": {
        "entityId": "ada-lovelace",
        "kind":     "char",
        "unitIds":  ["chapter-01", "scene-prologue"],
        "refCount": 5
      }
    }
  },
  "registries": {
    "characters": [{ "id": "ada-lovelace", "name": "Ada Lovelace" }]
  }
}

Extension slot — presentation / direction metadata
---------------------------------------------------
Each event carries "presentation": null.  This is a forward-compatibility
reservation for future burst(s) implementing cinematic/directorial metadata
(establishing shot, pan direction, tone, etc.).  Populating this field does
NOT require a schema version bump — consumers MUST ignore unknown keys.
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

PROJECTION_VERSION = "1.0.0"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _unit_id_from_event_id(ev_id: str) -> Optional[str]:
    """Extract source unitId from a canvas event id ('ev-{uid}' or 'ev-{uid}--{sid}')."""
    if not ev_id.startswith("ev-"):
        return None
    return ev_id[3:].split("--")[0]


def _layout_mode(unit: Any) -> str:
    """
    Return 'absolute', 'relative', or 'auto' from unit view.canvas.layout hint.
    """
    try:
        layout = unit.view.canvas.layout
        if layout is None or layout.mode != "manual":
            return "auto"
        return layout.coordinate_mode  # "absolute" or "relative"
    except AttributeError:
        return "auto"


# ---------------------------------------------------------------------------
# Canvas filter helpers (duplicated from render_timeline.py to avoid
# importing the app renderer module from a service)
# ---------------------------------------------------------------------------

def _collect_subtree_ids(scope_id: str, units: Dict) -> Set[str]:
    """Return the set of unitIds reachable from scope_id (inclusive)."""
    result: Set[str] = set()

    def _walk(uid: str) -> None:
        if uid in result:
            return
        result.add(uid)
        unit = units.get(uid)
        if unit:
            for child_id in (unit.children or []):
                _walk(child_id)

    _walk(scope_id)
    return result


def _filter_canvas_by_scope(canvas: Dict, scope_ids: Set[str]) -> Dict:
    def _uid(ev_id: str) -> Optional[str]:
        if not ev_id.startswith("ev-"):
            return None
        return ev_id[3:].split("--")[0]

    return {
        "timelines": canvas["timelines"],
        "threads": canvas["threads"],
        "events": {eid: e for eid, e in canvas["events"].items()
                   if _uid(eid) in scope_ids},
        "checkpoints": {cid: c for cid, c in canvas["checkpoints"].items()
                        if cid[3:] in scope_ids},
    }


def _filter_canvas_by_streams(canvas: Dict, stream_ids: Set[str]) -> Dict:
    return {
        "timelines": canvas["timelines"],
        "threads": {tid: t for tid, t in canvas["threads"].items() if tid in stream_ids},
        "events": {eid: e for eid, e in canvas["events"].items()
                   if e.get("laneId", 0) == 0 or e.get("attachedToId") in stream_ids},
        "checkpoints": canvas["checkpoints"],
    }


def _filter_canvas_by_status(canvas: Dict, status: str) -> Dict:
    if status == "locked":
        filtered = {eid: e for eid, e in canvas["events"].items() if e.get("isResolved")}
    else:
        filtered = {eid: e for eid, e in canvas["events"].items() if not e.get("isResolved")}
    return {**canvas, "events": filtered}


# ---------------------------------------------------------------------------
# Semantic helpers
# ---------------------------------------------------------------------------

def _build_semantic_by_unit(refs: List[Any]) -> Dict[str, Dict]:
    """
    Build per-unit semantic summary from a list of SemanticRef objects.
    Returns { unit_id → { refCount, byKind, entityIds, unresolvedCount } }
    """
    index: Dict[str, Dict] = {}
    for ref in refs:
        uid = ref.unit_id
        if uid not in index:
            index[uid] = {"refCount": 0, "byKind": {}, "entityIds": [], "unresolvedCount": 0}
        index[uid]["refCount"] += 1
        index[uid]["byKind"][ref.kind] = index[uid]["byKind"].get(ref.kind, 0) + 1
        if ref.entity_id and ref.entity_id not in index[uid]["entityIds"]:
            index[uid]["entityIds"].append(ref.entity_id)
        if not ref.resolved:
            index[uid]["unresolvedCount"] += 1
    return index


def _build_global_semantic(refs: List[Any]) -> Dict:
    """Build global semantic summary across all refs."""
    by_kind: Dict[str, int] = {}
    unresolved = 0
    by_entity: Dict[str, Dict] = {}

    for ref in refs:
        by_kind[ref.kind] = by_kind.get(ref.kind, 0) + 1
        if not ref.resolved:
            unresolved += 1
        if ref.kind and ref.entity_id:
            key = f"{ref.kind}:{ref.entity_id}"
            if key not in by_entity:
                by_entity[key] = {
                    "entityId": ref.entity_id,
                    "kind": ref.kind,
                    "unitIds": [],
                    "refCount": 0,
                }
            by_entity[key]["refCount"] += 1
            if ref.unit_id and ref.unit_id not in by_entity[key]["unitIds"]:
                by_entity[key]["unitIds"].append(ref.unit_id)

    return {
        "totalRefs": len(refs),
        "byKind": by_kind,
        "unresolvedCount": unresolved,
        "byEntity": by_entity,
    }


def _empty_execution() -> Dict:
    """Default execution summary stub (no execution backend in v1)."""
    return {
        "runCount": 0,
        "artifactCount": 0,
        "hasExecution": False,
        "latestRunStatus": None,
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_projection(
    project_dir: Path,
    *,
    scope: Optional[str] = None,
    streams: Optional[List[str]] = None,
    status: Optional[str] = None,
    semantic_kind: Optional[str] = None,
    semantic_entity_id: Optional[str] = None,
) -> Dict:
    """
    Build a normalized projection payload for a ProsAda project.

    Parameters
    ----------
    project_dir        : Path to prosada project directory (contains manifest.json)
    scope              : Optional unitId to scope layout/events to a subtree
    streams            : Optional list of stream IDs to include
    status             : Optional status filter ("draft" | "review" | "locked")
    semantic_kind      : Optional semantic ref kind filter for semantic section
    semantic_entity_id : Optional entity ID filter for semantic section

    Returns
    -------
    dict : JSON-serializable projection payload

    Raises
    ------
    FileNotFoundError : manifest.json not found in project_dir
    ValueError        : no units found in project
    """
    # Ensure backend dir is importable
    _backend = Path(__file__).parent.parent
    if str(_backend) not in sys.path:
        sys.path.insert(0, str(_backend))

    from persistence.unit_repository import UnitRepository
    from domain.v2_registry import RegistryType
    from services.canvas_layout_composer import CanvasLayoutComposer

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

    # Compose canvas
    canvas = CanvasLayoutComposer.compose(units, manifest, registries_raw)

    # Apply filters
    if scope:
        canvas = _filter_canvas_by_scope(canvas, _collect_subtree_ids(scope, units))
    if streams is not None:
        canvas = _filter_canvas_by_streams(canvas, set(streams))
    if status:
        canvas = _filter_canvas_by_status(canvas, status)

    # Scope ids for semantic filtering
    scope_ids: Optional[Set[str]] = None
    if scope:
        scope_ids = _collect_subtree_ids(scope, units)

    # Parse semantic refs
    from services.semantic_ref_parser import parse_project
    units_dir = project_dir / "units"
    try:
        parse_result = parse_project(
            units=units,
            registries_raw=registries_raw,
            units_dir=units_dir,
            scope_ids=scope_ids,
            filter_kind=semantic_kind,
            filter_entity_id=semantic_entity_id,
        )
        all_refs = parse_result.refs
    except Exception:
        all_refs = []

    # Semantic indexes
    semantic_by_unit = _build_semantic_by_unit(all_refs)
    global_semantic = _build_global_semantic(all_refs)

    # --- Lanes ---
    lane_objects: Dict[int, Dict] = {}
    for tl in canvas.get("timelines", {}).values():
        lid = tl.get("laneId", 0)
        lane_objects[lid] = {"_type": "spine", **tl}
    for th in canvas.get("threads", {}).values():
        lid = th.get("laneId", 1)
        lane_objects[lid] = {"_type": "stream", **th}

    lanes: List[Dict] = []
    for lid in sorted(lane_objects.keys()):
        obj = lane_objects[lid]
        lanes.append({
            "laneId": lid,
            "label": obj.get("name", f"Lane {lid}"),
            "type":  obj.get("_type", "spine"),
            "color": obj.get("color", "#888888"),
        })

    # --- Threads ---
    threads_list: List[Dict] = [
        {
            "threadId":      tid,
            "label":         th.get("name", tid),
            "type":          th.get("type", "plot"),
            "color":         th.get("color", "#888888"),
            "start":         th.get("position", 0.0),
            "span":          th.get("duration", 1.0),
            "laneId":        th.get("laneId", 1),
            "mergeTargetId": th.get("mergeTargetId"),
            "birthOriginId": th.get("birthOriginId"),
        }
        for tid, th in canvas.get("threads", {}).items()
    ]

    # --- Events ---
    events_list: List[Dict] = []
    for ev_id, ev in canvas.get("events", {}).items():
        uid = _unit_id_from_event_id(ev_id) or ev_id
        unit = units.get(uid)

        # Narrative status
        nar_status = "draft"
        if unit and unit.narrative and unit.narrative.status:
            st = unit.narrative.status
            nar_status = st.value if hasattr(st, "value") else str(st)

        # Layout mode
        layout_mode = _layout_mode(unit) if unit else "auto"

        # Links
        unit_links: List[Dict] = []
        if unit and unit.links:
            unit_links = [
                {"type": lnk.type.value, "targetId": lnk.target_id}
                for lnk in unit.links
            ]

        # Semantic summary
        sem = semantic_by_unit.get(uid, {
            "refCount": 0, "byKind": {}, "entityIds": [], "unresolvedCount": 0
        })

        # Presentation metadata — populated from unit.presentation if authored
        presentation_data = None
        if unit is not None and unit.presentation is not None:
            try:
                presentation_data = unit.presentation.model_dump(by_alias=True)
            except Exception:
                presentation_data = None

        events_list.append({
            "eventId":     ev_id,
            "unitId":      uid,
            "type":        (unit.type.value if unit else ev.get("type", "")),
            "title":       ev.get("title", ""),
            "status":      nar_status,
            "start":       ev.get("position", 0.0),
            "span":        ev.get("duration", 1.0),
            "laneId":      ev.get("laneId", 0),
            "isResolved":  ev.get("isResolved", False),
            "threadIds":   ev.get("relatedThreadIds", []),
            "characterIds": ev.get("characterIds", []),
            "summary":     ev.get("summary", ""),
            "links":       unit_links,
            "layoutMode":  layout_mode,
            "semantic":    sem,
            "execution":   _empty_execution(),
            # Populated from unit.presentation when authored; null otherwise.
            "presentation": presentation_data,
        })

    # --- Bounds ---
    starts = [e["start"] for e in events_list] or [0.0]
    ends   = [e["start"] + e["span"] for e in events_list] or [1.0]
    thread_ends = [t["start"] + t["span"] for t in threads_list]
    max_end = max(ends + thread_ends) if (ends + thread_ends) else 1.0

    # --- Minimal registry slices (referenced entities only) ---
    referenced_ids: Set[str] = {ref.entity_id for ref in all_refs if ref.entity_id}
    minimal_registries: Dict[str, list] = {}
    for reg_type, reg_data in registries_raw.items():
        entries = reg_data.get("entries", [])
        relevant = [e for e in entries if e.get("id") in referenced_ids]
        if relevant:
            minimal_registries[reg_type] = relevant

    # --- Normalized units map ---
    units_map: Dict[str, Dict] = {}
    for uid, unit in units.items():
        nar_st = "draft"
        if unit.narrative and unit.narrative.status:
            st = unit.narrative.status
            nar_st = st.value if hasattr(st, "value") else str(st)
        # Include presentation summary in units map for downstream use
        pres_summary = None
        if unit.presentation is not None:
            try:
                pres_summary = unit.presentation.model_dump(by_alias=True)
            except Exception:
                pres_summary = None
        units_map[uid] = {
            "unitId":       uid,
            "type":         unit.type.value,
            "title":        unit.title,
            "status":       nar_st,
            "parentId":     unit.parent_id,
            "presentation": pres_summary,
        }

    return {
        "meta": {
            "projectionVersion": PROJECTION_VERSION,
            "projectDir": str(project_dir),
            "generatedAt": _now_iso(),
            "filters": {
                "scope":           scope,
                "streams":         streams,
                "status":          status,
                "semanticKind":    semantic_kind,
                "semanticEntityId": semantic_entity_id,
            },
        },
        "bounds": {
            "minStart":   min(starts),
            "maxEnd":     max_end,
            "laneCount":  len(lanes),
            "eventCount": len(events_list),
        },
        "lanes":      lanes,
        "threads":    threads_list,
        "events":     events_list,
        "units":      units_map,
        "semantic":   global_semantic,
        "registries": minimal_registries,
    }
