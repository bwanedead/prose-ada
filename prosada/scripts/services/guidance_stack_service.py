"""
Guidance Stack Service — resolved inherited guidance governance stack

Purpose:
  Resolve the guidance governance stack for a target unit so agents and tools
  can deterministically answer:
    - what guidance artifacts govern this unit
    - where each artifact enters the hierarchy
    - whether each artifact is inherited, local, or both

Contract:
  - Guidance artifacts are canonical units attached via explicit links:
      usesTheory / usesEthos.
  - Inheritance walks ancestry root -> ... -> target and accumulates attachments.
  - A target includes ancestor-attached and directly-attached artifacts.
  - Optional global docs layer is discovered from project_dir/docs/ethos/*.md.
  - Stack is derived at read-time (never persisted as canonical story data).

Ordering:
  - globalDocs: path/name ascending
  - artifacts: nearest attachment scope depth DESC (more local first),
               then first attachment scope depth ASC (broader first tie-break),
               then artifactUnitId ASC
  - attachments per artifact: scope depth ASC (root -> target)
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

from domain.narrative_unit import LinkType, NarrativeUnit


_GUIDANCE_LINK_TYPES = {LinkType.USES_THEORY, LinkType.USES_ETHOS}


class GuidanceStackService:
    @staticmethod
    def build(
        unit_id: str,
        units: Dict[str, NarrativeUnit],
        project_dir: Path,
        manifest: Optional[dict] = None,
    ) -> dict:
        target = units.get(unit_id)
        if not target:
            raise KeyError(f"Unit '{unit_id}' not found")

        ancestry = GuidanceStackService._ancestry(unit_id, units)
        root_id = (manifest or {}).get("root")
        ancestry_ids = [u.unit_id for u in ancestry]

        artifacts_by_id: dict = {}
        unresolved: List[dict] = []
        target_depth = len(ancestry) - 1

        for depth, scope_unit in enumerate(ancestry):
            for link in scope_unit.links:
                if link.type not in _GUIDANCE_LINK_TYPES:
                    continue

                target_unit = units.get(link.target_id)
                attachment = {
                    "attachedAtUnitId": scope_unit.unit_id,
                    "attachedAtTitle": scope_unit.title,
                    "attachedAtType": scope_unit.type.value,
                    "linkType": link.type.value,
                    "label": link.label,
                    "scopeDepth": depth,
                }

                if target_unit is None:
                    unresolved.append(
                        {
                            **attachment,
                            "targetId": link.target_id,
                            "reason": "Link target does not resolve to a known unit",
                        }
                    )
                    continue

                existing = artifacts_by_id.get(target_unit.unit_id)
                if existing is None:
                    artifacts_by_id[target_unit.unit_id] = {
                        "artifactUnitId": target_unit.unit_id,
                        "artifactTitle": target_unit.title,
                        "artifactType": target_unit.type.value,
                        "summary": target_unit.summary,
                        "guidance": (
                            target_unit.guidance.model_dump(by_alias=True)
                            if target_unit.guidance is not None
                            else None
                        ),
                        "attachments": [attachment],
                        "firstAttachmentScopeDepth": depth,
                        "nearestAttachmentScopeDepth": depth,
                    }
                else:
                    existing["attachments"].append(attachment)
                    existing["firstAttachmentScopeDepth"] = min(existing["firstAttachmentScopeDepth"], depth)
                    existing["nearestAttachmentScopeDepth"] = max(existing["nearestAttachmentScopeDepth"], depth)

        artifacts = sorted(
            artifacts_by_id.values(),
            key=lambda a: (
                -a["nearestAttachmentScopeDepth"],
                a["firstAttachmentScopeDepth"],
                a["artifactUnitId"],
            ),
        )
        for idx, item in enumerate(artifacts):
            item["attachments"] = sorted(item["attachments"], key=lambda att: att["scopeDepth"])
            local = any(att["scopeDepth"] == target_depth for att in item["attachments"])
            inherited = any(att["scopeDepth"] < target_depth for att in item["attachments"])

            if local and inherited:
                applicability = "local_and_inherited"
            elif local:
                applicability = "local_only"
            else:
                applicability = "inherited_only"

            first_depth = item["firstAttachmentScopeDepth"]
            nearest_depth = item["nearestAttachmentScopeDepth"]
            first_scope = item["attachments"][0]
            nearest_scope = next(att for att in reversed(item["attachments"]) if att["scopeDepth"] == nearest_depth)

            item["applicability"] = applicability
            item["hasLocalAttachment"] = local
            item["hasInheritedAttachment"] = inherited
            item["attachmentScopeUnitIds"] = [att["attachedAtUnitId"] for att in item["attachments"]]
            item["firstAttachmentScopeDepth"] = first_depth
            item["nearestAttachmentScopeDepth"] = nearest_depth
            item["firstAttachmentScopeUnitId"] = first_scope["attachedAtUnitId"]
            item["nearestAttachmentScopeUnitId"] = nearest_scope["attachedAtUnitId"]
            item["governanceOrder"] = idx

        global_docs = GuidanceStackService._discover_global_ethos_docs(project_dir)

        return {
            "unitId": unit_id,
            "unitTitle": target.title,
            "unitType": target.type.value,
            "manifestRootUnitId": root_id,
            "ancestry": [
                {
                    "unitId": u.unit_id,
                    "title": u.title,
                    "type": u.type.value,
                    "isTarget": u.unit_id == unit_id,
                }
                for u in ancestry
            ],
            "includesManifestRoot": root_id in ancestry_ids if root_id else False,
            "ancestryStartUnitId": ancestry[0].unit_id if ancestry else None,
            "ordering": {
                "globalDocs": "path,name ascending",
                "artifacts": (
                    "nearestAttachmentScopeDepth DESC, "
                    "firstAttachmentScopeDepth ASC, artifactUnitId ASC"
                ),
                "attachments": "scopeDepth ASC (root->target)",
            },
            "globalDocs": global_docs,
            "artifacts": artifacts,
            "unresolvedAttachments": unresolved,
            "counts": {
                "ancestry": len(ancestry),
                "globalDocs": len(global_docs),
                "artifacts": len(artifacts),
                "unresolvedAttachments": len(unresolved),
            },
        }

    @staticmethod
    def _ancestry(unit_id: str, units: Dict[str, NarrativeUnit]) -> List[NarrativeUnit]:
        chain: List[NarrativeUnit] = []
        seen: set = set()
        current = units.get(unit_id)
        while current is not None and current.unit_id not in seen:
            chain.append(current)
            seen.add(current.unit_id)
            parent_id = current.parent_id
            current = units.get(parent_id) if parent_id else None
        chain.reverse()  # root -> ... -> target
        return chain

    @staticmethod
    def _discover_global_ethos_docs(project_dir: Path) -> List[dict]:
        docs_dir = Path(project_dir) / "docs" / "ethos"
        if not docs_dir.exists():
            return []

        docs: List[dict] = []
        for path in sorted(docs_dir.glob("*.md")):
            docs.append(
                {
                    "path": str(path),
                    "name": path.name,
                    "title": path.stem.replace("-", " "),
                }
            )
        return docs
