"""Minimal agent runtime loop."""

from __future__ import annotations
from typing import Any, Callable
from dataclasses import dataclass, field

@dataclass
class StepResult:
    success: bool
    output: Any
    message: str = ""

class AgentRuntime:
    def __init__(self, name: str = "coding-agent"):
        self.name = name
        self.tools: dict[str, Callable] = {}
        self.history: list[dict[str, Any]] = []

    def register_tool(self, name: str, fn: Callable) -> None:
        self.tools[name] = fn

    def plan(self, goal: str) -> list[str]:
        """Extremely simple planner for v0.1."""
        if "analyze" in goal.lower() or "repo" in goal.lower():
            return ["list_files", "summarize"]
        return ["echo"]

    def execute(self, goal: str, context: dict[str, Any] | None = None) -> StepResult:
        context = context or {}
        steps = self.plan(goal)
        results = []
        for step in steps:
            if step not in self.tools:
                return StepResult(False, None, f"Tool '{step}' not registered")
            try:
                out = self.tools[step](goal, context)
                results.append(out)
                self.history.append({"step": step, "output": out})
            except Exception as e:
                return StepResult(False, None, str(e))
        return StepResult(True, results, "ok")
