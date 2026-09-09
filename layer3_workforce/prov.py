"""File-backed execution provenance. COMPLETE requires a record (NEX-INT-001 I1)."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from .store import state_dir


MANDATORY = (
    "task_id",
    "role",
    "adapter",
    "adapter_mode",
    "input_hash",
    "output_hash",
    "started_at",
    "completed_at",
    "result",
)


def hash_payload(value: Any) -> str:
    blob = json.dumps(value, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def write_record(record: dict[str, Any]) -> dict[str, Any]:
    missing = [k for k in MANDATORY if k not in record]
    if missing:
        raise ValueError(f"provenance missing mandatory fields: {missing}")
    if record["result"] not in ("SUCCESS", "REFUSED", "FAILED"):
        raise ValueError(f"invalid result: {record['result']}")
    path = state_dir() / "provenance" / f"{record['task_id']}.json"
    path.write_text(json.dumps(record, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    return {"ok": True, "path": str(path), "record": record}


def read_record(task_id: str) -> dict[str, Any] | None:
    path = state_dir() / "provenance" / f"{task_id}.json"
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None
