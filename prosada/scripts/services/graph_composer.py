"""
Graph Composer — v2 Services Layer

Derives composed views from a flat collection of NarrativeUnits.

These are pure functions: { unitId: NarrativeUnit } in → derived view out.
No state, no side effects, no persistence.

The composed timeline/tree is NOT the canonical story. The unit files are.
This module exists only to produce views that the frontend can visualize.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from domain.narrative_unit import NarrativeUnit, UnitType


# ---------------------------------------------------------------------------
# Composed view types (plain dataclasses — not persisted)
# ---------------------------------------------------------------------------

@dataclass
class ComposedNode:
    """A node in the derived tree view."""
    unit: NarrativeUnit
    depth: int = 0
    children: List[ComposedNode] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Composer
# ---------------------------------------------------------------------------

class GraphComposer:
    """
    Composes a flat dict of NarrativeUnits into derived views.

    All methods are static — the composer holds no state.
    """

    @staticmethod
    def compose_tree(units: Dict[str, NarrativeUnit]) -> List[ComposedNode]:
        """
        Build an ordered tree from flat units using parentId + children[] ordering.

        Each parent unit's children[] list is the authoritative order for its children.
        Units referenced in children[] that don't exist in the units dict are silently
        skipped (graceful degradation for partially-loaded projects).

        Returns a list of root nodes (units whose parentId is None or points to a
        unitId not present in the dict).
        """
        known_ids = set(units.keys())

        def build_node(unit: NarrativeUnit, depth: int) -> ComposedNode:
            node = ComposedNode(unit=unit, depth=depth)
            for child_id in unit.children:
                child = units.get(child_id)
                if child:
                    node.children.append(build_node(child, depth + 1))
            return node

        # A unit is a root if it has no parentId, or its parentId isn't in the dict
        roots = [
            u for u in units.values()
            if not u.parent_id or u.parent_id not in known_ids
        ]

        # Stable sort: roots that appear as children of something should respect
        # whatever order their parent declared; for true roots just use title alpha.
        roots.sort(key=lambda u: u.title)

        return [build_node(r, 0) for r in roots]

    @staticmethod
    def compose_flat_timeline(units: Dict[str, NarrativeUnit]) -> List[Dict[str, Any]]:
        """
        Flatten units into a depth-first ordered list for timeline visualization.

        Assigns a sequential integer position based on tree traversal order.
        Returns plain dicts (safe for JSON serialization to the frontend).
        """
        tree = GraphComposer.compose_tree(units)
        flat: List[Dict[str, Any]] = []
        counter = [0]  # mutable int in closure

        def traverse(node: ComposedNode) -> None:
            u = node.unit
            flat.append({
                "unitId":    u.unit_id,
                "type":      u.type.value,
                "title":     u.title,
                "summary":   u.summary,
                "parentId":  u.parent_id,
                "children":  u.children,
                "depth":     node.depth,
                "position":  counter[0],
                "narrative": u.narrative.model_dump(by_alias=True),
                "view":      u.view.model_dump(by_alias=True),
            })
            counter[0] += 1
            for child in node.children:
                traverse(child)

        for root in tree:
            traverse(root)

        return flat

    @staticmethod
    def get_ancestry_path(units: Dict[str, NarrativeUnit], unit_id: str) -> List[str]:
        """
        Return the ancestry chain from root down to unit_id.
        e.g. ["book-01", "act-01", "chapter-01", "scene-the-anomaly"]
        """
        path: List[str] = []
        current_id: Optional[str] = unit_id
        visited: set = set()

        while current_id and current_id not in visited:
            visited.add(current_id)
            unit = units.get(current_id)
            if not unit:
                break
            path.append(current_id)
            current_id = unit.parent_id

        path.reverse()
        return path

    @staticmethod
    def get_units_by_type(
        units: Dict[str, NarrativeUnit],
        unit_type: UnitType,
    ) -> List[NarrativeUnit]:
        """Filter units by type. Order is arbitrary (use compose_flat_timeline for ordered views)."""
        return [u for u in units.values() if u.type == unit_type]

    @staticmethod
    def get_children(
        units: Dict[str, NarrativeUnit],
        parent_id: str,
    ) -> List[NarrativeUnit]:
        """
        Return ordered children of a given parent unit.
        Order follows the parent's children[] list.
        """
        parent = units.get(parent_id)
        if not parent:
            return []
        return [units[cid] for cid in parent.children if cid in units]
