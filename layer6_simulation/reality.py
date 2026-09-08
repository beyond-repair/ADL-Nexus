"""Reality-before-action state (claim-capped).

Constructs a local world snapshot for an objective.
Does not load RealityOS. Does not claim a living organization twin.
"""

from __future__ import annotations

from typing import Any


class RealityEngine:
    name = "reality"
    layer = 6
    claim_level = 2
    capabilities = ("state", "info")

    def state(self, goal: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        text = (goal or "").strip()
        known = [k for k in ("path", "role", "budget", "constraint") if k in context]
        unknown = [k for k in ("market", "competitors", "capital", "live_org") if k not in context]
        actions = ["inspect", "propose", "simulate"]
        if "analyze" in text.lower() or "repo" in text.lower() or "build" in text.lower():
            actions = ["inspect", "plan", "simulate", "assign"]
        return {
            "ok": True,
            "claim": "local reality snapshot; not a live RealityOS twin",
            "claim_level": self.claim_level,
            "current_state": {"goal": text, "context_keys": sorted(context)},
            "known_facts": known,
            "unknown_variables": unknown,
            "available_resources": {
                "workforce_roles": ["engineer", "researcher", "analyst", "tester", "manager"],
                "pathways": ["runtime", "workforce", "development", "research", "security"],
            },
            "constraints": {
                "execute_requires_authorize": True,
                "remote_bind": False,
                "live_adapters": False,
            },
            "possible_actions": actions,
            "simulated_outcomes": [
                {"action": a, "confidence": 0.4 if a == "simulate" else 0.55, "cost": "unknown"}
                for a in actions
            ],
            "risk_cost_confidence": {
                "risk": "unvalidated alternatives",
                "cost": "unmeasured",
                "confidence": 0.45,
            },
            "recommended_path": actions,
        }

    def info(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "layer": self.layer,
            "claim_level": self.claim_level,
            "capabilities": list(self.capabilities),
            "live_realityos": False,
        }
