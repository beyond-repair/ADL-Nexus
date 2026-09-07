"""
NEX-INT Contract — Frozen Vocabulary (v1.0)
===========================================
Authoritative contract for NEX-INT-005 and later.
Field names and status values are frozen.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Optional


class WorkStatus(str, Enum):
    ACCEPTED = "ACCEPTED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class WorkRequest:
    request_id: str
    description: str
    priority: str = "medium"
    role: Optional[str] = None
    agent_type: Optional[str] = None
    context: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class WorkResult:
    request_id: str
    status: WorkStatus
    task_id: Optional[str] = None
    agent_id: Optional[str] = None
    output: Any = None
    error: Optional[str] = None
