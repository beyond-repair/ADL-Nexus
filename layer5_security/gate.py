"""Minimal Security Fabric gate (v0.2)."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import time
import hashlib

@dataclass
class SecurityDecision:
    allowed: bool
    trust_score: float
    reason: str
    audit_id: str

class SecurityGate:
    """Fail-closed minimal gate."""

    def __init__(self, min_trust: float = 0.5):
        self.min_trust = min_trust
        self._log: list[dict[str, Any]] = []

    def evaluate(self, subsystem: str, action: str, context: dict[str, Any] | None = None) -> SecurityDecision:
        context = context or {}
        # v0.2 heuristic: local path actions are trusted; unknown elevated actions are not
        trust = 0.9 if action in {"status", "list_files", "summarize", "echo", "audit", "memory", "registry"} else 0.3
        if context.get("elevated"):
            trust = 0.2
        allowed = trust >= self.min_trust
        reason = "trust ok" if allowed else f"trust {trust:.2f} < {self.min_trust}"
        audit_id = hashlib.sha256(f"{subsystem}:{action}:{time.time()}".encode()).hexdigest()[:12]
        decision = SecurityDecision(allowed, trust, reason, audit_id)
        self._log.append({"subsystem": subsystem, "action": action, "decision": decision.__dict__, "ts": time.time()})
        return decision

    def get_log(self) -> list[dict[str, Any]]:
        return list(self._log)
