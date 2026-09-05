"""Digital Workforce role definitions (v0.2)."""

from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Role:
    name: str
    layer: int = 3
    capabilities: List[str]
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
