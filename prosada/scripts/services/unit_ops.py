"""
Unit Operations Service — v2 Atomic Mutations

High-level, safe operations for growing story structure top-down.

Each op:
  1. Loads all affected units from disk
  2. Applies the change in memory
  3. Runs the full validator on all modified units
  4. If dryRun=True  → returns validation result without writing
  5. If errors exist → returns failure (caller decides whether to raise HTTP 422)
  6. Otherwise      → saves all modified files (per-file atomic: temp + rename)

Return type: OpsResult dataclass
  { success, dry_run, errors, warnings, modified }

Stream-hierarchy invariants enforced as hard errors (not just validator warnings):
  - insert_unit: rejects inserting a stream-type unit under a content parent.
    Streams have no structural parent — create them via POST /v2/unit with parentId=null.
  - move_unit: rejects moving a stream into any content hierarchy.

Link forward references:
  - link_units allows targetId to reference a unit that does not yet exist.
    The validator emits a WARNING (not ERROR) so agent workflows can link
    units in any order without being blocked. See V2Validator rule 8.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from domain.narrative_unit import LinkType, NarrativeUnit, UnitLink, UnitType
from services.v2_validator import IssueSeverity, V2Validator, ValidationIssue


# ---------------------------------------------------------------------------
# Return type
# ---------------------------------------------------------------------------

@dataclass
class OpsResult:
    success: bool
    dry_run: bool
    errors: List[dict] = field(default_factory=list)
    warnings: List[dict] = field(default_factory=list)
    modified: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "success":  self.success,
            "dryRun":   self.dry_run,
            "errors":   self.errors,
            "warnings": self.warnings,
            "modified": self.modified,
        }


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _validate_modified(
    unit_ids: List[str],
    all_units: Dict[str, NarrativeUnit],
    project_dir,
    manifest: Optional[dict] = None,
) -> tuple[List[dict], List[dict]]:
    """Validate every modified unit. Returns (error_dicts, warning_dicts)."""
    issues: List[ValidationIssue] = []
    for uid in dict.fromkeys(unit_ids):   # preserve order, deduplicate
        unit = all_units.get(uid)
        if unit:
            issues.extend(V2Validator.validate_unit(unit, all_units, project_dir, manifest=manifest))
    errors   = [i.to_dict() for i in issues if i.severity == IssueSeverity.ERROR]
    warnings = [i.to_dict() for i in issues if i.severity == IssueSeverity.WARNING]
    return errors, warnings


def _save_all(repo, units: List[NarrativeUnit]) -> None:
    """Write each unit to disk. Best-effort: writes all regardless of individual failures."""
    for unit in units:
        repo.save_unit(unit)


def _err(unit_id: str, field: str, message: str) -> OpsResult:
    """Quick failure constructor for pre-validation guard errors."""
    return OpsResult(
        success=False, dry_run=False,
        errors=[{"severity": "error", "unitId": unit_id, "field": field, "message": message}],
    )


# ---------------------------------------------------------------------------
# Operations
# ---------------------------------------------------------------------------

class UnitOps:
    """
    Atomic unit mutations for top-down story structure authoring.

    All methods are static. Each takes the repository as first arg and
    returns OpsResult. The caller converts to HTTP response.
    """

    @staticmethod
    def insert_unit(
        repo,
        parent_id: str,
        unit_dict: dict,
        insert_after: Optional[str] = None,
        dry_run: bool = False,
    ) -> OpsResult:
        """
        Create a new unit and splice its ID into parent.children[].

        unit_dict must include at minimum: unitId, type, title.
        parentId is overridden to parent_id regardless of what unit_dict contains.

        insert_after:
            None            → prepend (insert at index 0)
            known sibling   → insert after that sibling
            unknown/missing → append to end
        """
        all_units = repo.load_all_units()
        manifest = repo.load_manifest()

        parent = all_units.get(parent_id)
        if not parent:
            return _err(parent_id, "parentId", f"Parent unit '{parent_id}' not found")

        # Parse unit, enforcing correct parentId
        unit_data = {**unit_dict, "parentId": parent_id}
        try:
            unit = NarrativeUnit(**unit_data)
        except Exception as exc:
            uid = unit_dict.get("unitId", "?")
            return _err(uid, "schema", f"Unit schema error: {exc}")

        # Guard: streams must never be structural children of content units.
        # They are parallel tracks (parentId=null). Create via POST /v2/unit instead.
        if unit.type == UnitType.STREAM:
            return _err(
                unit.unit_id, "type",
                "Stream units cannot be inserted as children of content units. "
                "Streams are parallel tracks with no structural parent. "
                "Create them via POST /v2/unit with parentId omitted.",
            )

        # Guard: do not overwrite existing units via this op
        if unit.unit_id in all_units:
            return _err(
                unit.unit_id, "unitId",
                f"Unit '{unit.unit_id}' already exists. "
                "Use POST /v2/unit to update an existing unit.",
            )

        # Splice into parent.children[]
        if insert_after is None:
            parent.children.insert(0, unit.unit_id)
        elif insert_after in parent.children:
            idx = parent.children.index(insert_after)
            parent.children.insert(idx + 1, unit.unit_id)
        else:
            parent.children.append(unit.unit_id)

        all_units[unit.unit_id] = unit
        all_units[parent_id]    = parent
        modified = [unit.unit_id, parent_id]

        errors, warnings = _validate_modified(modified, all_units, repo.project_dir, manifest=manifest)

        if dry_run:
            return OpsResult(
                success=not errors, dry_run=True,
                errors=errors, warnings=warnings, modified=modified,
            )
        if errors:
            return OpsResult(success=False, dry_run=False, errors=errors, warnings=warnings)

        _save_all(repo, [unit, parent])
        return OpsResult(success=True, dry_run=False, warnings=warnings, modified=modified)

    # -----------------------------------------------------------------------

    @staticmethod
    def set_unit_streams(
        repo,
        unit_id: str,
        streams: List[str],
        dry_run: bool = False,
    ) -> OpsResult:
        """
        Replace narrative.threadsAdvanced[] with the supplied stream unit ID list.

        The validator (rule 9) will emit warnings for IDs that don't resolve
        to stream-type units — this is a warning, not an error, to allow
        forward-referencing streams that don't exist yet.
        """
        all_units = repo.load_all_units()
        manifest = repo.load_manifest()
        unit = all_units.get(unit_id)
        if not unit:
            return _err(unit_id, "unitId", f"Unit '{unit_id}' not found")

        unit.narrative.threads_advanced = streams
        all_units[unit_id] = unit
        modified = [unit_id]

        errors, warnings = _validate_modified(modified, all_units, repo.project_dir, manifest=manifest)

        if dry_run:
            return OpsResult(
                success=not errors, dry_run=True,
                errors=errors, warnings=warnings, modified=modified,
            )
        if errors:
            return OpsResult(success=False, dry_run=False, errors=errors, warnings=warnings)

        _save_all(repo, [unit])
        return OpsResult(success=True, dry_run=False, warnings=warnings, modified=modified)

    # -----------------------------------------------------------------------

    @staticmethod
    def link_units(
        repo,
        source_id: str,
        link_type: str,
        target_id: str,
        label: Optional[str] = None,
        dry_run: bool = False,
    ) -> OpsResult:
        """
        Append a UnitLink to source unit's links[].

        link_type must be a valid LinkType enum value:
          merges-into | branches-from | intersects | payoffFor | setsUp | dependsOn | usesTheory | usesEthos

        Semantic constraints (enforced by V2Validator):
          - usesTheory target should be type "theory" (warning on mismatch)
          - usesEthos target should be type "ethos" (warning on mismatch)
          - merges-into / branches-from / intersects require stream source+target (error on mismatch)
        """
        all_units = repo.load_all_units()
        manifest = repo.load_manifest()
        source = all_units.get(source_id)
        if not source:
            return _err(source_id, "sourceId", f"Source unit '{source_id}' not found")

        try:
            lt = LinkType(link_type)
        except ValueError:
            valid = [v.value for v in LinkType]
            return _err(
                source_id, "linkType",
                f"Invalid linkType '{link_type}'. Valid values: {valid}",
            )

        link = UnitLink(type=lt, target_id=target_id, label=label)
        source.links.append(link)
        all_units[source_id] = source
        modified = [source_id]

        errors, warnings = _validate_modified(modified, all_units, repo.project_dir, manifest=manifest)

        if dry_run:
            return OpsResult(
                success=not errors, dry_run=True,
                errors=errors, warnings=warnings, modified=modified,
            )
        if errors:
            return OpsResult(success=False, dry_run=False, errors=errors, warnings=warnings)

        _save_all(repo, [source])
        return OpsResult(success=True, dry_run=False, warnings=warnings, modified=modified)

    # -----------------------------------------------------------------------

    @staticmethod
    def move_unit(
        repo,
        unit_id: str,
        new_parent_id: str,
        insert_after: Optional[str] = None,
        dry_run: bool = False,
    ) -> OpsResult:
        """
        Move a unit to a new parent.

        Steps:
          1. Remove unit from old parent.children[]
          2. Update unit.parentId = new_parent_id
          3. Insert into new parent.children[] at requested position
        """
        all_units = repo.load_all_units()
        manifest = repo.load_manifest()

        unit = all_units.get(unit_id)
        if not unit:
            return _err(unit_id, "unitId", f"Unit '{unit_id}' not found")

        # Guard: stream units must remain at the top level (parentId=null).
        # Moving a stream into a content hierarchy would violate the parallel-tracks model.
        if unit.type == UnitType.STREAM:
            return _err(
                unit_id, "type",
                "Stream units cannot be moved into a content hierarchy. "
                "Streams are parallel tracks and must remain without a structural parent. "
                "To reorder streams, use reorder-children on the root or update view.canvas.y directly.",
            )

        new_parent = all_units.get(new_parent_id)
        if not new_parent:
            return _err(new_parent_id, "newParentId", f"New parent '{new_parent_id}' not found")

        modified: List[str] = [unit_id, new_parent_id]

        # Remove from old parent
        old_parent_id = unit.parent_id
        if old_parent_id and old_parent_id != new_parent_id:
            old_parent = all_units.get(old_parent_id)
            if old_parent and unit_id in old_parent.children:
                old_parent.children.remove(unit_id)
                all_units[old_parent_id] = old_parent
                modified.append(old_parent_id)

        # Update parentId
        unit.parent_id = new_parent_id

        # Avoid duplicate in destination
        if unit_id in new_parent.children:
            new_parent.children.remove(unit_id)

        # Splice into new parent
        if insert_after is None:
            new_parent.children.insert(0, unit_id)
        elif insert_after in new_parent.children:
            idx = new_parent.children.index(insert_after)
            new_parent.children.insert(idx + 1, unit_id)
        else:
            new_parent.children.append(unit_id)

        all_units[unit_id]      = unit
        all_units[new_parent_id] = new_parent

        errors, warnings = _validate_modified(modified, all_units, repo.project_dir, manifest=manifest)

        if dry_run:
            return OpsResult(
                success=not errors, dry_run=True,
                errors=errors, warnings=warnings, modified=modified,
            )
        if errors:
            return OpsResult(success=False, dry_run=False, errors=errors, warnings=warnings)

        unique_ids  = list(dict.fromkeys(modified))
        units_batch = [all_units[uid] for uid in unique_ids if uid in all_units]
        _save_all(repo, units_batch)
        return OpsResult(success=True, dry_run=False, warnings=warnings, modified=unique_ids)

    # -----------------------------------------------------------------------

    @staticmethod
    def reorder_children(
        repo,
        parent_id: str,
        ordered_child_ids: List[str],
        dry_run: bool = False,
    ) -> OpsResult:
        """
        Replace parent.children[] with a new ordering of the same IDs.

        ordered_child_ids must contain exactly the same set of IDs as the
        current children[] — no additions or deletions are permitted.
        Use insert_unit / move_unit for structural changes.
        """
        all_units = repo.load_all_units()
        manifest = repo.load_manifest()
        parent = all_units.get(parent_id)
        if not parent:
            return _err(parent_id, "parentId", f"Parent unit '{parent_id}' not found")

        current_set  = set(parent.children)
        provided_set = set(ordered_child_ids)

        if current_set != provided_set:
            added   = sorted(provided_set - current_set)
            removed = sorted(current_set - provided_set)
            parts   = []
            if added:   parts.append(f"unexpected additions: {added}")
            if removed: parts.append(f"missing IDs: {removed}")
            return _err(
                parent_id, "orderedChildIds",
                "orderedChildIds must contain exactly the same IDs as current children[]. "
                + "; ".join(parts),
            )

        parent.children = ordered_child_ids
        all_units[parent_id] = parent
        modified = [parent_id]

        errors, warnings = _validate_modified(modified, all_units, repo.project_dir, manifest=manifest)

        if dry_run:
            return OpsResult(
                success=not errors, dry_run=True,
                errors=errors, warnings=warnings, modified=modified,
            )
        if errors:
            return OpsResult(success=False, dry_run=False, errors=errors, warnings=warnings)

        _save_all(repo, [parent])
        return OpsResult(success=True, dry_run=False, warnings=warnings, modified=modified)
