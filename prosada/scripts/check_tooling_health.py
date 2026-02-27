#!/usr/bin/env python3
"""
check_tooling_health.py — ProsAda repo-local tooling health check

MANAGED ARTIFACT — do not edit manually.
Version: 1.0.0
Refresh: POST /v2/tooling/refresh  (app backend)
         Or re-run: python scripts/check_tooling_health.py --heal

Usage:
    python prosada/scripts/check_tooling_health.py [options]

    --project PATH    Path to prosada/ directory
                      (default: auto-detected as two levels up from this script)
    --heal            Reinstall all stale or missing managed assets via app backend
    --json            Output status as machine-readable JSON
    --help            Show this help

Exit codes:
    0   All managed assets are present and checksums match
    1   One or more assets are missing or stale
    2   Project path not found or invalid
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

SCRIPT_VERSION = "1.0.0"
STATUS_OK = "ok"
STATUS_MISSING = "missing"
STATUS_STALE = "stale"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_tooling_json(project_dir: Path) -> dict:
    path = project_dir / "tooling.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _check_asset(project_dir: Path, rel_path: str, stored_checksum: str | None) -> str:
    full_path = project_dir / rel_path
    if not full_path.exists():
        return STATUS_MISSING
    if stored_checksum is None:
        return STATUS_OK  # no checksum recorded — treat as ok (legacy)
    actual = _sha256(full_path)
    return STATUS_OK if actual == stored_checksum else STATUS_STALE


def _auto_detect_project(script_path: Path) -> Path:
    """Script lives at <prosadaRoot>/scripts/check_tooling_health.py."""
    return script_path.parent.parent


def check_project(project_dir: Path) -> dict:
    """
    Return a structured status dict for all managed assets.

    {
        "overall": "ok" | "missing" | "stale",
        "projectDir": "...",
        "scripts": { "renderTimeline": {"status": "ok", ...}, ... },
        "docs": { "AGENT_START_HERE.md": {"status": "ok", ...}, ... }
    }
    """
    tooling = _load_tooling_json(project_dir)
    tools_meta = tooling.get("tools", {})
    docs_meta = tooling.get("docs", {})

    scripts_status = {}
    for name, meta in tools_meta.items():
        rel_path = meta.get("scriptPath", "")
        stored_checksum = meta.get("checksum")
        st = _check_asset(project_dir, rel_path, stored_checksum)
        scripts_status[name] = {
            "status": st,
            "installedVersion": meta.get("version"),
            "scriptPath": rel_path,
            "checksumMatch": st != STATUS_STALE,
        }

    docs_status = {}
    for name, meta in docs_meta.items():
        rel_path = meta.get("docPath", "")
        stored_checksum = meta.get("checksum")
        st = _check_asset(project_dir, rel_path, stored_checksum)
        docs_status[name] = {
            "status": st,
            "installedVersion": meta.get("version"),
            "docPath": rel_path,
            "checksumMatch": st != STATUS_STALE,
        }

    all_statuses = (
        [v["status"] for v in scripts_status.values()]
        + [v["status"] for v in docs_status.values()]
    )
    if STATUS_MISSING in all_statuses:
        overall = STATUS_MISSING
    elif STATUS_STALE in all_statuses:
        overall = STATUS_STALE
    else:
        overall = STATUS_OK

    return {
        "overall": overall,
        "projectDir": str(project_dir),
        "scripts": scripts_status,
        "docs": docs_status,
    }


def _heal_via_app(project_dir: Path) -> bool:
    """
    Attempt to heal by calling the app backend refresh endpoint.
    Returns True if successful, False otherwise.
    """
    try:
        import urllib.request, urllib.error
        url = "http://127.0.0.1:42100/v2/tooling/refresh"
        req = urllib.request.Request(url, method="POST",
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except Exception as exc:
        print(f"  Heal failed (is the app backend running?): {exc}", file=sys.stderr)
        return False


def _print_status(result: dict) -> None:
    overall = result["overall"]
    icon = "✓" if overall == STATUS_OK else ("✗" if overall == STATUS_MISSING else "~")
    print(f"\nProsAda Tooling Health  [{icon} {overall.upper()}]")
    print(f"Project: {result['projectDir']}\n")

    scripts = result.get("scripts", {})
    if scripts:
        print("Scripts:")
        for name, info in scripts.items():
            st = info["status"]
            mark = "✓" if st == STATUS_OK else "✗"
            ver = info.get("installedVersion") or "?"
            print(f"  {mark} {name:30s} {st:8s} v{ver}")

    docs = result.get("docs", {})
    if docs:
        print("Docs:")
        for name, info in docs.items():
            st = info["status"]
            mark = "✓" if st == STATUS_OK else "✗"
            ver = info.get("installedVersion") or "?"
            print(f"  {mark} {name:30s} {st:8s} v{ver}")
    print()


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        prog="check_tooling_health",
        description="Check ProsAda managed tooling health.",
    )
    p.add_argument("--project", default=None,
                   help="Path to prosada/ directory (auto-detected if omitted)")
    p.add_argument("--heal", action="store_true",
                   help="Reinstall stale/missing managed assets via app backend")
    p.add_argument("--json", action="store_true", dest="json_output",
                   help="Output status as JSON")
    args = p.parse_args(argv)

    if args.project:
        project_dir = Path(args.project).expanduser().resolve()
    else:
        project_dir = _auto_detect_project(Path(__file__).resolve())

    if not project_dir.exists():
        print(f"Error: project dir not found: {project_dir}", file=sys.stderr)
        return 2
    if not (project_dir / "manifest.json").exists():
        print(f"Error: no manifest.json in {project_dir}", file=sys.stderr)
        return 2

    result = check_project(project_dir)

    if args.json_output:
        print(json.dumps(result, indent=2))
    else:
        _print_status(result)

    if args.heal and result["overall"] != STATUS_OK:
        print("Healing: calling app backend refresh endpoint...")
        ok = _heal_via_app(project_dir)
        if ok:
            print("  Heal request accepted. Re-checking...")
            result = check_project(project_dir)
            if not args.json_output:
                _print_status(result)
        else:
            print("  Could not contact app backend. Manual refresh needed.")

    return 0 if result["overall"] == STATUS_OK else 1


if __name__ == "__main__":
    sys.exit(main())
