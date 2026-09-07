"""Thin Nexus-side Workforce adapter. No Agent/Task/Orchestrator imports."""
from __future__ import annotations
from typing import Any, Callable, Dict, Optional
from .contract import WorkRequest, WorkResult, WorkStatus

class InProcessWorkforceAdapter:
    def __init__(self, executor=None) -> None:
        self._executor = executor
        self._results: Dict[str, WorkResult] = {}
        self._invoke_count: Dict[str, int] = {}

    def submit(self, request: WorkRequest) -> WorkResult:
        rid = str(request.request_id)
        self._invoke_count[rid] = self._invoke_count.get(rid, 0) + 1
        if rid in self._results and self._results[rid].status in {
            WorkStatus.COMPLETED, WorkStatus.FAILED, WorkStatus.REJECTED, WorkStatus.CANCELLED
        }:
            return self._results[rid]
        if self._executor is not None:
            raw = self._executor.execute(request)
            result = self._normalize(raw, rid)
        else:
            result = WorkResult(rid, WorkStatus.COMPLETED, task_id="t-stub", agent_id="a-stub",
                                output={"echo": request.description})
        self._results[rid] = result
        return result

    def submit_async(self, request: WorkRequest, on_complete: Optional[Callable]=None) -> WorkResult:
        result = self.submit(request)
        if on_complete:
            on_complete(result)
        return result

    def status(self, request_id: str) -> WorkResult:
        rid = str(request_id)
        if rid in self._results:
            return self._results[rid]
        return WorkResult(rid, WorkStatus.REJECTED, error="unknown_request_id")

    def evidence(self, request_id: str):
        if self._executor is not None and hasattr(self._executor, "evidence"):
            return self._executor.evidence(request_id)
        rid = str(request_id)
        r = self._results.get(rid)
        if r is None:
            return None
        terminal = r.status in {WorkStatus.COMPLETED, WorkStatus.FAILED, WorkStatus.REJECTED, WorkStatus.CANCELLED}
        return type("E", (), {
            "request_id": rid,
            "handler_started": True,
            "terminal": terminal,
            "status": r.status.value,
            "task_id": r.task_id,
            "agent_id": r.agent_id,
            "output": r.output,
            "error": r.error,
        })()

    def invocation_count(self, request_id: str) -> int:
        return self._invoke_count.get(str(request_id), 0)

    @staticmethod
    def _normalize(raw, rid: str) -> WorkResult:
        try:
            status = WorkStatus(getattr(raw, "status"))
        except (ValueError, TypeError):
            status = WorkStatus.FAILED
        return WorkResult(
            rid, status,
            getattr(raw, "task_id", None),
            getattr(raw, "agent_id", None),
            getattr(raw, "output", None),
            getattr(raw, "error", None),
        )
