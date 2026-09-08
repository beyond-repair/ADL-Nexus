"""Universal objective engine — advise first, execute only after authorize.

This is the product spine. It does not deploy businesses, move money,
or call live siblings.
"""

from __future__ import annotations

import uuid
from typing import Any

from layer3_workforce.roles import assign
from layer6_simulation.reality import RealityEngine
from layer8_economic.provenance import record as prov_record, get as prov_get


_PROPOSALS: dict[str, dict[str, Any]] = {}


class ObjectiveEngine:
    name = "objective"
    claim_level = 2

    def __init__(self) -> None:
        self.reality = RealityEngine()

    def think(self, goal: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        reality = self.reality.state(goal, context)
        pid = uuid.uuid4().hex[:12]
        proposal = {
            "id": pid,
            "goal": goal,
            "status": "proposed",
            "authorized": False,
            "executed": False,
            "why": "reality constructed before action",
            "evidence": {"reality_claim": reality["claim"], "confidence": reality["risk_cost_confidence"]["confidence"]},
            "simulated_consequences": reality["simulated_outcomes"],
            "risk": reality["risk_cost_confidence"],
            "required_authority": "operator authorize",
            "recommended_path": reality["recommended_path"],
            "workforce_hint": "researcher" if "research" in goal.lower() else "engineer",
        }
        _PROPOSALS[pid] = proposal
        prov_record("think", {"proposal_id": pid, "goal": goal})
        return {
            "ok": True,
            "claim": "advice only; not execution",
            "reality": reality,
            "proposal": proposal,
        }

    def authorize(self, proposal_id: str, actor: str = "operator") -> dict[str, Any]:
        p = _PROPOSALS.get(proposal_id)
        if p is None:
            return {"ok": False, "error": f"unknown proposal {proposal_id}"}
        p["authorized"] = True
        p["status"] = "authorized"
        p["actor"] = actor
        prov_record("authorize", {"proposal_id": proposal_id, "actor": actor})
        return {"ok": True, "proposal": p}

    def commit(self, proposal_id: str) -> dict[str, Any]:
        p = _PROPOSALS.get(proposal_id)
        if p is None:
            return {"ok": False, "error": f"unknown proposal {proposal_id}"}
        if not p.get("authorized"):
            return {"ok": False, "error": "unauthorized — AI advises, it cannot execute"}
        assigned = assign(p.get("workforce_hint", "engineer"), p["goal"], note="from objective.commit")
        p["executed"] = True
        p["status"] = "committed"
        p["assignment"] = assigned
        entry = prov_record("commit", {"proposal_id": proposal_id, "assignment": assigned})
        return {
            "ok": True,
            "proposal": p,
            "provenance": entry,
            "claim": "local supervised assign only; no external deploy",
        }

    def get_proposal(self, proposal_id: str) -> dict[str, Any]:
        p = _PROPOSALS.get(proposal_id)
        if p is None:
            return {"ok": False, "error": f"unknown proposal {proposal_id}"}
        return {"ok": True, "proposal": p}

    def info(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "claim_level": self.claim_level,
            "open_proposals": sum(1 for p in _PROPOSALS.values() if p["status"] != "committed"),
            "capabilities": ["think", "authorize", "commit", "get_proposal"],
        }
