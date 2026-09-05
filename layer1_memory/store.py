"""Minimal local-first memory store."""

from __future__ import annotations
from typing import Any
import json
import hashlib
from pathlib import Path

class MemoryStore:
    def __init__(self, root: str | Path = ".nexus_memory"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self._kv_path = self.root / "kv.json"
        self._kv: dict[str, Any] = {}
        if self._kv_path.exists():
            self._kv = json.loads(self._kv_path.read_text())

    def put(self, key: str, value: Any) -> str:
        self._kv[key] = value
        self._persist()
        return hashlib.sha256(f"{key}:{value}".encode()).hexdigest()[:16]

    def get(self, key: str, default: Any = None) -> Any:
        return self._kv.get(key, default)

    def keys(self) -> list[str]:
        return list(self._kv.keys())

    def _persist(self) -> None:
        self._kv_path.write_text(json.dumps(self._kv, indent=2, default=str))
