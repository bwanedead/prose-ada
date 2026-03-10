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

import re
from dataclasses import dataclass, field
from pathlib import Path
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


_BEAT_MARKER_RE = re.compile(r"\[\[\[([^\]\n]+)\]\]\]")


def _resolve_units_text_ref_path(project_dir: Path, text_ref: str) -> Optional[Path]:
    units_dir = (project_dir / "units").resolve()
    candidate = (units_dir / text_ref).resolve()
    if units_dir not in [candidate, *candidate.parents]:
        return None
    return candidate


def _marker_payload_parts(raw_marker: str) -> tuple[str, str]:
    payload = raw_marker[3:-3]
    parts = [p.strip() for p in payload.split("|")]
    if not parts:
        return "", "point"
    marker_id = (parts[0] or "").strip()
    boundary = "point"
    if len(parts) >= 3:
        maybe_boundary = (parts[-1] or "").strip().lower()
        if maybe_boundary in {"start", "end", "point"}:
            boundary = maybe_boundary
    return marker_id, boundary


def _find_beat_marker_occurrences(text: str, beat_id: str) -> list[dict]:
    occurrences: list[dict] = []
    for m in _BEAT_MARKER_RE.finditer(text or ""):
        marker_text = m.group(0)
        marker_id, boundary = _marker_payload_parts(marker_text)
        if marker_id != beat_id:
            continue
        occurrences.append(
            {
                "start": m.start(),
                "end": m.end(),
                "boundary": boundary,
                "text": marker_text,
            }
        )
    return occurrences


def _remove_beat_spans(text: str, beat_id: str) -> tuple[str, int, int]:
    """
    Remove all beat marker spans for a beat id.

    Returns: (rewritten_text, pair_span_count, marker_only_count)
    """
    occurrences = _find_beat_marker_occurrences(text, beat_id)
    if not occurrences:
        return text, 0, 0

    ranges_to_delete: list[tuple[int, int]] = []
    starts = [o for o in occurrences if o["boundary"] == "start"]
    ends = [o for o in occurrences if o["boundary"] == "end"]
    points = [o for o in occurrences if o["boundary"] == "point"]
    used_end_idx: set[int] = set()

    pair_count = 0
    marker_only_count = 0

    for st in starts:
        match_idx = None
        for idx, en in enumerate(ends):
            if idx in used_end_idx:
                continue
            if en["start"] >= st["start"]:
                match_idx = idx
                break
        if match_idx is not None:
            en = ends[match_idx]
            used_end_idx.add(match_idx)
            ranges_to_delete.append((st["start"], en["end"]))
            pair_count += 1
        else:
            ranges_to_delete.append((st["start"], st["end"]))
            marker_only_count += 1

    for idx, en in enumerate(ends):
        if idx in used_end_idx:
            continue
        ranges_to_delete.append((en["start"], en["end"]))
        marker_only_count += 1

    for pt in points:
        ranges_to_delete.append((pt["start"], pt["end"]))
        marker_only_count += 1

    ranges_to_delete.sort(key=lambda r: (r[0], r[1]))
    merged: list[tuple[int, int]] = []
    for start, end in ranges_to_delete:
        if not merged:
            merged.append((start, end))
            continue
        prev_start, prev_end = merged[-1]
        if start <= prev_end:
            merged[-1] = (prev_start, max(prev_end, end))
        else:
            merged.append((start, end))

    out_parts: list[str] = []
    cursor = 0
    for start, end in merged:
        out_parts.append(text[cursor:start])
        cursor = end
    out_parts.append(text[cursor:])
    rewritten = "".join(out_parts)
    return rewritten, pair_count, marker_only_count


