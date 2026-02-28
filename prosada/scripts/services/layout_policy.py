"""
Layout Policy helpers for v2 projects.

Policy values:
  - legacy-auto : existing behavior (pins are optional hints; auto fallback allowed)
  - strict-pins : schema-authoritative positioning (required pins; no auto fallback)
"""

from __future__ import annotations

from typing import Any, Dict

LAYOUT_POLICY_LEGACY_AUTO = "legacy-auto"
LAYOUT_POLICY_STRICT_PINS = "strict-pins"


def get_layout_policy(manifest: Dict[str, Any] | None) -> str:
    """
    Resolve layout policy from manifest.

    Supported locations:
      - manifest["layoutPolicy"]
      - manifest["settings"]["layoutPolicy"]
    """
    if not manifest:
        return LAYOUT_POLICY_LEGACY_AUTO
    top = manifest.get("layoutPolicy")
    if isinstance(top, str) and top:
        return top
    settings = manifest.get("settings")
    if isinstance(settings, dict):
        nested = settings.get("layoutPolicy")
        if isinstance(nested, str) and nested:
            return nested
    return LAYOUT_POLICY_LEGACY_AUTO


def is_strict_pins_policy(manifest: Dict[str, Any] | None) -> bool:
    return get_layout_policy(manifest) == LAYOUT_POLICY_STRICT_PINS

