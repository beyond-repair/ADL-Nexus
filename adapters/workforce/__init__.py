"""Nexus-side Workforce adapter package (NEX-INT-002)."""
from .contract import WorkRequest, WorkResult, WorkStatus, Priority, WorkforceAdapter
from .adapter import InProcessWorkforceAdapter

__all__ = [
    "InProcessWorkforceAdapter",
    "WorkRequest",
    "WorkResult",
    "WorkStatus",
    "Priority",
    "WorkforceAdapter",
]