def _strip_beat_markers(text: str, beat_id: str) -> tuple[str, int]:
    occurrences = _find_beat_marker_occurrences(text, beat_id)
    if not occurrences:
        return text, 0
    out = text
    for occ in reversed(occurrences):
        out = out[: occ["start"]] + out[occ["end"] :]
    return out, len(occurrences)


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

    # -----------------------------------------------------------------------

    @staticmethod
    def delete_unit(
        repo,
        unit_id: str,
        dry_run: bool = False,
        beat_prose_policy: str = "cancel",
    ) -> OpsResult:
        """
        Delete a unit only when doing so is structurally safe.

        Current policy: safe structural delete.
          - cannot delete the manifest root
          - cannot delete units with children (descendants remain owned)
          - removes structural references from parent.children[] lists
          - cannot delete while inbound links target this unit
          - cannot delete while referenced in narrative.threadsAdvanced[]
        """
        all_units = repo.load_all_units()
        manifest = repo.load_manifest()
        unit = all_units.get(unit_id)
        if not unit:
            return _err(unit_id, "unitId", f"Unit '{unit_id}' not found")

        policy = (beat_prose_policy or "cancel").strip().lower()
        allowed_policies = {"cancel", "remove_span", "strip_markers", "keep_orphaned"}
        if policy not in allowed_policies:
            return _err(
                unit_id,
                "beatProsePolicy",
                (
                    f"Invalid beat prose policy '{beat_prose_policy}'. "
                    f"Allowed values: {sorted(allowed_policies)}"
                ),
            )

        errors: List[dict] = []

        root_id = manifest.get("root")
        if root_id == unit_id:
            errors.append({
                "severity": "error",
                "unitId": unit_id,
                "field": "manifest.root",
                "message": (
                    f"Unit '{unit_id}' is the manifest root and cannot be deleted directly. "
                    "Move root ownership first, then retry deletion."
                ),
            })

        if unit.children:
            errors.append({
                "severity": "error",
                "unitId": unit_id,
                "field": "children",
                "message": (
                    f"Unit '{unit_id}' has children and cannot be deleted safely. "
                    "Reparent or delete descendants first."
                ),
            })

        parents_to_cleanup: List[NarrativeUnit] = []
        parent_originals: Dict[str, NarrativeUnit] = {}
        for other in all_units.values():
            if other.unit_id == unit_id:
                continue
            if unit_id in other.children:
                cleaned_children = [cid for cid in other.children if cid != unit_id]
                if cleaned_children != other.children:
                    if other.unit_id not in parent_originals:
                        parent_originals[other.unit_id] = other.model_copy(deep=True)
                    other.children = cleaned_children
                    all_units[other.unit_id] = other
                    parents_to_cleanup.append(other)

        prose_reconciliation_candidates: List[dict] = []
        prose_rewrites: List[dict] = []
        if unit.type == UnitType.BEAT:
            for parent in parents_to_cleanup:
                text_ref = (parent.narrative.text_ref or "").strip()
                if not text_ref:
                    continue
                prose_path = _resolve_units_text_ref_path(repo.project_dir, text_ref)
                if prose_path is None or not prose_path.exists():
                    continue
                try:
                    original = prose_path.read_text(encoding="utf-8")
                except Exception:
                    continue
                occurrences = _find_beat_marker_occurrences(original, unit_id)
                if not occurrences:
                    continue
                candidate = {
                    "parentUnitId": parent.unit_id,
                    "textRef": text_ref,
                    "path": str(prose_path),
                    "markerCount": len(occurrences),
                    "boundaries": [o["boundary"] for o in occurrences],
                }
                prose_reconciliation_candidates.append(candidate)

                if policy == "strip_markers":
                    rewritten, stripped_count = _strip_beat_markers(original, unit_id)
                    prose_rewrites.append(
                        {
                            **candidate,
                            "originalContent": original,
                            "content": rewritten,
                            "action": "strip_markers",
                            "strippedMarkers": stripped_count,
                        }
                    )
                elif policy == "remove_span":
                    rewritten, pair_count, marker_only_count = _remove_beat_spans(original, unit_id)
                    prose_rewrites.append(
                        {
                            **candidate,
                            "originalContent": original,
                            "content": rewritten,
                            "action": "remove_span",
                            "removedPairs": pair_count,
                            "removedMarkerOnly": marker_only_count,
                        }
                    )

            if prose_reconciliation_candidates and policy == "cancel":
                errors.append(
                    {
                        "severity": "error",
                        "unitId": unit_id,
                        "field": "prose.reconciliation",
                        "message": (
                            f"Beat '{unit_id}' has prose markers in parent prose files. "
                            "Deletion requires explicit beatProsePolicy: "
                            "remove_span | strip_markers | keep_orphaned."
                        ),
                        "details": {
                            "candidates": prose_reconciliation_candidates,
                            "allowedPolicies": ["remove_span", "strip_markers", "keep_orphaned"],
                            "selectedPolicy": policy,
                        },
                    }
                )

        inbound_link_sources = []
        inbound_stream_sources = []
        for other in all_units.values():
            if other.unit_id == unit_id:
                continue
            if any(link.target_id == unit_id for link in other.links):
                inbound_link_sources.append(other.unit_id)
            if unit_id in other.narrative.threads_advanced:
                inbound_stream_sources.append(other.unit_id)

        if inbound_link_sources:
            errors.append({
                "severity": "error",
                "unitId": unit_id,
                "field": "links",
                "message": (
                    f"Unit '{unit_id}' is referenced by links from: {sorted(inbound_link_sources)}. "
                    "Remove inbound links before deleting."
                ),
            })

        if inbound_stream_sources:
            errors.append({
                "severity": "error",
                "unitId": unit_id,
                "field": "narrative.threadsAdvanced",
                "message": (
                    f"Unit '{unit_id}' is referenced in threadsAdvanced by: {sorted(inbound_stream_sources)}. "
                    "Remove stream memberships before deleting."
                ),
            })

        if errors:
            return OpsResult(
                success=False,
                dry_run=dry_run,
                errors=errors,
                modified=[unit_id] + [p.unit_id for p in parents_to_cleanup],
            )

        remaining_units = dict(all_units)
        remaining_units.pop(unit_id, None)
        validation_issues = V2Validator.validate_all(
            remaining_units,
            project_dir=repo.project_dir,
            manifest=manifest,
        )
        validation_errors = [i.to_dict() for i in validation_issues if i.severity == IssueSeverity.ERROR]
        validation_warnings = [i.to_dict() for i in validation_issues if i.severity == IssueSeverity.WARNING]

        if validation_errors:
            return OpsResult(
                success=False,
                dry_run=dry_run,
                errors=validation_errors,
                warnings=validation_warnings,
                modified=[unit_id] + [p.unit_id for p in parents_to_cleanup],
            )

        modified_ids = [unit_id] + [p.unit_id for p in parents_to_cleanup]
        reconciliation_warnings: List[dict] = []
        if prose_reconciliation_candidates:
            if policy == "keep_orphaned":
                reconciliation_warnings.append(
                    {
                        "severity": "warning",
                        "unitId": unit_id,
                        "field": "prose.reconciliation",
                        "message": (
                            f"Kept orphaned prose markers for deleted beat '{unit_id}' "
                            "by explicit policy keep_orphaned."
                        ),
                        "details": {"candidates": prose_reconciliation_candidates},
                    }
                )
            elif policy in {"strip_markers", "remove_span"}:
                reconciliation_warnings.append(
                    {
                        "severity": "warning",
                        "unitId": unit_id,
                        "field": "prose.reconciliation",
                        "message": (
                            f"Applied prose reconciliation policy '{policy}' for deleted beat '{unit_id}'."
                        ),
                        "details": {
                            "rewrites": [
                                {
                                    k: v
                                    for k, v in rw.items()
                                    if k != "content"
                                }
                                for rw in prose_rewrites
                            ]
                        },
                    }
                )
        if dry_run:
            return OpsResult(
                success=True,
                dry_run=True,
                warnings=validation_warnings + reconciliation_warnings,
                modified=modified_ids,
            )

        written_prose: List[dict] = []
        for rewrite in prose_rewrites:
            try:
                Path(rewrite["path"]).write_text(rewrite["content"], encoding="utf-8")
                written_prose.append(rewrite)
            except Exception as exc:
                for prior in reversed(written_prose):
                    try:
                        Path(prior["path"]).write_text(prior["originalContent"], encoding="utf-8")
                    except Exception:
                        continue
                return _err(
                    unit_id,
                    "prose.reconciliation",
                    (
                        f"Failed writing prose reconciliation to {rewrite.get('path')!r}: {exc}. "
                        "Structural deletion was not applied."
                    ),
                )

        deleted = False
        try:
            deleted = repo.delete_unit(unit_id)
            if not deleted:
                raise RuntimeError(f"Unit '{unit_id}' not found at delete time")

            for parent in parents_to_cleanup:
                repo.save_unit(parent)
        except Exception as exc:
            # Roll back structure first.
            if deleted:
                try:
                    repo.save_unit(unit)
                except Exception:
                    pass
            for original_parent in parent_originals.values():
                try:
                    repo.save_unit(original_parent)
                except Exception:
                    continue

            # Roll back any prose rewrites.
            for rewrite in reversed(written_prose):
                try:
                    Path(rewrite["path"]).write_text(rewrite["originalContent"], encoding="utf-8")
                except Exception:
                    continue
            return _err(
                unit_id,
                "delete",
                (
                    f"Failed structural delete for '{unit_id}': {exc}. "
                    "Attempted to roll back prose and structure."
                ),
            )

        return OpsResult(
            success=True,
            dry_run=False,
            warnings=validation_warnings + reconciliation_warnings,
            modified=modified_ids,
        )
