"""Digital Workforce role definitions + supervised task board.

Claim-capped: routing under explicit assign/complete. Not autonomy.
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


def get_role(name: str) -> Role | None:
    return ROLES.get(name.lower())


def list_roles() -> list[str]:
    return list(ROLES.keys())


@dataclass
class Task:
    id: str
    role: str
    goal: str
    status: str = "pending"
    created_at: float = field(default_factory=time.time)
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "role": self.role,
            "goal": self.goal,
            "status": self.status,
            "created_at": self.created_at,
            "note": self.note,
            "claim": "supervised routing only",
        }


_BOARD: dict[str, Task] = {}


def assign(role: str, goal: str, note: str = "") -> dict[str, Any]:
    """Manager-supervised assignment. Does not execute the role."""
    r = get_role(role)
    if r is None:
        return {"ok": False, "error": f"unknown role: {role}"}
    task = Task(id=uuid.uuid4().hex[:10], role=role.lower(), goal=goal, note=note)
    _BOARD[task.id] = task
    return {"ok": True, "task": task.to_dict()}


def list_tasks(status: str | None = None) -> dict[str, Any]:
    items = [t.to_dict() for t in _BOARD.values()]
    if status:
        items = [t for t in items if t["status"] == status]
    return {"ok": True, "tasks": items, "count": len(items)}


def complete(task_id: str, note: str = "") -> dict[str, Any]:
    task = _BOARD.get(task_id)
    if task is None:
        return {"ok": False, "error": f"unknown task: {task_id}"}
    task.status = "complete"
    if note:
        task.note = note
    return {"ok": True, "task": task.to_dict()}
