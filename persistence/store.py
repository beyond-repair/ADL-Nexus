"""
NEX-INT-005 — Append-only durable store for ExecutionRecords.
File-backed JSONL for restart safety. No Workforce state stored.
"""

from __future__ import annotations

import json
import os
import threading
from pathlib import Path
from typing import Dict, List, Optional

from .execution_record import ExecutionRecord


class DurableExecutionStore:
    """
    Nexus-owned, restart-safe store.
    - Unique request_id constraint
    - Append / update by rewriting sealed records
    - Survives process restart
    """

    def __init__(self, path: str | Path = "./nexus_execution.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._index: Dict[str, ExecutionRecord] = {}
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                rec = ExecutionRecord.from_dict(data)
                self._index[rec.request_id] = rec

    def _rewrite(self) -> None:
        tmp = self.path.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            for rec in self._index.values():
                f.write(json.dumps(rec.to_dict(), default=str) + "\n")
        os.replace(tmp, self.path)

    def get(self, request_id: str) -> Optional[ExecutionRecord]:
        with self._lock:
            return self._index.get(request_id)

    def exists(self, request_id: str) -> bool:
        with self._lock:
            return request_id in self._index

    def put(self, record: ExecutionRecord) -> ExecutionRecord:
        with self._lock:
            record.seal()
            existing = self._index.get(record.request_id)
            if existing is not None:
                record.version = existing.version + 1
                record.created_at = existing.created_at
                record.seal()
            self._index[record.request_id] = record
            self._rewrite()
            return record

    def list_all(self) -> List[ExecutionRecord]:
        with self._lock:
            return list(self._index.values())

    def count(self) -> int:
        with self._lock:
            return len(self._index)
