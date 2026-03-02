"""
Canvas Layout Composer — Phase 1 + Burst 08/08.1

Derives legacy canvas layout data from v2 NarrativeUnits.
This is a pure adapter: v2 units in → legacy canvas shape out.
No canvas component source files are touched.

Output shape matches the legacy canvas store:
    { timelines, threads, events, checkpoints }

Coordinate system:
    The legacy canvas components each define RENDER_SCALE = 100.
    They render `left: position * 100` and `width: duration * 100` (px).
    Therefore positions and durations in the STORE are abstract units, not pixels.
    This composer outputs abstract units; the canvas scales them internally.

Lane model:
    Lane 0 = spine (book/series root + all backbone content units)
    Lane 1..N = stream lanes (each stream unit gets its own lane, stable sort)

Duration model (auto/derived):
    duration(unit) = count of unit itself + all its descendants.
    This ensures parent units span exactly the width of all their children.
    Example: book with 1 act → book.duration=2, act.duration=1
    The act event sits at position 1, inside book's span [0, 2).

Layout hint resolution (Burst 08 / 08.1):
    Content units (act/chapter/scene/beat/arc/sequence) can carry
    view.canvas.layout hints that override the derived position+span.

    Reconciliation rules (applied top-down from root):
      1. mode="manual", coordinateMode="absolute", start/span valid:
            use start/span directly as absolute spine units.
      2. mode="manual", coordinateMode="relative", start/span valid, parent resolved:
            absStart = parentStart + start * parentSpan
            absSpan  = span * parentSpan
            (start is unclamped; span must be > 0 to be valid)
      3. Any other case (auto mode, missing/invalid fields, unresolvable parent):
            fall back to derived position/duration.

    Stream/thread units: absolute layout only (Burst 08 behaviour unchanged).
    Relative pins for streams are reserved for a future burst.

Multi-lane appearance:
    Content units are assigned to at most one rendered lane:
      - If narrative.threadsAdvanced[] has at least one valid stream unitId,
        owner = first valid stream id, and the event renders on that stream lane.
      - Otherwise, event renders on spine lane 0.
    Additional stream memberships are preserved in relatedThreadIds metadata.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Tuple

from domain.narrative_unit import NarrativeUnit, UnitType, UnitStatus
from services.graph_composer import GraphComposer
from services.layout_policy import is_strict_pins_policy

# NOTE: RENDER_SCALE = 100 lives in the canvas components (TimelineLane, ThreadNode).
# Do NOT multiply by 100 here — the canvas does that internally.
SPINE_LANE = 0
DEFAULT_THREAD_COLOR = "#888888"

# Content unit types that map to canvas Events
_CONTENT_TYPES = frozenset({
    UnitType.ACT,
    UnitType.CHAPTER,
    UnitType.SEQUENCE,
    UnitType.CONNECTIVE,
    UnitType.SCENE,
    UnitType.BEAT,
    UnitType.ARC,
})

# Units that should never participate in canvas interval composition.
_NON_CANVAS_TYPES = frozenset({
    UnitType.THEORY,
    UnitType.ETHOS,
})


def _event_type(unit_type: UnitType) -> str:
    if unit_type == UnitType.SCENE:
        return "scene"
    if unit_type == UnitType.BEAT:
        return "beat"
    if unit_type == UnitType.CONNECTIVE:
        return "beat"
    return "chapter_break"


# ---------------------------------------------------------------------------
# Layout hint resolution — top-down DFS
# ---------------------------------------------------------------------------

def _resolve_content_intervals(
    root_id: Optional[str],
    content_units: Dict[str, NarrativeUnit],
    position_map: Dict[str, int],
    count_all: Callable[[str], int],
    strict_pins: bool = False,
) -> Dict[str, Tuple[float, float]]:
    """
    Resolve the canvas (start, span) for every content unit in top-down order.

    For each unit, the reconciliation priority is:
      1. mode="manual" + coordinateMode="absolute"  → use layout.start/span directly
      2. mode="manual" + coordinateMode="relative"  → convert using parent interval
      3. fallback                                   → view.canvas.x (if set) else derived

    Returns Dict[unitId, (start, span)] in spine logical units.
    Processing parents before children ensures relative pins can always access
    their parent's resolved interval.
    """
    resolved: Dict[str, Tuple[float, float]] = {}
    visited: set = set()

    def _derived(uid: str) -> Tuple[float, float]:
        unit = content_units.get(uid)
        if not unit:
            return (0.0, 1.0)
        pos = unit.view.canvas.x if unit.view.canvas.x is not None else float(position_map.get(uid, 0))
        span = max(count_all(uid), 1)
        return (pos, float(span))

    def resolve(uid: str) -> None:
        if uid in visited:
            return
        visited.add(uid)

        unit = content_units.get(uid)
        if not unit:
            return

        layout = unit.view.canvas.layout
        is_root = root_id is not None and uid == root_id

        # Check for a valid manual layout hint
        has_valid_hint = (
            layout is not None
            and layout.mode == "manual"
            and layout.start is not None
            and layout.span is not None
            and layout.span > 0
        )

        if has_valid_hint:
            coord_mode = layout.coordinate_mode  # type: ignore[union-attr]

            if coord_mode == "absolute":
                resolved[uid] = (layout.start, layout.span)  # type: ignore[arg-type]

            elif coord_mode == "relative":
                # Ensure parent is resolved first
                parent_id = unit.parent_id
                if parent_id and parent_id in content_units and parent_id not in visited:
                    resolve(parent_id)

                parent_interval = resolved.get(parent_id) if parent_id else None

                if parent_interval and parent_interval[1] > 0:
                    p_start, p_span = parent_interval
                    abs_start = p_start + layout.start * p_span  # type: ignore[operator]
                    abs_span = layout.span * p_span               # type: ignore[operator]
                    resolved[uid] = (abs_start, max(abs_span, 0.01))
                else:
                    if strict_pins:
                        raise ValueError(
                            f"strict-pins: unit '{uid}' has relative pin but parent "
                            f"'{parent_id}' interval is unavailable."
                        )
                    # Parent unavailable or has zero span → fall back to derived
                    resolved[uid] = _derived(uid)

            else:
                if strict_pins:
                    raise ValueError(
                        f"strict-pins: unit '{uid}' has unsupported coordinateMode '{coord_mode}'."
                    )
                # Unknown coordinateMode → fall back to derived
                resolved[uid] = _derived(uid)

        else:
            if strict_pins:
                raise ValueError(
                    f"strict-pins: unit '{uid}' is missing a valid manual layout pin."
                )
            # No valid manual hint → derived layout
            resolved[uid] = _derived(uid)

        if strict_pins:
            # Enforce unit-class pin semantics in resolver as a fail-safe.
            mode = layout.coordinate_mode if layout is not None else None  # type: ignore[union-attr]
            if unit.type in {
                UnitType.SERIES, UnitType.BOOK, UnitType.ACT, UnitType.SEQUENCE,
                UnitType.CONNECTIVE, UnitType.CHAPTER, UnitType.SCENE, UnitType.BEAT, UnitType.ARC,
            }:
                if is_root and mode != "absolute":
                    raise ValueError(
                        f"strict-pins: root unit '{uid}' must use coordinateMode='absolute'."
                    )
                if not is_root and mode != "relative":
                    raise ValueError(
                        f"strict-pins: non-root content unit '{uid}' must use coordinateMode='relative'."
                    )

        # Recurse into content children (top-down, so parent is always resolved first)
        for child_id in unit.children:
            if child_id in content_units:
                resolve(child_id)

    # Start DFS from the declared root
    if root_id and root_id in content_units:
        resolve(root_id)

    # Catch any orphaned units not reachable from the root
    for uid in content_units:
        if uid not in visited:
            if strict_pins:
                raise ValueError(
                    f"strict-pins: content unit '{uid}' is not reachable from root '{root_id}'."
                )
            resolved.setdefault(uid, _derived(uid))

    return resolved


# ---------------------------------------------------------------------------
# Composer
# ---------------------------------------------------------------------------

class CanvasLayoutComposer:
    """
    Stateless adapter: v2 units → legacy canvas layout.
    All methods are static.
    """

    @staticmethod
    def compose(
        units: Dict[str, NarrativeUnit],
        manifest: dict,
        registries: Optional[Dict[str, Any]] = None,
    ) -> dict:
        """
        Produce a canvas layout dict from the v2 unit graph.

        Parameters
        ----------
        units       : all loaded NarrativeUnits keyed by unitId
        manifest    : project manifest dict (for root pointer)
        registries  : optional registry dicts (used for thread color/type lookup)
        """
        # -----------------------------------------------------------------------
        # 1. Separate streams from content; build position map on content only
        #    Stream units have parentId=null and must NOT influence flat positions.
        # -----------------------------------------------------------------------
        stream_units_list: List[NarrativeUnit] = sorted(
            [u for u in units.values() if u.type == UnitType.STREAM],
            key=lambda u: u.unit_id,  # stable, deterministic lane assignment
        )
        content_units: Dict[str, NarrativeUnit] = {
            uid: u for uid, u in units.items()
            if u.type != UnitType.STREAM and u.type not in _NON_CANVAS_TYPES
        }

        flat = GraphComposer.compose_flat_timeline(content_units)
        position_map: Dict[str, int] = {
            entry["unitId"]: entry["position"] for entry in flat
        }

        # -----------------------------------------------------------------------
        # 2. Subtree unit count → duration in abstract units
        #    duration(unit) = 1 (self) + sum(duration(child) for child in children)
        #    This ensures a parent's span exactly covers all its children.
        # -----------------------------------------------------------------------
        def count_all(unit_id: str) -> int:
            unit = content_units.get(unit_id)
            if not unit:
                return 0
            if not unit.children:
                return 1
            return 1 + sum(count_all(cid) for cid in unit.children if cid in content_units)

        # -----------------------------------------------------------------------
        # 3. Registry lookup: thread colors + types
        # -----------------------------------------------------------------------
        thread_colors: Dict[str, str] = {}
        thread_types: Dict[str, str] = {}
        if registries:
            threads_reg = registries.get("threads") or {}
            for entry in threads_reg.get("entries", []):
                eid = entry.get("id", "")
                thread_colors[eid] = entry.get("color", DEFAULT_THREAD_COLOR)
                raw_type = entry.get("type", "plot")
                valid_canvas_thread_types = {"character", "mystery", "plot", "theme", "other"}
                thread_types[eid] = raw_type if raw_type in valid_canvas_thread_types else "plot"

        # -----------------------------------------------------------------------
        # 4. Resolve layout hints for all content units (top-down DFS).
        #    Must happen before building timelines or events so that both the
        #    root timeline and all child events use a consistent resolved interval.
        # -----------------------------------------------------------------------
        root_id: Optional[str] = manifest.get("root")
        root_unit = content_units.get(root_id) if root_id else None
        strict_pins = is_strict_pins_policy(manifest)

        resolved_intervals = _resolve_content_intervals(
            root_id, content_units, position_map, count_all, strict_pins=strict_pins
        )

        # -----------------------------------------------------------------------
        # 5. Root book/series → Timeline on lane 0
        # -----------------------------------------------------------------------
        timelines: Dict[str, dict] = {}
        threads: Dict[str, dict] = {}
        events: Dict[str, dict] = {}
        checkpoints: Dict[str, dict] = {}

        if root_unit and root_unit.type in (UnitType.BOOK, UnitType.SERIES):
            r_pos, r_span = resolved_intervals.get(root_unit.unit_id, (0.0, 1.0))
            timelines[root_unit.unit_id] = {
                "id": root_unit.unit_id,
                "name": root_unit.title,
                "description": root_unit.summary or "",
                "type": "linear",
                "laneId": SPINE_LANE,
                "isVisible": True,
                "position": r_pos,
                "duration": r_span,
            }

        # -----------------------------------------------------------------------
        # 6. Stream units → Thread objects on lanes 1..N
        #    (Burst 08 behaviour: absolute manual hints only for streams)
        # -----------------------------------------------------------------------
        stream_lane_map: Dict[str, int] = {}

        for idx, stream in enumerate(stream_units_list):
            lane_id = idx + 1
            stream_lane_map[stream.unit_id] = lane_id

            # Merge / branch from links[]
            merge_target_id: Optional[str] = None
            birth_origin_id: Optional[str] = None
            for lnk in stream.links:
                if lnk.type.value == "merges-into":
                    merge_target_id = lnk.target_id
                elif lnk.type.value == "branches-from":
                    birth_origin_id = lnk.target_id

            # Position span: use manual layout hint if valid, else derive from members.
            layout = stream.view.canvas.layout
            if (
                layout is not None
                and layout.mode == "manual"
                and layout.start is not None
                and layout.span is not None
                and layout.span > 0
            ):
                if strict_pins and layout.coordinate_mode != "absolute":
                    raise ValueError(
                        f"strict-pins: stream '{stream.unit_id}' must use coordinateMode='absolute'."
                    )
                start_pos = layout.start
                duration = layout.span
            else:
                if strict_pins:
                    raise ValueError(
                        f"strict-pins: stream '{stream.unit_id}' is missing valid absolute manual layout."
                    )
                member_positions = [
                    (
                        u.view.canvas.x
                        if u.view.canvas.x is not None
                        else position_map.get(uid, 0)
                    )
                    for uid, u in content_units.items()
                    if stream.unit_id in u.narrative.threads_advanced
                ]
                start_pos = min(member_positions) if member_positions else 0
                end_pos = max(member_positions) + 1 if member_positions else 1
                duration = max(end_pos - start_pos, 1)

            color = thread_colors.get(stream.unit_id, DEFAULT_THREAD_COLOR)
            t_type = thread_types.get(stream.unit_id, "plot")

            threads[stream.unit_id] = {
                "id": stream.unit_id,
                "name": stream.title,
                "description": stream.summary or "",
                "type": t_type,
                "color": color,
                "visible": True,
                "timelineId": root_id or "",
                "position": start_pos,
                "duration": duration,
                "laneId": lane_id,
                "birthOriginId": birth_origin_id,
                "mergeTargetId": merge_target_id,
                "relatedCharacterIds": stream.narrative.characters,
            }

        # -----------------------------------------------------------------------
        # 7. Content units → Event objects (spine lane + stream lanes)
        #    Use resolved_intervals for position/duration (honours layout hints).
        # -----------------------------------------------------------------------
        for unit in content_units.values():
            if unit.type not in _CONTENT_TYPES:
                continue

            pos, duration = resolved_intervals.get(
                unit.unit_id,
                (float(position_map.get(unit.unit_id, 0)), max(count_all(unit.unit_id), 1.0))
            )
            is_resolved = unit.narrative.status == UnitStatus.LOCKED
            ev_type = _event_type(unit.type)

            # Stream IDs this unit belongs to (only ones that exist as stream units)
            related_stream_ids = [
                sid for sid in unit.narrative.threads_advanced
                if sid in stream_lane_map
            ]
            owner_stream_id: Optional[str] = related_stream_ids[0] if related_stream_ids else None

            # Primary event lane assignment:
            # stream-owned events render on their owner stream lane only.
            event_lane = stream_lane_map[owner_stream_id] if owner_stream_id is not None else SPINE_LANE
            attached_to = owner_stream_id if owner_stream_id is not None else (root_id or "")

            # Primary event (single rendered copy only)
            ev_id = f"ev-{unit.unit_id}"
            events[ev_id] = {
                "id": ev_id,
                "title": unit.title,
                "summary": unit.summary or "",
                "position": pos,
                "relativePosition": pos,
                "duration": duration,
                "timelineId": root_id or "",
                "attachedToId": attached_to,
                "laneId": event_lane,
                "relatedThreadIds": related_stream_ids,
                "characterIds": unit.narrative.characters,
                "type": ev_type,
                "isResolved": is_resolved,
            }

            # Checkpoint for locked units
            if is_resolved:
                cp_id = f"cp-{unit.unit_id}"
                checkpoints[cp_id] = {
                    "id": cp_id,
                    "name": unit.title,
                    "description": unit.summary or "",
                    "position": pos,
                    "relativePosition": pos,
                    "parentType": "timeline",
                    "parentId": root_id or "",
                    "type": "milestone",
                    "color": "#FFD700",
                }

        return {
            "timelines": timelines,
            "threads": threads,
            "events": events,
            "checkpoints": checkpoints,
        }
