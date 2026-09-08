"""Append-only operation provenance (local, not a chain)."""

from __future__ import annotations

import hashlib
import json
import time
from typing import Any

_LOG: list[dict[str, Any]] = []


def record(kind: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = payload or {}
    body = {"kind": kind, "payload": payload, "ts": time.time()}
    digest = hashlib.sha256(json.dumps(body, sort_keys=True, default=str).encode()).hexdigest()[:16]
    body["id"] = digest
    _LOG.append(body)
    return {"ok": True, "entry": body, "claim": "local provenance; not BlockSwarm settlement"}


def list_entries(kind: str | None = None) -> dict[str, Any]:
    items = list(_LOG)
    if kind:
        items = [e for e in items if e.get("kind") == kind]
    return {"ok": True, "entries": items, "count": len(items)}


def get(entry_id: str) -> dict[str, Any]:
    for e in _LOG:
        if e.get("id") == entry_id:
            return {"ok": True, "entry": e}
    return {"ok": False, "error": f"unknown entry {entry_id}"}
