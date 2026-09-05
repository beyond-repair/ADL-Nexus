"""Claim-capped adapter for beyond-repair/sunder.

SCAN → SNAP → SUNDER loop is the target backend for the Agent Runtime.
This adapter does not claim full runtime interop until an optional import succeeds
and basic smoke tests pass.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class SunderStatus:
    available: bool
    mode: str  # "live" | "stub"
    message: str

class SunderAdapter:
    """Fail-soft bridge to sunder."""

    def __init__(self):
        self._sunder = None
        self.status = self._detect()

    def _detect(self) -> SunderStatus:
        try:
            import sunder  # type: ignore
            self._sunder = sunder
            return SunderStatus(True, "live", "sunder package importable")
        except Exception as e:
            return SunderStatus(False, "stub", f"sunder not available ({e.__class__.__name__})")

    def capabilities(self) -> list[str]:
        if self.status.available:
            return ["scan", "snap", "sunder", "spike", "anchor"]
        return ["scan_stub", "echo"]

    def scan(self, goal: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        if self.status.available and hasattr(self._sunder, "scan"):
            # Future: call real sunder.scan
            return {"mode": "live", "goal": goal, "note": "live path reserved"}
        return {
            "mode": "stub",
            "goal": goal,
            "path": context.get("path", "."),
            "message": "SunderAdapter operating in stub mode — install/enable sunder for live SCAN",
        }

    def run_goal(self, goal: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """High-level entry used by Nexus Agent Runtime."""
        scan_result = self.scan(goal, context)
        return {
            "adapter": "sunder",
            "status": self.status.__dict__,
            "scan": scan_result,
            "claim": "claim-capped; no full interop asserted",
        }
