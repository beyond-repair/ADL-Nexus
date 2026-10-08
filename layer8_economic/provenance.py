"""Append-only local provenance log.

Each record stores the previous record's digest. The first record's previous
is empty. The digest covers kind, payload, and previous — not the wall clock.
The log is a file under .nexus_memory/ (same directory as kv.json).

This is not a blockchain and not BlockSwarm settlement.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

_LOG: list[dict[str, Any]] = []
_BOUND: Path | None = None


def _store_path() -> Path:
    root = Path(".nexus_memory")
    root.mkdir(parents=True, exist_ok=True)
    return (root / "provenance.jsonl").resolve()


def _reload_if_needed() -> None:
    """Load the cwd log when the process or working directory has no copy in RAM."""
    global _LOG, _BOUND
    path = _store_path()
    if _BOUND == path:
        return
    _BOUND = path
    _LOG = []
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            _LOG.append(json.loads(line))


def _linked_digest(kind: str, payload: dict[str, Any], previous: str) -> str:
    linked = {"kind": kind, "payload": payload, "previous": previous}
    raw = json.dumps(linked, sort_keys=True, default=str).encode()
    return hashlib.sha256(raw).hexdigest()[:16]


def record(kind: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    _reload_if_needed()
    payload = payload or {}
    previous = _LOG[-1]["id"] if _LOG else ""
    digest = _linked_digest(kind, payload, previous)
    body = {
        "kind": kind,
        "payload": payload,
        "previous": previous,
        "id": digest,
        "ts": time.time(),
    }
    _LOG.append(body)
    with _store_path().open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(body, sort_keys=True, default=str) + "\n")
    return {"ok": True, "entry": body, "claim": "local provenance; not BlockSwarm settlement"}


def list_entries(kind: str | None = None) -> dict[str, Any]:
    _reload_if_needed()
    items = list(_LOG)
    if kind:
        items = [e for e in items if e.get("kind") == kind]
    return {"ok": True, "entries": items, "count": len(items)}


def get(entry_id: str) -> dict[str, Any]:
    _reload_if_needed()
    for e in _LOG:
        if e.get("id") == entry_id:
            return {"ok": True, "entry": e}
    return {"ok": False, "error": f"unknown entry {entry_id}"}
