"""Security Fabric gate (v0.3) — policy table + trust heuristic."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import time
import hashlib

# Explicit allow / deny policy (fail-closed for unknown elevated actions)
POLICY = {
    "allow": {
        "status", "list_files", "summarize", "echo", "audit", "memory",
        "registry", "roles", "research", "adapters", "metrics", "scan", "run_goal",
        "evaluate", "put", "get", "info",
    },
    "deny": {
        "network_unrestricted", "exfiltrate", "privilege_escalate", "disable_governance",
    },
}

@dataclass
class SecurityDecision:
    allowed: bool
    trust_score: float
    reason: str
    audit_id: str
    policy_match: str  # allow | deny | heuristic

class SecurityGate:
    """Fail-closed gate with explicit policy table."""

    def __init__(self, min_trust: float = 0.5):
        self.min_trust = min_trust
        self._log: list[dict[str, Any]] = []

    def evaluate(self, subsystem: str, action: str, context: dict[str, Any] | None = None) -> SecurityDecision:
        context = context or {}
        action_l = action.lower().strip()

        if action_l in POLICY["deny"] or context.get("elevated") is True and action_l not in POLICY["allow"]:
            trust = 0.0
            allowed = False
            reason = f"policy deny: {action_l}"
            match = "deny"
        elif action_l in POLICY["allow"]:
            trust = 0.95
            allowed = True
            reason = "policy allow"
            match = "allow"
        else:
            # Unknown action — heuristic, biased toward deny
            trust = 0.25
            allowed = trust >= self.min_trust
            reason = f"unknown action heuristic trust={trust:.2f}"
            match = "heuristic"

        if context.get("force_deny"):
            allowed = False
            trust = 0.0
            reason = "force_deny"
            match = "deny"

        audit_id = hashlib.sha256(f"{subsystem}:{action}:{time.time()}".encode()).hexdigest()[:12]
        decision = SecurityDecision(allowed, trust, reason, audit_id, match)
        self._log.append({
            "subsystem": subsystem,
            "action": action,
            "decision": decision.__dict__,
            "ts": time.time(),
        })
        return decision

    def get_log(self) -> list[dict[str, Any]]:
        return list(self._log)

    def policy_snapshot(self) -> dict[str, Any]:
        return {"allow": sorted(POLICY["allow"]), "deny": sorted(POLICY["deny"]), "min_trust": self.min_trust}
