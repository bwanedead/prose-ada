#!/usr/bin/env python3
"""
resolve_guidance_doc_stack.py — canonical story guidance documents for one unit

MANAGED ARTIFACT SOURCE (installed into story repos by tooling refresh).

Usage:
  python prosada/scripts/resolve_guidance_doc_stack.py --unit-id <unitId>
  python prosada/scripts/resolve_guidance_doc_stack.py --unit-id <unitId> --json

Behavior:
  - Uses engine endpoint (`/v2/guidance-doc-stack/{unitId}`) when available.
  - Falls back to local derived resolution when API is unavailable.
  - Produces deterministic output for story-agent guidance lookup.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.error import URLError, HTTPError
from urllib.request import urlopen


GUIDANCE_DOC_STACK_SCRIPT_VERSION = "1.0.0"


def _auto_detect_project(script_path: Path) -> Path:
    # Preferred installed location: <repo>/prosada/scripts/resolve_guidance_doc_stack.py
    candidate = script_path.parent.parent
    if (candidate / "manifest.json").exists():
        return candidate

    cwd = Path.cwd()
    if (cwd / "manifest.json").exists():
        return cwd
    if (cwd / "prosada" / "manifest.json").exists():
        return cwd / "prosada"
    return candidate


def _endpoint_url(base: str, unit_id: str) -> str:
    return f"{base.rstrip('/')}/v2/guidance-doc-stack/{unit_id}"


def _fetch_from_api(base: str, unit_id: str) -> dict:
    url = _endpoint_url(base, unit_id)
    with urlopen(url, timeout=5) as response:
        payload = response.read().decode("utf-8")
        return json.loads(payload)


def _resolve_locally(project_dir: Path, unit_id: str) -> dict:
    script_dir = Path(__file__).resolve().parent
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))

    from persistence.unit_repository import UnitRepository
    from services.guidance_doc_stack_service import GuidanceDocStackService

    repo = UnitRepository(project_dir)
    units = repo.load_all_units()
    manifest = repo.load_manifest()
    return GuidanceDocStackService.build(
        unit_id=unit_id,
        units=units,
        project_dir=project_dir,
        manifest=manifest,
    )


def _print_human(payload: dict) -> None:
    print("Guidance Document Stack")
    print(f"Target: {payload['unitId']} ({payload['unitType']})")
    print(f"Title: {payload['unitTitle']}")
    print(f"Documents: {payload['counts']['documents']}")
    print("")

    for doc in payload["documents"]:
        order = doc["governanceOrder"]
        applicability = doc["applicability"]
        if doc.get("canonicalDocPath"):
            display = doc["canonicalDocPath"]
            source = "doc"
        else:
            display = ", ".join(doc["sourceArtifactUnitIds"])
            source = "artifact-fallback"
        scopes = " -> ".join(doc["attachmentScopeUnitIds"])
        print(f"{order:>2}. [{source}] {display} ({applicability})")
        print(f"    scopes: {scopes}")

    if payload.get("unresolvedAttachments"):
        print("")
        print(f"Unresolved attachments: {len(payload['unresolvedAttachments'])}")
        for item in payload["unresolvedAttachments"]:
            print(f"  - {item['targetId']} (from {item['attachedAtUnitId']}): {item['reason']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="resolve_guidance_doc_stack",
        description="Resolve canonical story guidance document stack for a unit.",
    )
    parser.add_argument("--unit-id", required=True, help="Target unitId to resolve.")
    parser.add_argument("--project", default=None, help="Path to prosada/ project root.")
    parser.add_argument("--api-base", default="http://127.0.0.1:42100", help="ProsAda API base URL.")
    parser.add_argument(
        "--prefer-local",
        action="store_true",
        help="Skip API and resolve directly from local project files.",
    )
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable JSON.")
    args = parser.parse_args(argv)

    script_path = Path(__file__).resolve()
    project_dir = (
        Path(args.project).expanduser().resolve()
        if args.project
        else _auto_detect_project(script_path)
    )

    if not (project_dir / "manifest.json").exists():
        print(f"Error: project dir missing manifest.json: {project_dir}", file=sys.stderr)
        return 2

    payload = None
    api_error = None
    if not args.prefer_local:
        try:
            payload = _fetch_from_api(args.api_base, args.unit_id)
        except (URLError, HTTPError, TimeoutError, json.JSONDecodeError) as exc:
            api_error = exc

    if payload is None:
        try:
            payload = _resolve_locally(project_dir, args.unit_id)
        except KeyError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        except Exception as exc:
            if api_error is not None:
                print(f"API resolution failed: {api_error}", file=sys.stderr)
            print(f"Local resolution failed: {exc}", file=sys.stderr)
            return 1

    if args.json_output:
        print(json.dumps(payload, indent=2))
    else:
        _print_human(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
