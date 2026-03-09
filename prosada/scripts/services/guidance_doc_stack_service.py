"""
Guidance Doc Stack Service — canonical story guidance documents for a unit

Purpose:
  Resolve the document-facing guidance stack for a target unit so story agents
  can answer: "What guidance documents should I read for this scope?"

Contract:
  - Built on top of structural guidance inheritance (`GuidanceStackService`).
  - Includes only story guidance artifacts (currently `theory` / `ethos`).
  - Excludes governed story units (book/chapter/scene/beat/etc.).
  - Excludes operational/engine docs (managed docs, workflows, patch notes).
  - Collapses wrapper+doc duplication:
      * if `narrative.textRef` exists, surface one canonical document entry
      * otherwise, fall back to the artifact unit as the only guidance source
  - Derived at read-time; never persisted.

Ordering:
  - documents: global story docs first (path/name ASC),
               then nearestAttachmentScopeDepth DESC (more local first),
               firstAttachmentScopeDepth ASC (broader tie-break),
               canonicalDocPath ASC (if present),
               fallbackArtifactUnitId ASC
  - attachment scopes per document: scopeDepth ASC (root -> target)
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

from domain.narrative_unit import NarrativeUnit, UnitType
from services.guidance_stack_service import GuidanceStackService


_GUIDANCE_ARTIFACT_TYPES = {UnitType.THEORY.value, UnitType.ETHOS.value}


class GuidanceDocStackService:
    @staticmethod
    def build(
        unit_id: str,
        units: Dict[str, NarrativeUnit],
        project_dir: Path,
        manifest: Optional[dict] = None,
    ) -> dict:
        structural = GuidanceStackService.build(
            unit_id=unit_id,
            units=units,
            project_dir=project_dir,
            manifest=manifest,
        )

        docs_by_key: dict = {}
        excluded_non_guidance_artifacts: List[dict] = []

        # Include optional story-wide docs layer (docs/ethos/*.md) as additive
        # story guidance documents; these are not operational engine docs.
        for global_doc in structural["globalDocs"]:
            key = f"global:{global_doc['path']}"
            docs_by_key[key] = {
                "documentId": key,
                "sourceKind": "global_story_doc",
                "canonicalDocPath": GuidanceDocStackService._project_relative_path(
                    Path(project_dir), global_doc["path"]
                ),
                "canonicalDocExists": True,
                "title": global_doc["title"],
                "sourceArtifacts": [],
                "sourceArtifactUnitIds": [],
                "attachments": [],
                "firstAttachmentScopeDepth": -1,
                "nearestAttachmentScopeDepth": -1,
                "_hasLocalAttachment": False,
                "_hasInheritedAttachment": True,
                "_isGlobalStoryDoc": True,
            }

        for artifact in structural["artifacts"]:
            artifact_unit_id = artifact["artifactUnitId"]
            artifact_type = artifact["artifactType"]
            artifact_unit = units.get(artifact_unit_id)
            if artifact_unit is None:
                continue

            if artifact_type not in _GUIDANCE_ARTIFACT_TYPES:
                excluded_non_guidance_artifacts.append(
                    {
                        "artifactUnitId": artifact_unit_id,
                        "artifactTitle": artifact["artifactTitle"],
                        "artifactType": artifact_type,
                        "reason": "Artifact type is not a story guidance artifact",
                    }
                )
                continue

            canonical_doc_path, canonical_doc_exists = GuidanceDocStackService._resolve_canonical_doc(
                project_dir=Path(project_dir),
                unit=artifact_unit,
            )

            if canonical_doc_path:
                key = f"doc:{canonical_doc_path}"
            else:
                key = f"artifact:{artifact_unit_id}"

            existing = docs_by_key.get(key)
            if existing is None:
                existing = {
                    "documentId": key,
                    "sourceKind": "canonical_doc" if canonical_doc_path else "artifact_fallback",
                    "canonicalDocPath": canonical_doc_path,
                    "canonicalDocExists": canonical_doc_exists if canonical_doc_path else None,
                    "title": artifact["artifactTitle"],
                    "sourceArtifacts": [],
                    "sourceArtifactUnitIds": [],
                    "attachments": [],
                    "firstAttachmentScopeDepth": artifact["firstAttachmentScopeDepth"],
                    "nearestAttachmentScopeDepth": artifact["nearestAttachmentScopeDepth"],
                    "_hasLocalAttachment": False,
                    "_hasInheritedAttachment": False,
                    "_isGlobalStoryDoc": False,
                }
                docs_by_key[key] = existing

            source_artifact = {
                "artifactUnitId": artifact_unit_id,
                "artifactTitle": artifact["artifactTitle"],
                "artifactType": artifact_type,
                "summary": artifact["summary"],
                "guidance": artifact.get("guidance"),
                "applicability": artifact["applicability"],
            }
            if artifact_unit_id not in existing["sourceArtifactUnitIds"]:
                existing["sourceArtifactUnitIds"].append(artifact_unit_id)
                existing["sourceArtifacts"].append(source_artifact)

            existing["firstAttachmentScopeDepth"] = min(
                existing["firstAttachmentScopeDepth"],
                artifact["firstAttachmentScopeDepth"],
            )
            existing["nearestAttachmentScopeDepth"] = max(
                existing["nearestAttachmentScopeDepth"],
                artifact["nearestAttachmentScopeDepth"],
            )
            existing["_hasLocalAttachment"] = (
                existing["_hasLocalAttachment"] or artifact["hasLocalAttachment"]
            )
            existing["_hasInheritedAttachment"] = (
                existing["_hasInheritedAttachment"] or artifact["hasInheritedAttachment"]
            )

            existing["attachments"].extend(artifact["attachments"])

        documents = sorted(
            docs_by_key.values(),
            key=lambda doc: (
                0 if doc["_isGlobalStoryDoc"] else 1,
                -doc["nearestAttachmentScopeDepth"],
                doc["firstAttachmentScopeDepth"],
                doc["canonicalDocPath"] or "",
                doc["sourceArtifactUnitIds"][0] if doc["sourceArtifactUnitIds"] else "",
            ),
        )

        for idx, document in enumerate(documents):
            document["sourceArtifacts"] = sorted(
                document["sourceArtifacts"], key=lambda item: item["artifactUnitId"]
            )
            document["sourceArtifactUnitIds"] = sorted(document["sourceArtifactUnitIds"])
            document["attachments"] = sorted(
                document["attachments"],
                key=lambda att: (att["scopeDepth"], att["attachedAtUnitId"]),
            )
            document["attachmentScopeUnitIds"] = GuidanceDocStackService._ordered_unique_scope_ids(
                document["attachments"]
            )
            if document["_hasLocalAttachment"] and document["_hasInheritedAttachment"]:
                applicability = "local_and_inherited"
            elif document["_hasLocalAttachment"]:
                applicability = "local_only"
            else:
                applicability = "inherited_only"

            document["applicability"] = applicability
            document["governanceOrder"] = idx
            del document["_hasLocalAttachment"]
            del document["_hasInheritedAttachment"]
            del document["_isGlobalStoryDoc"]

        return {
            "unitId": structural["unitId"],
            "unitTitle": structural["unitTitle"],
            "unitType": structural["unitType"],
            "ordering": {
                "documents": (
                    "global story docs first (path/name ASC), "
                    "then nearestAttachmentScopeDepth DESC, "
                    "firstAttachmentScopeDepth ASC, "
                    "canonicalDocPath ASC, fallbackArtifactUnitId ASC"
                ),
                "attachments": "scopeDepth ASC (root->target)",
            },
            "documents": documents,
            "unresolvedAttachments": structural["unresolvedAttachments"],
            "excludedNonGuidanceArtifacts": excluded_non_guidance_artifacts,
            "derivedFrom": {
                "source": "guidance-stack",
                "unitId": structural["unitId"],
                "artifactCount": structural["counts"]["artifacts"],
                "globalDocsIncluded": True,
                "storyGuidanceTypes": sorted(_GUIDANCE_ARTIFACT_TYPES),
            },
            "counts": {
                "documents": len(documents),
                "sourceArtifacts": sum(len(doc["sourceArtifacts"]) for doc in documents),
                "globalStoryDocs": len(structural["globalDocs"]),
                "unresolvedAttachments": len(structural["unresolvedAttachments"]),
                "excludedNonGuidanceArtifacts": len(excluded_non_guidance_artifacts),
            },
        }

    @staticmethod
    def _resolve_canonical_doc(project_dir: Path, unit: NarrativeUnit) -> tuple[Optional[str], Optional[bool]]:
        text_ref = unit.narrative.text_ref
        if not text_ref:
            return None, None
        raw = str(text_ref).strip()
        if not raw:
            return None, None
        normalized = raw.replace("\\", "/")

        # Canonical contract: textRef is relative to units/. Keep backward
        # compatibility for existing explicit "units/..." values.
        candidate_units = project_dir / "units" / raw
        candidate_project = project_dir / raw
        if candidate_units.exists():
            return f"units/{normalized}", True
        if candidate_project.exists():
            rel = GuidanceDocStackService._project_relative_path(project_dir, str(candidate_project))
            return rel, True
        # Existence unknown at read-time if file missing; still surface intended path.
        if normalized.startswith("units/"):
            return normalized, False
        return f"units/{normalized}", False

    @staticmethod
    def _project_relative_path(project_dir: Path, maybe_abs_path: str) -> str:
        path = Path(maybe_abs_path)
        try:
            return str(path.relative_to(project_dir)).replace("\\", "/")
        except Exception:
            return str(path).replace("\\", "/")

    @staticmethod
    def _ordered_unique_scope_ids(attachments: List[dict]) -> List[str]:
        seen = set()
        ordered: List[str] = []
        for att in attachments:
            scope_id = att["attachedAtUnitId"]
            if scope_id in seen:
                continue
            seen.add(scope_id)
            ordered.append(scope_id)
        return ordered
