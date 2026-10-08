"""Claim-capped adapter for beyond-repair/sunder.

SCAN → SNAP → SUNDER is the upstream target. This module does not implement
that loop. mode "live" is used only after sunder.scan is actually called and
returns. Import success without a call is "detected", not live. A missing
package is "unavailable". The string "live path reserved" is not a scan result.

Advertised capabilities are methods on this adapter only. snap, sunder, spike,
and anchor are not methods here and are not advertised.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass
class SunderStatus:
    available: bool
    mode: str  # "live" | "detected" | "unavailable"
    message: str

class SunderAdapter:
    """Fail-soft bridge to sunder. Never reports a reserved string as a live scan."""

    def __init__(self):
        self._sunder = None
        self.status = self._detect()

    def _detect(self) -> SunderStatus:
        try:
            import sunder  # type: ignore
        except ImportError as e:
            self._sunder = None
            return SunderStatus(False, "unavailable", f"sunder unavailable ({type(e).__name__}: {e})")
        except Exception as e:
            # Fail-soft for a broken optional package. The error is the status;
            # this is not a live scan and not a successful import.
            self._sunder = None
            return SunderStatus(False, "unavailable", f"sunder import failed ({type(e).__name__}: {e})")
        self._sunder = sunder
        scan = getattr(sunder, "scan", None)
        if not callable(scan):
            return SunderStatus(
                False, "detected",
                "sunder importable; scan is not callable; detected-not-executed",
            )
        return SunderStatus(
            False, "detected",
            "sunder importable; detected-not-executed until scan runs",
        )

    def capabilities(self) -> list[str]:
        """Methods this adapter actually implements. Not upstream verbs."""
        return ["scan", "run_goal", "capabilities"]

    def scan(self, goal: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        if self._sunder is None:
            return {
                "mode": "unavailable",
                "executed": False,
                "goal": goal,
                "path": context.get("path", "."),
                "message": self.status.message,
            }
        fn = getattr(self._sunder, "scan", None)
        if not callable(fn):
            return {
                "mode": "detected",
                "executed": False,
                "goal": goal,
                "note": "detected-not-executed",
                "message": "sunder.scan is not callable",
            }
        try:
            result = fn(goal, context)
        except Exception as e:
            return {
                "mode": "detected",
                "executed": False,
                "goal": goal,
                "note": "detected-not-executed",
                "error": f"{type(e).__name__}: {e}",
            }
        self.status = SunderStatus(True, "live", "sunder.scan executed")
        return {"mode": "live", "executed": True, "goal": goal, "result": result}

    def run_goal(self, goal: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """High-level entry used by Nexus Agent Runtime."""
        scan_result = self.scan(goal, context)
        return {
            "adapter": "sunder",
            "status": self.status.__dict__,
            "scan": scan_result,
            "claim": "claim-capped; no full interop asserted",
        }
