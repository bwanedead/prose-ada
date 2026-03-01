"""
Doctor Service — v2 Structural Health + Auto-Fix

Analyzes loaded units for structural drift and computes deterministic,
data-safe auto-fixes for issues that are unambiguous to repair.

Safe auto-fix types (all three are reversible and deterministic):
  remove_duplicate_child  — deduplicate children[] in place (keep first occurrence)
  add_missing_to_parent   — append child ID to parent.children[] when child.parentId
                            points to a parent that doesn't list it
  remove_dead_child       — remove a children[] entry whose target unit doesn't exist

NOT auto-fixed (require human judgment):
  - parentId disagreements where both sides have conflicting data
  - type mismatches (e.g. stream accidentally in children[])
  - cycle detection repairs
  - any ambiguity where silent repair could destroy authorial intent

Usage:
    report = DoctorService.scan(units, project_dir)
    result = DoctorService.apply_fixes(repo, fix_dicts, dry_run=True)
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from domain.narrative_unit import NarrativeUnit, UnitType
from services.v2_validator import IssueSeverity, V2Validator


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class DoctorFix:
    fix_type: str          # one of the three safe types above
    unit_id: str           # unit to modify
    data: Dict[str, Any]   # type-specific parameters
    description: str       # human-readable summary shown in Doctor UI

    def to_dict(self) -> dict:
        return {
            "fixType":     self.fix_type,
            "unitId":      self.unit_id,
            "data":        self.data,
            "description": self.description,
        }


@dataclass
class DoctorReport:
    issues: List[dict]          # raw ValidationIssue dicts from V2Validator
    fixes: List[DoctorFix]      # suggested auto-fixes
    error_count: int
    warning_count: int
    strict_readiness: Optional[dict] = None

    @property
    def fixable_count(self) -> int:
        return len(self.fixes)

    def to_dict(self) -> dict:
        return {
            "issues":       self.issues,
            "fixes":        [f.to_dict() for f in self.fixes],
            "errorCount":   self.error_count,
            "warningCount": self.warning_count,
            "fixableCount": self.fixable_count,
            "strictReadiness": self.strict_readiness,
        }


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------

class DoctorService:
    """Stateless diagnostic + repair service. All methods are static."""

    @staticmethod
    def scan(
        units: Dict[str, NarrativeUnit],
        project_dir=None,
        manifest: Optional[Dict[str, Any]] = None,
    ) -> DoctorReport:
        """
        Run full validation and compute auto-fix suggestions.

        Returns a DoctorReport with both the raw issues and a deduplicated
        list of deterministic fixes that can be applied via apply_fixes().
        """
        raw_issues = V2Validator.validate_all(units, project_dir, manifest=manifest)
        issue_dicts = [i.to_dict() for i in raw_issues]
        errors   = sum(1 for i in raw_issues if i.severity == IssueSeverity.ERROR)
        warnings = sum(1 for i in raw_issues if i.severity == IssueSeverity.WARNING)

        strict_issues = V2Validator.validate_strict_readiness(
            units,
            project_dir=project_dir,
            manifest=manifest,
        )
        strict_errors = [i for i in strict_issues if i.severity == IssueSeverity.ERROR]
        strict_warnings = [i for i in strict_issues if i.severity == IssueSeverity.WARNING]

        planning_issues = DoctorService._planning_warnings(
            units,
            project_dir=project_dir,
            manifest=manifest,
        )
        issue_dicts.extend(planning_issues)
        warnings += len(planning_issues)

        fixes = DoctorService._compute_fixes(units)
        return DoctorReport(
            issues=issue_dicts,
            fixes=fixes,
            error_count=errors,
            warning_count=warnings,
            strict_readiness={
                "layoutPolicyTarget": "strict-pins",
                "ready": len(strict_errors) == 0,
                "errorCount": len(strict_errors),
                "warningCount": len(strict_warnings),
                "issues": [i.to_dict() for i in strict_issues],
            },
        )

    @staticmethod
    def _planning_warnings(
        units: Dict[str, NarrativeUnit],
        project_dir=None,
        manifest: Optional[Dict[str, Any]] = None,
    ) -> List[dict]:
        """
        Read-only planning diagnostics (no auto-fixes).

        These warnings are advisory instrumentation checks for:
          - effort/reward mismatches
          - promise contract completeness/progression
          - cadence envelope activity mismatches
          - dead chapter runs with no rewards and no promise movement
        """
        issues: List[dict] = []

        def warn(unit_id: str, field: str, message: str) -> None:
            issues.append({
                "severity": "warning",
                "unitId": unit_id,
                "field": field,
                "message": message,
            })

        # 1) High effort units should usually pay with at least one reward token.
        for u in units.values():
            st = getattr(u, "structure", None)
            if not st:
                continue
            if getattr(st, "effort_load", None) == "high":
                tokens = getattr(st, "reward_tokens", None) or []
                if len(tokens) == 0:
                    warn(
                        u.unit_id,
                        "structure.rewardTokens",
                        "effortLoad='high' but no rewardTokens are authored.",
                    )

        # Canonical promise source: registries/promises.json
        promises = DoctorService._load_promises_registry(project_dir)
        transitions_by_unit: Dict[str, int] = {}
        for p in promises:
            pid = p.get("id") or p.get("promiseId") or "(unknown)"
            ptype = p.get("promiseType")
            if ptype and ptype not in {"mystery", "plot", "character", "thematic", "symbolic"}:
                warn(pid, "promiseType", f"Unknown promiseType '{ptype}'.")

            opened = p.get("openedAtUnitId")
            if not opened:
                warn(pid, "openedAtUnitId", "Promise is missing openedAtUnitId.")

            history = p.get("history") or []
            state = p.get("state")
            if state and state not in {
                "opened", "sharpened", "reframed", "delayed",
                "partially_paid", "paid", "inverted", "abandoned"
            }:
                warn(pid, "state", f"Unknown promise state '{state}'.")

            for h in history:
                uid = h.get("unitId")
                tr = h.get("transition")
                if uid:
                    transitions_by_unit[uid] = transitions_by_unit.get(uid, 0) + 1
                if tr and tr not in {
                    "opened", "sharpened", "reframed", "delayed",
                    "partially_paid", "paid", "inverted", "abandoned"
                }:
                    warn(pid, "history.transition", f"Unknown transition '{tr}'.")

            # 2) Promise target window exceeded with no movement/payment.
            tw = p.get("targetWindow") or {}
            if tw.get("kind") == "chapter_range":
                to_ch = tw.get("to")
                if isinstance(to_ch, int) and to_ch > 0:
                    max_ch = DoctorService._max_chapter_index(units)
                    moved = len(history) > 0 or bool(p.get("paidAtUnitId"))
                    if max_ch >= to_ch and not moved:
                        warn(
                            pid,
                            "targetWindow",
                            f"targetWindow chapter_range ended at {to_ch} with no promise movement/history.",
                        )

        # 3) Long chapter runs with no reward tokens and no promise movement.
        chapter_ids = DoctorService._chapter_ids_in_order(units, manifest)
        run_len = 0
        run_ids: List[str] = []
        for cid in chapter_ids:
            cu = units.get(cid)
            if not cu:
                continue
            tokens = (getattr(getattr(cu, "structure", None), "reward_tokens", None) or [])
            moved = transitions_by_unit.get(cid, 0) > 0
            if len(tokens) == 0 and not moved:
                run_len += 1
                run_ids.append(cid)
            else:
                if run_len >= 2:
                    for rid in run_ids:
                        warn(
                            rid,
                            "structure.rewardTokens",
                            "Chapter is part of a no-reward/no-transition run; consider adding reward token or promise movement.",
                        )
                run_len = 0
                run_ids = []
        if run_len >= 2:
            for rid in run_ids:
                warn(
                    rid,
                    "structure.rewardTokens",
                    "Chapter is part of a no-reward/no-transition run; consider adding reward token or promise movement.",
                )

        # 4) Stream cadence envelope exists but no unit maps to that stream.
        for u in units.values():
            if u.type != UnitType.STREAM:
                continue
            st = getattr(u, "structure", None)
            cadence = getattr(st, "cadence_envelope", None) if st else None
            if not cadence:
                continue
            has_activity = any(
                ou.type != UnitType.STREAM
                and u.unit_id in (ou.narrative.threads_advanced or [])
                for ou in units.values()
            )
            if not has_activity:
                warn(
                    u.unit_id,
                    "structure.cadenceEnvelope",
                    "cadenceEnvelope is defined but no units reference this stream in narrative.threadsAdvanced.",
                )

        return issues

    @staticmethod
    def _load_promises_registry(project_dir) -> List[dict]:
        if not project_dir:
            return []
        try:
            path = Path(project_dir) / "registries" / "promises.json"
            if not path.exists():
                return []
            data = json.loads(path.read_text(encoding="utf-8"))
            return data.get("entries", []) if isinstance(data, dict) else []
        except Exception:
            return []

    @staticmethod
    def _max_chapter_index(units: Dict[str, NarrativeUnit]) -> int:
        max_idx = 0
        for u in units.values():
            if u.type != UnitType.CHAPTER:
                continue
            idx = DoctorService._chapter_index_from_id_or_title(u)
            if idx > max_idx:
                max_idx = idx
        return max_idx

    @staticmethod
    def _chapter_index_from_id_or_title(unit: NarrativeUnit) -> int:
        # best-effort parser for chapter-03-* or "Chapter 3" title
        import re
        for src in (unit.unit_id, unit.title):
            m = re.search(r"(?:chapter[-_\s]?)(\d+)", src, flags=re.IGNORECASE)
            if m:
                try:
                    return int(m.group(1))
                except Exception:
                    pass
        return 0

    @staticmethod
    def _chapter_ids_in_order(units: Dict[str, NarrativeUnit], manifest: Optional[Dict[str, Any]]) -> List[str]:
        root = (manifest or {}).get("root")
        if not root or root not in units:
            # fallback deterministic by index parse
            chapters = [u for u in units.values() if u.type == UnitType.CHAPTER]
            chapters.sort(key=lambda u: (DoctorService._chapter_index_from_id_or_title(u), u.unit_id))
            return [u.unit_id for u in chapters]

        out: List[str] = []
        stack: List[str] = [root]
        while stack:
            uid = stack.pop()
            u = units.get(uid)
            if not u:
                continue
            if u.type == UnitType.CHAPTER:
                out.append(uid)
            for cid in reversed(u.children):
                if cid in units:
                    stack.append(cid)
        return out

    @staticmethod
    def _compute_fixes(units: Dict[str, NarrativeUnit]) -> List[DoctorFix]:
        """Scan all units for the three safe-fix patterns."""
        fixes: List[DoctorFix] = []
        seen: set = set()

        # Pre-compute which unit IDs already appear in at least one parent's
        # children[].  A unit that's already listed in *some* parent (even if
        # not the one it claims via parentId) represents a parentId disagreement
        # that requires human judgment — not a safe auto-fix.
        already_listed: set = set()
        for u in units.values():
            for cid in u.children:
                already_listed.add(cid)

        for unit in units.values():

            # --- Fix 1: duplicate IDs in children[] ---
            seen_children: set = set()
            has_dup = any(
                (cid in seen_children or seen_children.add(cid))  # type: ignore[func-returns-value]
                for cid in unit.children
            )
            # Simpler duplicate check:
            has_dup = len(unit.children) != len(set(unit.children))
            if has_dup:
                key = f"dedup:{unit.unit_id}"
                if key not in seen:
                    seen.add(key)
                    dupes = sorted({c for c in unit.children if unit.children.count(c) > 1})
                    fixes.append(DoctorFix(
                        fix_type="remove_duplicate_child",
                        unit_id=unit.unit_id,
                        data={"duplicates": dupes},
                        description=(
                            f"Deduplicate children[] of '{unit.title}' "
                            f"(duplicate IDs: {dupes})"
                        ),
                    ))

            # --- Fix 2: child claims parent but parent's children[] missing it ---
            # Guards:
            #   • stream units must never be inserted into a content hierarchy
            #   • if the unit already appears in a *different* parent's children[],
            #     this is a parentId disagreement — leave it for human judgment
            if (unit.parent_id
                    and unit.parent_id in units
                    and unit.type != UnitType.STREAM
                    and unit.unit_id not in already_listed):
                parent = units[unit.parent_id]
                if unit.unit_id not in parent.children:
                    key = f"add_to_parent:{unit.unit_id}"
                    if key not in seen:
                        seen.add(key)
                        fixes.append(DoctorFix(
                            fix_type="add_missing_to_parent",
                            unit_id=unit.unit_id,
                            data={"parentId": unit.parent_id},
                            description=(
                                f"Add '{unit.title}' to parent "
                                f"'{parent.title}' children[]"
                            ),
                        ))

            # --- Fix 3: dead reference in children[] (target doesn't exist) ---
            for cid in unit.children:
                if cid not in units:
                    key = f"remove_dead:{unit.unit_id}:{cid}"
                    if key not in seen:
                        seen.add(key)
                        fixes.append(DoctorFix(
                            fix_type="remove_dead_child",
                            unit_id=unit.unit_id,
                            data={"deadId": cid},
                            description=(
                                f"Remove non-existent reference '{cid}' "
                                f"from '{unit.title}' children[]"
                            ),
                        ))

        return fixes

    @staticmethod
    def apply_fixes(
        repo,
        fixes_raw: List[dict],
        dry_run: bool = False,
    ) -> dict:
        """
        Apply a list of fix dicts (as returned by scan().to_dict()["fixes"]).

        Returns an OpsResult-shaped dict:
            { success, dryRun, errors, warnings, modified }

        Callers can apply all fixes from a scan report or a user-selected subset.
        Atomic guarantee: each file write uses temp + rename (via repo.save_unit).
        """
        all_units = repo.load_all_units()
        manifest = repo.load_manifest()
        modified_ids: list = []
        apply_errors: List[dict] = []

        for fix_raw in fixes_raw:
            fix_type = fix_raw.get("fixType", "")
            unit_id  = fix_raw.get("unitId", "")
            data     = fix_raw.get("data", {})

            unit = all_units.get(unit_id)
            if not unit:
                apply_errors.append({
                    "fixType": fix_type, "unitId": unit_id,
                    "error": f"Unit '{unit_id}' not found",
                })
                continue

            if fix_type == "remove_duplicate_child":
                # Deduplicate in place, preserving first occurrence order
                seen_cids: dict = {}
                unit.children = [
                    c for c in unit.children
                    if not (c in seen_cids or seen_cids.__setitem__(c, True))
                ]
                modified_ids.append(unit_id)
                all_units[unit_id] = unit

            elif fix_type == "add_missing_to_parent":
                parent_id = data.get("parentId", "")
                parent = all_units.get(parent_id)
                if not parent:
                    apply_errors.append({
                        "fixType": fix_type, "unitId": unit_id,
                        "error": f"Parent '{parent_id}' not found",
                    })
                    continue
                if unit_id not in parent.children:
                    parent.children.append(unit_id)
                    modified_ids.append(parent_id)
                    all_units[parent_id] = parent

            elif fix_type == "remove_dead_child":
                dead_id = data.get("deadId", "")
                if dead_id in unit.children:
                    unit.children.remove(dead_id)
                    modified_ids.append(unit_id)
                    all_units[unit_id] = unit

            else:
                apply_errors.append({
                    "fixType": fix_type, "unitId": unit_id,
                    "error": f"Unknown fix type '{fix_type}'",
                })

        # Validate all modified units
        val_issues = []
        for uid in dict.fromkeys(modified_ids):
            u = all_units.get(uid)
            if u:
                val_issues.extend(V2Validator.validate_unit(u, all_units, repo.project_dir, manifest=manifest))

        val_errors   = [i.to_dict() for i in val_issues if i.severity == IssueSeverity.ERROR]
        val_warnings = [i.to_dict() for i in val_issues if i.severity == IssueSeverity.WARNING]
        all_errors   = apply_errors + val_errors

        unique_modified = list(dict.fromkeys(modified_ids))

        if dry_run:
            return {
                "success":  not all_errors,
                "dryRun":   True,
                "errors":   all_errors,
                "warnings": val_warnings,
                "modified": unique_modified,
            }

        if all_errors:
            return {
                "success":  False,
                "dryRun":   False,
                "errors":   all_errors,
                "warnings": val_warnings,
                "modified": [],
            }

        for uid in unique_modified:
            u = all_units.get(uid)
            if u:
                repo.save_unit(u)

        return {
            "success":  True,
            "dryRun":   False,
            "errors":   [],
            "warnings": val_warnings,
            "modified": unique_modified,
        }
