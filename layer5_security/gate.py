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
        "evaluate", "put", "get", "info", "integrity", "execute_work",
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
            trust, allowed, reason, match = 0.0, False, f"policy deny: {action_l}", "deny"
        elif action_l in POLICY["allow"]:
            trust, allowed, reason, match = 0.95, True, "policy allow", "allow"
        else:
            trust, allowed, reason, match = 0.25, False, "unknown action heuristic trust=0.25", "heuristic"

        # Context override for tests / explicit deny
        if context.get("force_deny"):
            trust, allowed, reason, match = 0.0, False, "force_deny", "deny"

        if allowed and trust < self.min_trust:
            allowed, reason, match = False, f"trust {trust} < min_trust {self.min_trust}", "heuristic"

        audit_id = hashlib.sha256(f"{subsystem}:{action}:{time.time()}".encode()).hexdigest()[:12]
        d = SecurityDecision(allowed, trust, reason, audit_id, match)
        self._log.append({"subsystem": subsystem, "action": action, "decision": d.__dict__, "ts": time.time()})
        return d

    def get_log(self) -> list[dict[str, Any]]:
        return list(self._log)

    def policy_snapshot(self) -> dict[str, Any]:
        return {"allow": sorted(POLICY["allow"]), "deny": sorted(POLICY["deny"]), "min_trust": self.min_trust}
