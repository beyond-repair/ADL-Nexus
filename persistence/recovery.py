"""NEX-INT-006 — Recovery worker. No automatic re-drive."""
from __future__ import annotations
from typing import Any, List
from .execution_state import ExecutionState
from .store import DurableExecutionStore, ExecutionRecord

class ExecutionRecoveryWorker:
    def __init__(self, store: DurableExecutionStore, adapter: Any) -> None:
        self.store = store
        self.adapter = adapter

    def recover_all(self) -> List[ExecutionRecord]:
        recovered: List[ExecutionRecord] = []
        for rec in list(self.store.running()):
            recovered.append(self._recover_one(rec))
        return recovered

    def _recover_one(self, rec: ExecutionRecord) -> ExecutionRecord:
        evidence = None
        if hasattr(self.adapter, "evidence"):
            evidence = self.adapter.evidence(rec.request_id)

        if evidence is not None and getattr(evidence, "terminal", False):
            status = getattr(evidence, "status", None) or "COMPLETED"
            try:
                state = ExecutionState(status)
            except ValueError:
                state = ExecutionState.COMPLETED
            return self.store.finalize(
                rec.request_id,
                state,
                task_id=getattr(evidence, "task_id", None),
                agent_id=getattr(evidence, "agent_id", None),
                result=getattr(evidence, "output", None),
                error=getattr(evidence, "error", None),
                force=True,
            )

        return self.store.finalize(
            rec.request_id,
            ExecutionState.INDETERMINATE,
            error="recovery: no terminal Workforce evidence; re-drive forbidden",
            force=True,
        )
