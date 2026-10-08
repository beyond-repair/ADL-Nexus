"""Digital Workforce role definitions + supervised task board.

Claim-capped: routing under explicit assign/complete. Not autonomy.
assign checks the declared role contract: an unknown role, or a capability
that is not in that role's contract, is rejected and does not create a task.
complete only flips a pending or assigned task to complete. Execution is not
implemented: complete does not run code, call a model, or pretend the role
did the work.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any, List


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

# complete may only move these statuses. It never executes the capability.
_COMPLETABLE = frozenset({"pending", "assigned"})


def get_role(name: str) -> Role | None:
    return ROLES.get(name.lower())


def list_roles() -> list[str]:
    return list(ROLES.keys())


@dataclass
class Task:
    id: str
    role: str
    goal: str
    capability: str | None = None
    status: str = "pending"
    created_at: float = field(default_factory=time.time)
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "role": self.role,
            "capability": self.capability,
            "goal": self.goal,
            "status": self.status,
            "created_at": self.created_at,
            "note": self.note,
            "claim": "supervised routing only; execution not implemented",
        }


_BOARD: dict[str, Task] = {}


def assign(role: str, goal: str, capability: str | None = None, note: str = "") -> dict[str, Any]:
    """Record a task when the role contract allows it. Does not execute it."""
    r = get_role(role)
    if r is None:
        return {"ok": False, "error": f"unknown role: {role}"}
    if capability is not None and capability not in r.capabilities:
        return {
            "ok": False,
            "error": f"capability {capability!r} is not in {role.lower()} contract",
        }
    task = Task(
        id=uuid.uuid4().hex[:10],
        role=role.lower(),
        goal=goal,
        capability=capability,
        note=note,
    )
    _BOARD[task.id] = task
    return {"ok": True, "task": task.to_dict()}


def list_tasks(status: str | None = None) -> dict[str, Any]:
    items = [t.to_dict() for t in _BOARD.values()]
    if status:
        items = [t for t in items if t["status"] == status]
    return {"ok": True, "tasks": items, "count": len(items)}


def get_task(task_id: str) -> dict[str, Any]:
    """Return the stored task record. Does not run the role."""
    task = _BOARD.get(task_id)
    if task is None:
        return {"ok": False, "error": f"unknown task: {task_id}"}
    return {"ok": True, "task": task.to_dict()}


def complete(task_id: str, note: str = "") -> dict[str, Any]:
    """Flip pending/assigned to complete. Does not run code or call a model."""
    task = _BOARD.get(task_id)
    if task is None:
        return {"ok": False, "error": f"unknown task: {task_id}"}
    if task.status not in _COMPLETABLE:
        return {
            "ok": False,
            "error": (
                f"task {task_id} is {task.status}; "
                "complete only accepts pending or assigned"
            ),
        }
    task.status = "complete"
    if note:
        task.note = note
    return {"ok": True, "task": task.to_dict()}
