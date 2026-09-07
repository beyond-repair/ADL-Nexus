"""NEX-INT-005/006 — Durable execution identity store (Nexus-owned)."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from pathlib import Path
import json, os, threading
from .execution_state import ExecutionState

def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class ExecutionRecord:
    request_id: str
    state: ExecutionState
    governance_audit_id: str = ""
    security_audit_id: str = ""
    workforce_task_id: Optional[str] = None
    workforce_agent_id: Optional[str] = None
    result: Any = None
    error: Optional[str] = None
    created_at: str = field(default_factory=_utc_now)
    updated_at: str = field(default_factory=_utc_now)
    version: int = 1

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["state"] = self.state.value
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExecutionRecord":
        return cls(
            request_id=data["request_id"],
            state=ExecutionState(data["state"]),
            governance_audit_id=data.get("governance_audit_id", ""),
            security_audit_id=data.get("security_audit_id", ""),
            workforce_task_id=data.get("workforce_task_id"),
            workforce_agent_id=data.get("workforce_agent_id"),
            result=data.get("result"),
            error=data.get("error"),
            created_at=data.get("created_at", _utc_now()),
            updated_at=data.get("updated_at", _utc_now()),
            version=int(data.get("version", 1)),
        )

class DurableExecutionStore:
    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path or "./nexus_execution.jsonl")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
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
                rec = ExecutionRecord.from_dict(json.loads(line))
                self._index[rec.request_id] = rec

    def _rewrite(self) -> None:
        tmp = self.path.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            for rec in self._index.values():
                f.write(json.dumps(rec.to_dict(), default=str) + "\n")
        os.replace(tmp, self.path)

    def get(self, request_id: str) -> Optional[ExecutionRecord]:
        with self._lock:
            return self._index.get(str(request_id))

    def running(self) -> List[ExecutionRecord]:
        with self._lock:
            return [r for r in self._index.values() if r.state is ExecutionState.RUNNING]

    def begin(self, request_id: str, gov_audit: str, sec_audit: str) -> ExecutionRecord:
        rid = str(request_id)
        with self._lock:
            existing = self._index.get(rid)
            if existing is not None:
                return existing
            rec = ExecutionRecord(
                request_id=rid,
                state=ExecutionState.ACCEPTED,
                governance_audit_id=gov_audit,
                security_audit_id=sec_audit,
            )
            self._index[rid] = rec
            self._rewrite()
            return rec

    def mark_running(self, request_id: str) -> ExecutionRecord:
        with self._lock:
            rec = self._index[str(request_id)]
            if rec.state in {ExecutionState.COMPLETED, ExecutionState.FAILED,
                            ExecutionState.REJECTED, ExecutionState.CANCELLED,
                            ExecutionState.INDETERMINATE}:
                return rec
            rec.state = ExecutionState.RUNNING
            rec.updated_at = _utc_now()
            rec.version += 1
            self._rewrite()
            return rec

    def finalize(
        self,
        request_id: str,
        state: ExecutionState,
        *,
        task_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        result: Any = None,
        error: Optional[str] = None,
        force: bool = False,
    ) -> ExecutionRecord:
        terminal = {
            ExecutionState.COMPLETED, ExecutionState.FAILED,
            ExecutionState.REJECTED, ExecutionState.CANCELLED,
            ExecutionState.INDETERMINATE,
        }
        with self._lock:
            rec = self._index[str(request_id)]
            if rec.state in terminal and not force:
                return rec
            rec.state = state
            if task_id is not None:
                rec.workforce_task_id = task_id
            if agent_id is not None:
                rec.workforce_agent_id = agent_id
            if result is not None:
                rec.result = result
            if error is not None:
                rec.error = error
            rec.updated_at = _utc_now()
            rec.version += 1
            self._rewrite()
            return rec
