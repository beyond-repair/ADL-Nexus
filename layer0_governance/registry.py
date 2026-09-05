"""Minimal subsystem registration and request evaluation."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import time
import hashlib
import json

_REGISTRY: dict[str, dict[str, Any]] = {}
_AUDIT: list[dict[str, Any]] = []

@dataclass
class GovernanceDecision:
    allowed: bool
    reason: str
    claim_level: int
    audit_id: str

def register_subsystem(name: str, layer: int, claim_level: int, capabilities: list[str]) -> str:
    """Register a subsystem. Returns registration hash."""
    entry = {
        "name": name,
        "layer": layer,
        "claim_level": claim_level,
        "capabilities": capabilities,
        "registered_at": time.time(),
    }
    payload = json.dumps(entry, sort_keys=True)
    reg_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]
    entry["reg_hash"] = reg_hash
    _REGISTRY[name] = entry
    _AUDIT.append({"event": "register", "entry": entry, "ts": time.time()})
    return reg_hash

def evaluate_request(subsystem: str, action: str, context: dict[str, Any] | None = None) -> GovernanceDecision:
    """Fail-closed evaluation."""
    if subsystem not in _REGISTRY:
        decision = GovernanceDecision(False, f"Subsystem '{subsystem}' not registered", 0, "")
    else:
        entry = _REGISTRY[subsystem]
        # v0.1: allow only if claim_level <= 2 and action is in capabilities or is 'status'
        allowed = action == "status" or action in entry.get("capabilities", [])
        reason = "allowed" if allowed else f"Action '{action}' not in declared capabilities"
        decision = GovernanceDecision(allowed, reason, entry["claim_level"], "")
    audit_id = hashlib.sha256(f"{subsystem}:{action}:{time.time()}".encode()).hexdigest()[:12]
    decision.audit_id = audit_id
    _AUDIT.append({"event": "evaluate", "subsystem": subsystem, "action": action, "decision": decision.__dict__, "ts": time.time()})
    return decision

def get_audit_log() -> list[dict[str, Any]]:
    return list(_AUDIT)

def list_subsystems() -> dict[str, dict[str, Any]]:
    return dict(_REGISTRY)
