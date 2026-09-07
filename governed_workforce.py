"""Nexus-owned governance/security/durable-identity boundary for Workforce."""
from __future__ import annotations
from typing import Any, Callable, Optional
import threading

from adapters.workforce.contract import WorkRequest, WorkResult, WorkStatus
from persistence import (
    DurableExecutionStore,
    ExecutionState,
    ExecutionRecoveryWorker,
)

try:
    from layer0_governance.registry import evaluate_request, record_audit, register_subsystem
except Exception:  # pragma: no cover
    def evaluate_request(subsystem, action, context=None):
        class D:
            allowed = True
            reason = "allow-default"
            claim_level = 2
            audit_id = "gov-default"
        return D()
    def record_audit(event, **payload):
        return "audit-default"
    def register_subsystem(*a, **k):
        return "reg"

try:
    from layer5_security.gate import SecurityGate
except Exception:  # pragma: no cover
    class SecurityGate:
        def evaluate(self, subsystem, action, context=None):
            class D:
                allowed = True
                trust_score = 0.95
                reason = "allow-default"
                audit_id = "sec-default"
                policy_match = "allow"
            return D()


class GovernedWorkforce:
    """Nexus coordinates; Workforce executes. No Agent/Task ownership here."""

    def __init__(self, adapter, security=None, store=None):
        self.adapter = adapter
        self.security = security or SecurityGate()
        self.store = store or DurableExecutionStore()
        self._callback_lock = threading.Lock()
        try:
            register_subsystem("workforce", layer=3, claim_level=2, capabilities=["execute_work"])
        except Exception:
            pass

    def submit(self, request: WorkRequest, asynchronous: bool = False) -> WorkResult:
        if asynchronous:
            return self.submit_async(request)
        return self._submit_sync(request)

    def submit_async(self, request: WorkRequest) -> WorkResult:
        """Non-blocking accept; Workforce owns async execution."""
        rid = str(request.request_id)
        existing = self.store.get(rid)
        if existing is not None:
            return self._result_from_record(existing)

        g = evaluate_request("workforce", "execute_work", {"request_id": rid})
        s = self.security.evaluate("workforce", "execute_work", {"request_id": rid})
        if not g.allowed or not s.allowed:
            self.store.begin(rid, g.audit_id, s.audit_id)
            self.store.finalize(
                rid, ExecutionState.REJECTED,
                error=f"governance={g.reason}; security={s.reason}",
            )
            record_audit("workforce_denied", request_id=rid)
            return WorkResult(rid, WorkStatus.REJECTED,
                              error=f"governance={g.reason}; security={s.reason}")

        record = self.store.begin(rid, g.audit_id, s.audit_id)
        if record.state is not ExecutionState.ACCEPTED:
            return self._result_from_record(record)

        self.store.mark_running(rid)
        record_audit("workforce_route_async", request_id=rid)

        if hasattr(self.adapter, "submit_async"):
            self.adapter.submit_async(request, on_complete=self._on_complete)
        else:
            def _run():
                try:
                    result = self.adapter.submit(request)
                    self._on_complete(result)
                except Exception as exc:
                    self._on_complete(WorkResult(rid, WorkStatus.FAILED, error=str(exc)))
            threading.Thread(target=_run, daemon=True).start()

        return WorkResult(rid, WorkStatus.RUNNING)

    def _submit_sync(self, request: WorkRequest) -> WorkResult:
        rid = str(request.request_id)
        existing = self.store.get(rid)
        if existing is not None:
            return self._result_from_record(existing)

        g = evaluate_request("workforce", "execute_work", {"request_id": rid})
        s = self.security.evaluate("workforce", "execute_work", {"request_id": rid})
        if not g.allowed or not s.allowed:
            self.store.begin(rid, g.audit_id, s.audit_id)
            self.store.finalize(
                rid, ExecutionState.REJECTED,
                error=f"governance={g.reason}; security={s.reason}",
            )
            record_audit("workforce_denied", request_id=rid)
            return WorkResult(rid, WorkStatus.REJECTED,
                              error=f"governance={g.reason}; security={s.reason}")

        record = self.store.begin(rid, g.audit_id, s.audit_id)
        if record.state is not ExecutionState.ACCEPTED:
            return self._result_from_record(record)

        self.store.mark_running(rid)
        record_audit("workforce_route", request_id=rid)

        result = self.adapter.submit(request)
        final_state = ExecutionState(result.status.value)
        self.store.finalize(
            rid, final_state,
            task_id=result.task_id, agent_id=result.agent_id,
            result=result.output, error=result.error,
        )
        record_audit("workforce_result", request_id=rid, status=result.status.value)
        return result

    def _on_complete(self, result: WorkResult) -> None:
        """Completion callback. Terminal/indeterminate states are authoritative."""
        with self._callback_lock:
            rid = str(result.request_id)
            existing = self.store.get(rid)
            if existing is None:
                return
            if existing.state in {
                ExecutionState.COMPLETED, ExecutionState.FAILED,
                ExecutionState.REJECTED, ExecutionState.CANCELLED,
                ExecutionState.INDETERMINATE,
            }:
                record_audit("workforce_late_callback_ignored", request_id=rid,
                             existing=existing.state.value)
                return
            try:
                state = ExecutionState(result.status.value)
            except ValueError:
                state = ExecutionState.FAILED
            self.store.finalize(
                rid, state,
                task_id=result.task_id, agent_id=result.agent_id,
                result=result.output, error=result.error,
            )
            record_audit("workforce_result", request_id=rid, status=result.status.value)

    def recover(self):
        return ExecutionRecoveryWorker(self.store, self.adapter).recover_all()

    def complete_callback(self, result: WorkResult) -> None:
        self._on_complete(result)

    @staticmethod
    def _result_from_record(record) -> WorkResult:
        if record.state in {ExecutionState.ACCEPTED, ExecutionState.RUNNING, ExecutionState.RECOVERING}:
            status = WorkStatus.ACCEPTED if record.state is ExecutionState.ACCEPTED else WorkStatus.RUNNING
        elif record.state is ExecutionState.INDETERMINATE:
            status = WorkStatus.FAILED
        else:
            status = WorkStatus(record.state.value)
        return WorkResult(
            record.request_id, status,
            record.workforce_task_id, record.workforce_agent_id,
            record.result, record.error,
        )
