"""Local metrics snapshot for ADL Nexus Core."""

from __future__ import annotations
from typing import Any
import time

def snapshot(
    subsystems: dict,
    audit_len: int,
    security_log_len: int,
    memory_keys: int,
    experiments: int,
    adapter_status: dict[str, Any],
) -> dict[str, Any]:
    return {
        "ts": time.time(),
        "subsystems": len(subsystems),
        "audit_entries": audit_len,
        "security_events": security_log_len,
        "memory_keys": memory_keys,
        "research_experiments": experiments,
        "adapters": adapter_status,
        "claim": "local snapshot only; not a production telemetry channel",
    }
