"""Execution state enum for durable Nexus records."""
from enum import Enum

class ExecutionState(str, Enum):
    ACCEPTED = "ACCEPTED"
    RUNNING = "RUNNING"
    RECOVERING = "RECOVERING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    INDETERMINATE = "INDETERMINATE"
