"""Minimal subsystem registration and request evaluation.

ADL-Governance is an external dependency and is not imported. This module is
the local stand-in. It enforces MAX_CLAIM_LEVEL (2): registration above the
cap is rejected, and evaluate_request denies any stored claim above the cap.
That is not ADL-Governance integration.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import time
import hashlib
import json
from pathlib import Path

_REGISTRY: dict[str, dict[str, Any]] = {}
_AUDIT: list[dict[str, Any]] = []


def _audit_file() -> Path:
    return Path(".nexus_memory") / "audit.jsonl"


def persist_audit_record(record: dict[str, Any]) -> None:
    """Append one governance or security decision. Callers must not pass secrets."""
    path = _audit_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, sort_keys=True, default=str)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def read_persisted_audit() -> list[dict[str, Any]]:
    """Read the durable audit file. Does not use the in-memory list."""
    path = _audit_file()
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _audit(record: dict[str, Any]) -> None:
    record.setdefault("channel", "governance")
    _AUDIT.append(record)
    persist_audit_record(record)

# Local cap from the previous in-file rule "claim_level <= 2".
# Status does not bypass this cap. ADL-Governance is not consulted.
MAX_CLAIM_LEVEL = 2

@dataclass
class GovernanceDecision:
    allowed: bool
    reason: str
    claim_level: int
    audit_id: str

def register_subsystem(name: str, layer: int, claim_level: int, capabilities: list[str]) -> str:
    """Register a subsystem. Returns registration hash.

    Fails closed: claim_level above MAX_CLAIM_LEVEL is not stored.
    Re-registration may not raise an existing subsystem's claim level.
    """
    if not isinstance(claim_level, int) or isinstance(claim_level, bool):
        raise ValueError(f"claim_level {claim_level!r} is not an int")
    if claim_level > MAX_CLAIM_LEVEL:
        _audit({
            "event": "register_denied",
            "name": name,
            "claim_level": claim_level,
            "reason": f"claim_level {claim_level} exceeds cap {MAX_CLAIM_LEVEL}",
            "ts": time.time(),
        })
        raise ValueError(f"claim_level {claim_level} exceeds cap {MAX_CLAIM_LEVEL}")
    existing = _REGISTRY.get(name)
    if existing is not None and claim_level > int(existing["claim_level"]):
        _audit({
            "event": "register_denied",
            "name": name,
            "claim_level": claim_level,
            "reason": "self-elevate",
            "ts": time.time(),
        })
        raise ValueError(
            f"subsystem {name} cannot self-elevate claim_level "
            f"from {existing['claim_level']} to {claim_level}"
        )
    entry = {
        "name": name,
        "layer": layer,
        "claim_level": claim_level,
        "capabilities": list(capabilities),
        "registered_at": time.time(),
    }
    payload = json.dumps(entry, sort_keys=True)
    reg_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]
    entry["reg_hash"] = reg_hash
    _REGISTRY[name] = entry
    _audit({"event": "register", "entry": entry, "ts": time.time()})
    return reg_hash

def evaluate_request(subsystem: str, action: str, context: dict[str, Any] | None = None) -> GovernanceDecision:
    """Fail-closed evaluation.

    Allowed only when the subsystem is registered, its claim_level is
    <= MAX_CLAIM_LEVEL, and the action is declared or is 'status'.
    'status' does not bypass the claim cap. context is accepted for
    callers; this stand-in has no human-override flag (ADL-Governance
    is not imported).
    """
    del context  # no local override channel; do not invent one
    if subsystem not in _REGISTRY:
        decision = GovernanceDecision(False, f"Subsystem '{subsystem}' not registered", 0, "")
    else:
        entry = _REGISTRY[subsystem]
        level = int(entry["claim_level"])
        if level > MAX_CLAIM_LEVEL:
            allowed = False
            reason = f"claim_level {level} exceeds cap {MAX_CLAIM_LEVEL}"
        elif action == "status" or action in entry.get("capabilities", []):
            allowed = True
            reason = "allowed"
        else:
            allowed = False
            reason = f"Action '{action}' not in declared capabilities"
        decision = GovernanceDecision(allowed, reason, level, "")
    audit_id = hashlib.sha256(f"{subsystem}:{action}:{time.time()}".encode()).hexdigest()[:12]
    decision.audit_id = audit_id
    _audit({
        "event": "evaluate",
        "subsystem": subsystem,
        "action": action,
        "decision": decision.__dict__,
        "ts": time.time(),
    })
    return decision

def get_audit_log() -> list[dict[str, Any]]:
    """Governance decisions from disk, so a restarted process still has them."""
    return [
        row for row in read_persisted_audit()
        if row.get("channel", "governance") == "governance"
    ]

def list_subsystems() -> dict[str, dict[str, Any]]:
    return dict(_REGISTRY)
