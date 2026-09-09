"""Digital Workforce: supervised assign → execute → provenance → complete.

Claim-capped: not autonomy. NEX-INT-001.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass
from typing import Any, List

from adapters.sunder.bridge import SunderAdapter
from layer6_simulation.reality import RealityEngine

from .claims import evaluate_claim
from .prov import hash_payload, read_record, write_record
from .store import load_tasks, save_tasks


@dataclass(frozen=True)
class Role:
    name: str
    capabilities: List[str]
    layer: int = 3
    claim_level: int = 1


ROLES = {
    "engineer": Role("Engineer", capabilities=["code", "refactor", "test", "document"]),
    "researcher": Role("Researcher", capabilities=["hypothesis", "experiment", "evidence", "replicate"]),
    "writer": Role("Writer", capabilities=["draft", "edit", "summarize"]),
    "analyst": Role("Analyst", capabilities=["analyze", "metric", "report"]),
    "tester": Role("Tester", capabilities=["test", "benchmark", "fuzz"]),
    "operator": Role("Operator", capabilities=["deploy", "monitor", "recover"]),
    "manager": Role("Manager", capabilities=["prioritize", "assign", "review"]),
}

EXECUTABLE_ROLES = frozenset({"engineer", "tester", "analyst"})


def get_role(name: str) -> Role | None:
    return ROLES.get(name.lower())


def list_roles() -> list[str]:
    return list(ROLES.keys())


def _task_dict(task: dict[str, Any]) -> dict[str, Any]:
    out = dict(task)
    out.setdefault("claim", "supervised routing only")
    return out


def assign(role: str, goal: str, note: str = "") -> dict[str, Any]:
    """Manager-supervised assignment. Does not execute the role."""
    r = get_role(role)
    if r is None:
        return {"ok": False, "error": f"unknown role: {role}"}
    tasks = load_tasks()
    task_id = uuid.uuid4().hex[:10]
    task = {
        "id": task_id,
        "role": role.lower(),
        "goal": goal,
        "status": "pending",
        "created_at": time.time(),
        "note": note,
        "claim": "supervised routing only",
    }
    tasks[task_id] = task
    save_tasks(tasks)
    return {"ok": True, "task": _task_dict(task)}


def list_tasks(status: str | None = None) -> dict[str, Any]:
    tasks = load_tasks()
    items = [_task_dict(t) for t in tasks.values()]
    if status:
        items = [t for t in items if t.get("status") == status]
    return {"ok": True, "tasks": items, "count": len(items)}


def get_task(task_id: str) -> dict[str, Any]:
    tasks = load_tasks()
    task = tasks.get(task_id)
    if task is None:
        return {"ok": False, "error": f"unknown task: {task_id}"}
    return {"ok": True, "task": _task_dict(task)}


def execute(task_id: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
    """Invoke sunder after claim/reality check. Writes provenance. Never silent-completes."""
    context = dict(context or {})
    tasks = load_tasks()
    task = tasks.get(task_id)
    if task is None:
        return {"ok": False, "result": "FAILED", "error": f"unknown task: {task_id}"}

    started_at = time.time()
    goal = str(task.get("goal", ""))
    role = str(task.get("role", "engineer"))

    gate = evaluate_claim(goal, context)
    reality = RealityEngine().state(goal, context)

    def _finish(result: str, output: Any, reason: str, adapter: SunderAdapter | None = None) -> dict[str, Any]:
        mode = adapter.status.mode if adapter is not None else "none"
        record = {
            "task_id": task_id,
            "role": role,
            "adapter": "sunder" if adapter is not None else "none",
            "adapter_mode": mode,
            "input_hash": hash_payload({"goal": goal, "context": context, "role": role}),
            "output_hash": hash_payload(output),
            "started_at": started_at,
            "completed_at": time.time(),
            "result": result,
            "reason": reason,
            "reality_claim": reality.get("claim"),
        }
        written = write_record(record)
        status = {"SUCCESS": "executed", "REFUSED": "refused", "FAILED": "failed"}[result]
        task["status"] = status
        task["note"] = reason
        tasks[task_id] = task
        save_tasks(tasks)
        return {
            "ok": result == "SUCCESS",
            "result": result,
            "reason": reason,
            "task": _task_dict(task),
            "provenance": written["record"],
            "provenance_path": written["path"],
            "gate": gate,
            "reality": {"claim": reality.get("claim"), "constraints": reality.get("constraints")},
            "adapter_output": output if adapter is not None else None,
        }

    if not gate["allowed"]:
        return _finish("REFUSED", {"gate": gate}, gate["reason"], adapter=None)

    if role not in EXECUTABLE_ROLES:
        return _finish("REFUSED", {"role": role}, f"role {role} is not executable via sunder", adapter=None)

    adapter = SunderAdapter()
    try:
        output = adapter.run_goal(goal, context)
    except Exception as exc:
        return _finish("FAILED", {"error": f"{type(exc).__name__}: {exc}"}, f"adapter exception: {exc}", adapter=adapter)

    if not isinstance(output, dict) or output.get("adapter") != "sunder":
        return _finish("FAILED", output, "sunder adapter did not return a sunder payload", adapter=adapter)

    return _finish("SUCCESS", output, "sunder invoked", adapter=adapter)


def complete(task_id: str, note: str = "") -> dict[str, Any]:
    """Mark complete only if SUCCESS provenance exists (I1)."""
    tasks = load_tasks()
    task = tasks.get(task_id)
    if task is None:
        return {"ok": False, "error": f"unknown task: {task_id}"}
    record = read_record(task_id)
    if record is None:
        return {"ok": False, "error": "complete refused: provenance missing"}
    if record.get("result") != "SUCCESS":
        return {
            "ok": False,
            "error": f"complete refused: provenance result is {record.get('result')}",
            "provenance": record,
        }
    task["status"] = "complete"
    if note:
        task["note"] = note
    tasks[task_id] = task
    save_tasks(tasks)
    return {"ok": True, "task": _task_dict(task), "provenance": record}


def run_goal(goal: str, context: dict[str, Any] | None = None, role: str = "engineer") -> dict[str, Any]:
    """Acceptance loop: assign → execute → complete-if-success."""
    context = context or {}
    assigned = assign(role, goal, note="nex-int-001 run_goal")
    if not assigned.get("ok"):
        return {"ok": False, "stage": "assign", **assigned}
    task_id = assigned["task"]["id"]
    executed = execute(task_id, context)
    if executed.get("result") != "SUCCESS":
        return {
            "ok": False,
            "stage": "execute",
            "assigned": assigned,
            "executed": executed,
        }
    done = complete(task_id, note="nex-int-001 auto-complete after SUCCESS")
    return {
        "ok": done.get("ok", False),
        "stage": "complete" if done.get("ok") else "complete_refused",
        "assigned": assigned,
        "executed": executed,
        "completed": done,
    }
