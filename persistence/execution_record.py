"""
NEX-INT-005 — Durable Execution Identity
Nexus-owned record. Does not store Agent/Task objects.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional
from datetime import datetime, timezone
import json
import hashlib


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class GovernanceSnapshot:
    allowed: bool
    reason: str
    claim_level: int
    audit_id: str


@dataclass
class SecuritySnapshot:
    allowed: bool
    trust_score: float
    reason: str
    audit_id: str
    policy_match: str


@dataclass
class ExecutionRecord:
    """
    Single durable identity for a governed WorkRequest.
    Owned entirely by Nexus.
    """
    request_id: str
    description: str
    priority: str
    role: Optional[str]
    agent_type: Optional[str]
    governance: GovernanceSnapshot
    security: SecuritySnapshot
    status: str
    task_id: Optional[str] = None
    agent_id: Optional[str] = None
    output: Any = None
    error: Optional[str] = None
    created_at: str = field(default_factory=_utc_now)
    updated_at: str = field(default_factory=_utc_now)
    version: int = 1
    record_hash: str = ""

    def compute_hash(self) -> str:
        payload = {
            "request_id": self.request_id,
            "description": self.description,
            "priority": self.priority,
            "role": self.role,
            "agent_type": self.agent_type,
            "governance": asdict(self.governance),
            "security": asdict(self.security),
            "status": self.status,
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "output": self.output,
            "error": self.error,
            "version": self.version,
        }
        canonical = json.dumps(payload, sort_keys=True, default=str, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def seal(self) -> None:
        self.updated_at = _utc_now()
        self.record_hash = self.compute_hash()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "description": self.description,
            "priority": self.priority,
            "role": self.role,
            "agent_type": self.agent_type,
            "governance": asdict(self.governance),
            "security": asdict(self.security),
            "status": self.status,
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "output": self.output,
            "error": self.error,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "version": self.version,
            "record_hash": self.record_hash,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExecutionRecord":
        g = data["governance"]
        s = data["security"]
        return cls(
            request_id=data["request_id"],
            description=data["description"],
            priority=data.get("priority", "medium"),
            role=data.get("role"),
            agent_type=data.get("agent_type"),
            governance=GovernanceSnapshot(**g),
            security=SecuritySnapshot(**s),
            status=data["status"],
            task_id=data.get("task_id"),
            agent_id=data.get("agent_id"),
            output=data.get("output"),
            error=data.get("error"),
            created_at=data.get("created_at", _utc_now()),
            updated_at=data.get("updated_at", _utc_now()),
            version=data.get("version", 1),
            record_hash=data.get("record_hash", ""),
        )
