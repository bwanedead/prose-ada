"""
Invariants Validator — v2

Validates a NarrativeUnit (or full project) for internal consistency before
persistence. Returns structured issues rather than raising exceptions — callers
decide whether errors block the operation or just generate warnings.

Rules
-----
ERROR (blocks save):
  1. unitId must be non-empty
  2. If parentId is set, parent must exist in the known units dict
  3. No cycles in the ancestry chain
  6. If unit.children[] lists X, then X.parentId must agree (points back here)

WARNING (non-blocking, reported to caller):
  4. If unit references parentId, the parent's children[] should list this unit
  5. If textRef is set, the referenced file should exist
     (missing file is allowed — it may be created later)
  7. Duplicate unitIds in children[]
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from domain.narrative_unit import NarrativeUnit, UnitType
from services.layout_policy import (
    LAYOUT_POLICY_STRICT_PINS,
    get_layout_policy,
    is_strict_pins_policy,
)


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

class IssueSeverity(str, Enum):
    ERROR   = "error"    # Must be resolved before save
    WARNING = "warning"  # Reported but does not block save


@dataclass
class ValidationIssue:
    severity: IssueSeverity
    unit_id: str
    field: str
    message: str

    def to_dict(self) -> dict:
        return {
            "severity": self.severity.value,
            "unitId":   self.unit_id,
            "field":    self.field,
            "message":  self.message,
        }


# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------

class V2Validator:
    """
    Stateless validator for v2 NarrativeUnits.
    All methods are static — instantiate is never required.
    """

    @staticmethod
    def validate_unit(
        unit: NarrativeUnit,
        all_units: Dict[str, NarrativeUnit],
        project_dir: Optional[Path] = None,
        manifest: Optional[Dict[str, Any]] = None,
    ) -> List[ValidationIssue]:
        """
        Validate a single unit in the context of all units.

        `all_units` should include the unit being validated (so self-referential
        checks work correctly for create operations).
        `project_dir` is used to check textRef file existence (optional).
        """
        issues: List[ValidationIssue] = []

        strict_pins = is_strict_pins_policy(manifest)

        # --- Rule 0: layoutPolicy value sanity ---
        policy = get_layout_policy(manifest)
        if policy not in ("legacy-auto", "strict-pins"):
            issues.append(ValidationIssue(
                severity=IssueSeverity.WARNING,
                unit_id=unit.unit_id or "(unknown)",
                field="manifest.layoutPolicy",
                message=(
                    f"Unknown layoutPolicy '{policy}'. "
                    f"Expected 'legacy-auto' or '{LAYOUT_POLICY_STRICT_PINS}'."
                ),
            ))

        # --- Rule 1: unitId must be non-empty ---
        if not unit.unit_id or not unit.unit_id.strip():
            issues.append(ValidationIssue(
                severity=IssueSeverity.ERROR,
                unit_id=unit.unit_id or "(empty)",
                field="unitId",
                message="unitId must not be empty",
            ))
            # Can't do further checks without a valid ID
            return issues

        # --- Rule 2: parentId must resolve ---
        if unit.parent_id and unit.parent_id not in all_units:
            issues.append(ValidationIssue(
                severity=IssueSeverity.ERROR,
                unit_id=unit.unit_id,
                field="parentId",
                message=f"parentId '{unit.parent_id}' does not refer to a known unit",
            ))

        # --- Rule 3: no cycles ---
        if unit.parent_id:
            visited: set = set()
            current_id: Optional[str] = unit.parent_id
            cycle_detected = False
            while current_id:
                if current_id == unit.unit_id:
                    cycle_detected = True
                    break
                if current_id in visited:
                    break
                visited.add(current_id)
                ancestor = all_units.get(current_id)
                if not ancestor:
                    break
                current_id = ancestor.parent_id
            if cycle_detected:
                issues.append(ValidationIssue(
                    severity=IssueSeverity.ERROR,
                    unit_id=unit.unit_id,
                    field="parentId",
                    message="cycle detected in ancestry chain",
                ))

        # --- Rule 4: parent's children[] should include this unit ---
        if unit.parent_id and unit.parent_id in all_units:
            parent = all_units[unit.parent_id]
            if unit.unit_id not in parent.children:
                issues.append(ValidationIssue(
                    severity=IssueSeverity.WARNING,
                    unit_id=unit.unit_id,
                    field="parentId",
                    message=(
                        f"unit references parent '{unit.parent_id}' but that parent's "
                        f"children[] list does not include '{unit.unit_id}'. "
                        "Update the parent file to add this unit to its children list."
                    ),
                ))

        # --- Rule 5: textRef file existence ---
        text_ref = unit.narrative.text_ref
        if text_ref and project_dir:
            text_path = project_dir / "units" / text_ref
            if not text_path.exists():
                issues.append(ValidationIssue(
                    severity=IssueSeverity.WARNING,
                    unit_id=unit.unit_id,
                    field="narrative.textRef",
                    message=(
                        f"textRef '{text_ref}' does not exist yet — "
                        "create the file when prose is ready"
                    ),
                ))

        # --- Rule 6: children[] must agree on their parentId ---
        # If this unit claims X as a child, X must point back here as its parent.
        # This prevents silent tree corruption from an agent typo on either side.
        for child_id in unit.children:
            child = all_units.get(child_id)
            if child and child.parent_id != unit.unit_id:
                issues.append(ValidationIssue(
                    severity=IssueSeverity.ERROR,
                    unit_id=unit.unit_id,
                    field="children",
                    message=(
                        f"children[] lists '{child_id}' but that unit's parentId is "
                        f"'{child.parent_id}', not '{unit.unit_id}'. "
                        "Either remove it from children[] or update the child's parentId."
                    ),
                ))

        # --- Rule 7: no duplicate IDs in children[] ---
        seen_children: set = set()
        for child_id in unit.children:
            if child_id in seen_children:
                issues.append(ValidationIssue(
                    severity=IssueSeverity.WARNING,
                    unit_id=unit.unit_id,
                    field="children",
                    message=f"children[] contains duplicate unitId '{child_id}'",
                ))
                break  # one warning per unit is enough
            seen_children.add(child_id)

        # --- Rule 8: link targetIds should resolve ---
        for lnk in unit.links:
            if lnk.target_id not in all_units:
                issues.append(ValidationIssue(
                    severity=IssueSeverity.WARNING,
                    unit_id=unit.unit_id,
                    field="links",
                    message=(
                        f"link targetId '{lnk.target_id}' does not resolve to a known unit "
                        "(forward references are allowed during authoring)"
                    ),
                ))

        # --- Rule 9: threadsAdvanced[] values should resolve to stream units ---
        for stream_id in unit.narrative.threads_advanced:
            target = all_units.get(stream_id)
            if target is None:
                issues.append(ValidationIssue(
                    severity=IssueSeverity.WARNING,
                    unit_id=unit.unit_id,
                    field="narrative.threadsAdvanced",
                    message=(
                        f"threadsAdvanced value '{stream_id}' does not resolve to a known unit. "
                        "Values must be stream unit IDs (not registry thread IDs)."
                    ),
                ))
            elif target.type != UnitType.STREAM:
                issues.append(ValidationIssue(
                    severity=IssueSeverity.WARNING,
                    unit_id=unit.unit_id,
                    field="narrative.threadsAdvanced",
                    message=(
                        f"threadsAdvanced value '{stream_id}' resolves to a unit of type "
                        f"'{target.type.value}', not 'stream'. "
                        "threadsAdvanced should reference stream unit IDs only."
                    ),
                ))

        # --- Rule 10: stream units must not appear in any children[] list ---
        if unit.type == UnitType.STREAM:
            for other in all_units.values():
                if other.unit_id != unit.unit_id and unit.unit_id in other.children:
                    issues.append(ValidationIssue(
                        severity=IssueSeverity.WARNING,
                        unit_id=unit.unit_id,
                        field="parentId",
                        message=(
                            f"stream unit '{unit.unit_id}' appears in '{other.unit_id}' children[] list. "
                            "Stream units are parallel tracks and must not be sequential children. "
                            "Remove it from children[] and set parentId to null."
                        ),
                    ))
                    break  # one warning per stream unit is enough

        # --- Rule 11+: strict pin policy enforcement ---
        if strict_pins:
            issues.extend(V2Validator._validate_strict_pins(unit, all_units, manifest))

        return issues

    @staticmethod
    def validate_all(
        units: Dict[str, NarrativeUnit],
        project_dir: Optional[Path] = None,
        manifest: Optional[Dict[str, Any]] = None,
    ) -> List[ValidationIssue]:
        """Validate all units in the project."""
        all_issues: List[ValidationIssue] = []
        for unit in units.values():
            all_issues.extend(
                V2Validator.validate_unit(unit, units, project_dir, manifest=manifest)
            )
        return all_issues

    @staticmethod
    def validate_strict_readiness(
        units: Dict[str, NarrativeUnit],
        project_dir: Optional[Path] = None,
        manifest: Optional[Dict[str, Any]] = None,
    ) -> List[ValidationIssue]:
        """
        Report issues that would block strict pin mode.

        This is intentionally independent of current manifest policy so teams
        can migrate safely before flipping layoutPolicy to strict-pins.
        """
        strict_manifest = dict(manifest or {})
        strict_manifest["layoutPolicy"] = LAYOUT_POLICY_STRICT_PINS
        return V2Validator.validate_all(units, project_dir, manifest=strict_manifest)

    # -------------------------------------------------------------------
    # Strict pin rules
    # -------------------------------------------------------------------

    @staticmethod
    def _layout_shape(unit: NarrativeUnit) -> tuple[bool, Optional[str], Optional[float], Optional[float]]:
        layout = unit.view.canvas.layout
        if not layout:
            return False, None, None, None
        mode = layout.mode
        cm = layout.coordinate_mode
        start = layout.start
        span = layout.span
        valid = (
            mode == "manual"
            and cm in ("absolute", "relative")
            and start is not None
            and span is not None
            and span > 0
        )
        return valid, cm, start, span

    @staticmethod
    def _is_content(unit: NarrativeUnit) -> bool:
        return unit.type in {
            UnitType.SERIES,
            UnitType.BOOK,
            UnitType.ACT,
            UnitType.SEQUENCE,
            UnitType.CHAPTER,
            UnitType.SCENE,
            UnitType.BEAT,
            UnitType.ARC,
        }

    @staticmethod
    def _validate_strict_pins(
        unit: NarrativeUnit,
        all_units: Dict[str, NarrativeUnit],
        manifest: Optional[Dict[str, Any]],
    ) -> List[ValidationIssue]:
        issues: List[ValidationIssue] = []

        valid_layout, coord_mode, _start, span = V2Validator._layout_shape(unit)
        if not valid_layout:
            issues.append(ValidationIssue(
                severity=IssueSeverity.ERROR,
                unit_id=unit.unit_id,
                field="view.canvas.layout",
                message=(
                    "strict-pins requires mode='manual' with coordinateMode "
                    "('absolute'|'relative') and start/span>0."
                ),
            ))
            return issues

        root_id = (manifest or {}).get("root")
        is_root = unit.unit_id == root_id

        # Root content unit must be absolute.
        if is_root and V2Validator._is_content(unit) and coord_mode != "absolute":
            issues.append(ValidationIssue(
                severity=IssueSeverity.ERROR,
                unit_id=unit.unit_id,
                field="view.canvas.layout.coordinateMode",
                message="Root content unit must use coordinateMode='absolute' in strict-pins.",
            ))

        # Non-root content units must be relative to parent.
        if V2Validator._is_content(unit) and not is_root:
            if not unit.parent_id:
                issues.append(ValidationIssue(
                    severity=IssueSeverity.ERROR,
                    unit_id=unit.unit_id,
                    field="parentId",
                    message="Non-root content unit must have parentId in strict-pins.",
                ))
            if coord_mode != "relative":
                issues.append(ValidationIssue(
                    severity=IssueSeverity.ERROR,
                    unit_id=unit.unit_id,
                    field="view.canvas.layout.coordinateMode",
                    message="Non-root content unit must use coordinateMode='relative' in strict-pins.",
                ))
            if unit.parent_id and unit.parent_id in all_units:
                parent = all_units[unit.parent_id]
                parent_valid, _, _, p_span = V2Validator._layout_shape(parent)
                if not parent_valid:
                    issues.append(ValidationIssue(
                        severity=IssueSeverity.ERROR,
                        unit_id=unit.unit_id,
                        field="parentId",
                        message=(
                            f"Parent '{unit.parent_id}' must have a valid manual layout "
                            "before relative children can resolve in strict-pins."
                        ),
                    ))
                elif p_span is not None and p_span <= 0:
                    issues.append(ValidationIssue(
                        severity=IssueSeverity.ERROR,
                        unit_id=unit.unit_id,
                        field="parentId",
                        message=f"Parent '{unit.parent_id}' has non-positive span.",
                    ))

        # Stream units must use explicit absolute pins in strict mode (v1 strict contract).
        if unit.type == UnitType.STREAM and coord_mode != "absolute":
            issues.append(ValidationIssue(
                severity=IssueSeverity.ERROR,
                unit_id=unit.unit_id,
                field="view.canvas.layout.coordinateMode",
                message="Stream units must use coordinateMode='absolute' in strict-pins.",
            ))

        return issues
