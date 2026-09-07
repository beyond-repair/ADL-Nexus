"""
NEX-INT-002 — Thin Nexus-side Workforce Adapter

Hard rules enforced:
1. Import only the public contract.
2. Do not import Agent, Task, or Orchestrator.
3. No persistence.
4. No LLM.
5. No scheduling logic.
6. No governance/security evaluation.
7. Normalize adapter failures into WorkResult.
8. Preserve request_id across the entire call.
9. Adapter is replaceable.
10. Deterministic unit-test surface.
"""

from __future__ import annotations

from typing import Dict
from .contract import (
    WorkRequest,
    WorkResult,
    WorkStatus,
)


class InProcessWorkforceAdapter:
    """
    In-process, memory-only adapter.

    For NEX-INT-002 this is a deliberate stub/backend that:
    - Accepts WorkRequests
    - Tracks them by request_id
    - Can be later replaced by a real Digital Workforce service
      that implements the same interface.

    It does NOT execute real agent work. That is NEX-INT-003.
    """

    def __init__(self, executor=None) -> None:
        self._executor = executor
        self._results: Dict[str, WorkResult] = {}

    def submit(self, request: WorkRequest) -> WorkResult:
        if not isinstance(request, WorkRequest):
            return WorkResult(
                request_id=getattr(request, "request_id", "unknown"),
                status=WorkStatus.REJECTED,
                error="malformed_request: expected WorkRequest",
            )

        if not request.request_id:
            return WorkResult(
                request_id="",
                status=WorkStatus.REJECTED,
                error="malformed_request: missing request_id",
            )

        if request.request_id in self._results:
            return self._results[request.request_id]

        if self._executor is not None:
            raw = self._executor.execute(request)
            result = self._normalize(raw, request.request_id)
            self._results[request.request_id] = result
            return result

        # Pure stub path (no executor injected)
        result = WorkResult(
            request_id=request.request_id,
            status=WorkStatus.ACCEPTED,
        )
        self._results[request.request_id] = result
        return result

    def status(self, request_id: str) -> WorkResult:
        if not request_id:
            return WorkResult(
                request_id="",
                status=WorkStatus.REJECTED,
                error="malformed_request: empty request_id",
            )
        if request_id in self._results:
            return self._results[request_id]
        if self._executor is not None:
            raw = self._executor.status(request_id)
            if raw is not None:
                return self._normalize(raw, request_id)
        return WorkResult(
            request_id=request_id,
            status=WorkStatus.REJECTED,
            error="unknown_request_id",
        )

    def cancel(self, request_id: str) -> WorkResult:
        if not request_id:
            return WorkResult(
                request_id="",
                status=WorkStatus.REJECTED,
                error="malformed_request: empty request_id",
            )
        existing = self._results.get(request_id)
        if existing is not None and existing.status in {
            WorkStatus.COMPLETED,
            WorkStatus.FAILED,
            WorkStatus.REJECTED,
            WorkStatus.CANCELLED,
        }:
            return existing
        if self._executor is not None:
            raw = self._executor.cancel(request_id)
            result = self._normalize(raw, request_id)
            self._results[request_id] = result
            return result
        result = WorkResult(
            request_id=request_id,
            status=WorkStatus.CANCELLED,
        )
        self._results[request_id] = result
        return result

    def evidence(self, request_id: str):
        if self._executor is None:
            return None
        evidence_fn = getattr(self._executor, "evidence", None)
        return evidence_fn(request_id) if evidence_fn else None

    @staticmethod
    def _normalize(raw, rid: str) -> WorkResult:
        try:
            status = WorkStatus(getattr(raw, "status"))
        except (ValueError, TypeError):
            status = WorkStatus.FAILED
        return WorkResult(
            request_id=rid,
            status=status,
            task_id=getattr(raw, "task_id", None),
            agent_id=getattr(raw, "agent_id", None),
            output=getattr(raw, "output", None),
            error=getattr(raw, "error", None),
        )


def create_workforce_adapter(executor=None) -> InProcessWorkforceAdapter:
    return InProcessWorkforceAdapter(executor=executor)
