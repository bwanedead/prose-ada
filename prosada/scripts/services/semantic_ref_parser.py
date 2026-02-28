"""
Semantic Reference Parser — ProsAda Burst 10

Parses inline semantic annotations from narrative text fields and external prose files.

Syntax (v1):
    Visible Text[[kind:entity-id]]

Examples:
    Joey Valdez[[char:joey-valdez]]
    The Arboros lattice[[concept:arboros-lattice]]
    Red sigil[[symbol:red-sigil]]
    Blueberry Pond[[location:blueberry-pond]]

Supported kinds → RegistryType mapping:
    char     → characters
    concept  → concepts
    symbol   → symbols
    location → locations
    artifact → artifacts
    thread   → threads

Parse sources (v1):
    1. NarrativeUnit text fields:
       summary, narrative.notes, narrative.new_info, narrative.drip_hook,
       narrative.payoff_delivered, narrative.beauty_hooks
    2. External prose files referenced by narrative.textRef (if file exists)

Malformed annotations (missing brackets, empty kind/id, unknown kind) are silently
skipped. The parser never throws on plain text without any annotations.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set

from domain.narrative_unit import NarrativeUnit

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Registry kind → RegistryType value
KIND_TO_REGISTRY: Dict[str, str] = {
    "char":     "characters",
    "concept":  "concepts",
    "symbol":   "symbols",
    "location": "locations",
    "artifact": "artifacts",
    "thread":   "threads",
}

# All valid annotation kinds
VALID_KINDS: Set[str] = set(KIND_TO_REGISTRY.keys())

# Regex: match `Text[[kind:id]]` anywhere in a string.
# Group 1: visible text before [[ (may be empty)
# Group 2: kind
# Group 3: entity-id
_REF_PATTERN = re.compile(
    r"([^\[\n]*?)\[\[(\w+):([^\]\n]+)\]\]"
)

# Unit text fields to scan (in order)
_UNIT_TEXT_FIELDS = [
    ("summary",           lambda u: u.summary),
    ("notes",             lambda u: u.narrative.notes),
    ("newInfo",           lambda u: u.narrative.new_info),
    ("dripHook",          lambda u: u.narrative.drip_hook),
    ("payoffDelivered",   lambda u: u.narrative.payoff_delivered),
    ("beautyHooks",       lambda u: u.narrative.beauty_hooks),
]


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class SemanticRef:
    """A single resolved or unresolved semantic reference detected in text."""
    kind: str           # annotation kind (char, concept, …)
    entity_id: str      # stable entity id from the annotation
    visible_text: str   # the text before [[
    registry_type: str  # RegistryType value (characters, concepts, …) or "unknown"
    unit_id: str        # source NarrativeUnit unitId
    source_field: str   # field name or "prose_file"
    source_path: Optional[str] = None   # absolute path if from prose file
    resolved: bool = False  # True if entity_id found in its registry


@dataclass
class ParseResult:
    """
    Full parse result for a project.

    refs:           list of all SemanticRef objects (including unresolved)
    by_entity:      grouped by entity_id → list of refs
    by_unit:        grouped by unit_id   → list of refs
    unresolved:     refs whose entity_id is not in the registry
    """
    refs: List[SemanticRef] = field(default_factory=list)
    by_entity: Dict[str, List[SemanticRef]] = field(default_factory=dict)
    by_unit: Dict[str, List[SemanticRef]] = field(default_factory=dict)
    unresolved: List[SemanticRef] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Core parser
# ---------------------------------------------------------------------------

def _parse_text(text: str, unit_id: str, source_field: str,
                source_path: Optional[str] = None) -> List[SemanticRef]:
    """
    Extract all semantic refs from a single text string.

    Malformed or unrecognised annotations are silently skipped.
    """
    if not text:
        return []
    refs: List[SemanticRef] = []
    for m in _REF_PATTERN.finditer(text):
        visible = m.group(1).strip()
        kind = m.group(2).strip().lower()
        entity_id = m.group(3).strip()
        if not kind or not entity_id or kind not in VALID_KINDS:
            continue  # unknown kind — skip
        registry_type = KIND_TO_REGISTRY[kind]
        refs.append(SemanticRef(
            kind=kind,
            entity_id=entity_id,
            visible_text=visible,
            registry_type=registry_type,
            unit_id=unit_id,
            source_field=source_field,
            source_path=source_path,
        ))
    return refs


def _parse_unit(unit: NarrativeUnit, units_dir: Optional[Path] = None) -> List[SemanticRef]:
    """
    Extract all semantic refs from a single NarrativeUnit.

    Scans text fields first, then prose file if textRef is set and units_dir given.
    """
    refs: List[SemanticRef] = []

    # 1. Unit text fields
    for field_name, getter in _UNIT_TEXT_FIELDS:
        value = getter(unit)
        if value:
            refs.extend(_parse_text(value, unit.unit_id, field_name))

    # 2. External prose file
    if units_dir and unit.narrative.text_ref:
        prose_path = units_dir / unit.narrative.text_ref
        if prose_path.exists():
            try:
                prose_text = prose_path.read_text(encoding="utf-8")
                refs.extend(_parse_text(
                    prose_text, unit.unit_id, "prose_file",
                    source_path=str(prose_path)
                ))
            except OSError:
                pass  # unreadable — skip

    return refs


def parse_project(
    units: Dict[str, NarrativeUnit],
    registries_raw: Optional[Dict[str, dict]] = None,
    units_dir: Optional[Path] = None,
    scope_ids: Optional[Set[str]] = None,
    filter_kind: Optional[str] = None,
    filter_entity_id: Optional[str] = None,
) -> ParseResult:
    """
    Parse semantic refs from all units (and their prose files) in a project.

    Parameters
    ----------
    units           : all loaded NarrativeUnits keyed by unitId
    registries_raw  : optional dict of { registry_type_str: {entries: [...]} }
                      used to resolve entity IDs → resolved=True/False
    units_dir       : path to units/ folder (for textRef prose file scanning)
    scope_ids       : if provided, only scan units in this set
    filter_kind     : if provided, return only refs of this annotation kind
    filter_entity_id: if provided, return only refs for this entity_id

    Returns ParseResult with all refs grouped by entity and by unit.
    """
    # Build registry entity-id sets for resolution checks
    known_ids: Dict[str, Set[str]] = {}  # registry_type → set of entity IDs
    if registries_raw:
        for reg_type, reg_data in registries_raw.items():
            ids: Set[str] = set()
            for entry in reg_data.get("entries", []):
                eid = entry.get("id", "")
                if eid:
                    ids.add(eid)
            known_ids[reg_type] = ids

    all_refs: List[SemanticRef] = []

    for unit_id, unit in units.items():
        if scope_ids is not None and unit_id not in scope_ids:
            continue
        unit_refs = _parse_unit(unit, units_dir)
        # Mark resolution status
        for ref in unit_refs:
            reg_ids = known_ids.get(ref.registry_type, set())
            ref.resolved = ref.entity_id in reg_ids
        all_refs.extend(unit_refs)

    # Apply filters
    if filter_kind:
        all_refs = [r for r in all_refs if r.kind == filter_kind]
    if filter_entity_id:
        all_refs = [r for r in all_refs if r.entity_id == filter_entity_id]

    # Group results
    by_entity: Dict[str, List[SemanticRef]] = {}
    by_unit: Dict[str, List[SemanticRef]] = {}
    unresolved: List[SemanticRef] = []

    for ref in all_refs:
        by_entity.setdefault(ref.entity_id, []).append(ref)
        by_unit.setdefault(ref.unit_id, []).append(ref)
        if not ref.resolved:
            unresolved.append(ref)

    return ParseResult(
        refs=all_refs,
        by_entity=by_entity,
        by_unit=by_unit,
        unresolved=unresolved,
    )


def parse_result_to_response(result: ParseResult) -> dict:
    """
    Serialize a ParseResult to a JSON-serialisable dict for the API response.

    Response shape (grouped by entity):
    {
        "refs": [...],
        "byEntity": {
            "joey-valdez": {
                "kind": "char",
                "entityId": "joey-valdez",
                "registryType": "characters",
                "resolved": true,
                "occurrences": [
                    {"unitId": "scene-1", "visibleText": "Joey", "sourceField": "summary"},
                    ...
                ]
            },
            ...
        },
        "unresolvedCount": 2,
        "totalRefs": 5
    }
    """
    by_entity_out: Dict[str, dict] = {}

    for entity_id, refs in result.by_entity.items():
        # All refs for this entity share the same kind and registryType
        sample = refs[0]
        by_entity_out[entity_id] = {
            "kind": sample.kind,
            "entityId": entity_id,
            "registryType": sample.registry_type,
            "resolved": sample.resolved,
            "occurrences": [
                {
                    "unitId": r.unit_id,
                    "visibleText": r.visible_text,
                    "sourceField": r.source_field,
                    "sourcePath": r.source_path,
                }
                for r in refs
            ],
        }

    flat_refs = [
        {
            "kind": r.kind,
            "entityId": r.entity_id,
            "visibleText": r.visible_text,
            "registryType": r.registry_type,
            "unitId": r.unit_id,
            "sourceField": r.source_field,
            "sourcePath": r.source_path,
            "resolved": r.resolved,
        }
        for r in result.refs
    ]

    return {
        "refs": flat_refs,
        "byEntity": by_entity_out,
        "unresolvedCount": len(result.unresolved),
        "totalRefs": len(result.refs),
    }
