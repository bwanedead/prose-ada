"""
Layout Migration Helpers

Generate strict-compatible pins from current resolved layout intervals.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Tuple

from domain.narrative_unit import NarrativeUnit, StreamLayout, UnitType
from services.canvas_layout_composer import CanvasLayoutComposer
from services.layout_policy import LAYOUT_POLICY_LEGACY_AUTO


_CONTENT_TYPES = {
    UnitType.SERIES,
    UnitType.BOOK,
    UnitType.ACT,
    UnitType.SEQUENCE,
    UnitType.CHAPTER,
    UnitType.SCENE,
    UnitType.BEAT,
    UnitType.ARC,
}


def _is_valid_manual(layout: StreamLayout | None, coordinate_mode: str) -> bool:
    if layout is None:
        return False
    return (
        layout.mode == "manual"
        and layout.coordinate_mode == coordinate_mode
        and layout.start is not None
        and layout.span is not None
        and layout.span > 0
    )


def _set_manual(unit: NarrativeUnit, coordinate_mode: str, start: float, span: float) -> None:
    unit.view.canvas.layout = StreamLayout(
        mode="manual",
        coordinate_mode=coordinate_mode,
        start=float(start),
        span=float(span),
    )


def build_pin_migration(
    units: Dict[str, NarrativeUnit],
    manifest: Dict[str, Any],
    registries_raw: Dict[str, Any],
    *,
    force: bool = False,
) -> Tuple[Dict[str, NarrativeUnit], Dict[str, Any]]:
    """
    Build strict-pin layout values from current resolved layout.

    Returns (units_copy, report).
    """
    units_out: Dict[str, NarrativeUnit] = {uid: u.model_copy(deep=True) for uid, u in units.items()}
    report: Dict[str, Any] = {
        "modifiedUnits": [],
        "skippedUnits": [],
        "errors": [],
    }

    # Always compose using legacy policy so existing projects can be migrated.
    compose_manifest = deepcopy(manifest)
    compose_manifest["layoutPolicy"] = LAYOUT_POLICY_LEGACY_AUTO
    canvas = CanvasLayoutComposer.compose(units, compose_manifest, registries_raw)

    # Content intervals from primary (non-stream-copy) events
    content_intervals: Dict[str, Tuple[float, float]] = {}
    for event_id, ev in canvas.get("events", {}).items():
        if "--" in event_id:
            continue
        if not event_id.startswith("ev-"):
            continue
        uid = event_id[3:]
        content_intervals[uid] = (float(ev.get("position", 0.0)), float(ev.get("duration", 1.0)))

    root_id = manifest.get("root")
    root_timeline = canvas.get("timelines", {}).get(root_id) if root_id else None
    if root_id and root_timeline:
        content_intervals[root_id] = (
            float(root_timeline.get("position", 0.0)),
            float(root_timeline.get("duration", 1.0)),
        )

    # Stream intervals from thread objects
    stream_intervals: Dict[str, Tuple[float, float]] = {
        sid: (float(th.get("position", 0.0)), float(th.get("duration", 1.0)))
        for sid, th in canvas.get("threads", {}).items()
    }

    for uid, unit in units_out.items():
        # Streams: required absolute pins in strict mode.
        if unit.type == UnitType.STREAM:
            interval = stream_intervals.get(uid)
            if interval is None:
                report["errors"].append(
                    f"Stream '{uid}' has no resolved thread interval."
                )
                continue
            if (not force) and _is_valid_manual(unit.view.canvas.layout, "absolute"):
                report["skippedUnits"].append(uid)
                continue
            _set_manual(unit, "absolute", interval[0], interval[1])
            report["modifiedUnits"].append(uid)
            continue

        if unit.type not in _CONTENT_TYPES:
            continue

        interval = content_intervals.get(uid)
        if interval is None:
            report["errors"].append(f"Content unit '{uid}' has no resolved interval.")
            continue

        is_root = uid == root_id
        if is_root:
            if (not force) and _is_valid_manual(unit.view.canvas.layout, "absolute"):
                report["skippedUnits"].append(uid)
                continue
            _set_manual(unit, "absolute", interval[0], interval[1])
            report["modifiedUnits"].append(uid)
            continue

        parent_id = unit.parent_id
        if not parent_id:
            report["errors"].append(f"Non-root content unit '{uid}' has no parentId.")
            continue
        parent_interval = content_intervals.get(parent_id)
        if parent_interval is None:
            report["errors"].append(
                f"Unit '{uid}' parent '{parent_id}' has no resolved interval."
            )
            continue
        p_start, p_span = parent_interval
        if p_span <= 0:
            report["errors"].append(
                f"Unit '{uid}' parent '{parent_id}' has non-positive span."
            )
            continue

        rel_start = (interval[0] - p_start) / p_span
        rel_span = interval[1] / p_span

        if (not force) and _is_valid_manual(unit.view.canvas.layout, "relative"):
            report["skippedUnits"].append(uid)
            continue
        _set_manual(unit, "relative", rel_start, rel_span)
        report["modifiedUnits"].append(uid)

    report["modifiedCount"] = len(report["modifiedUnits"])
    report["skippedCount"] = len(report["skippedUnits"])
    report["errorCount"] = len(report["errors"])
    return units_out, report

