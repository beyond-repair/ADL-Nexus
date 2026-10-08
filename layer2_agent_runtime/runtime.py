"""Minimal agent runtime loop (claim level 2).

Goal → plan → registered tools → recorded history.
Not a supervisor LLM. Tools are local and deterministic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from layer0_governance.registry import evaluate_request
from layer5_security.gate import SecurityGate

# Tool names checked inside execute. They are capabilities of coding-agent,
# not separate pathway actions. snap/sunder/spike/anchor are not tools here.
TOOL_ACTIONS = ("list_files", "summarize", "echo")


@dataclass
class StepResult:
    success: bool
    output: Any
    message: str = ""
    steps: list[str] = field(default_factory=list)


def _tool_list_files(goal: str, context: dict[str, Any]) -> Any:
    path = Path(context.get("path", "."))
    if not path.exists():
        return []
    return [str(p.relative_to(path)) for p in path.rglob("*") if p.is_file()][:80]


def _tool_summarize(goal: str, context: dict[str, Any]) -> Any:
    files = _tool_list_files(goal, context)
    by_ext: dict[str, int] = {}
    for f in files:
        ext = Path(f).suffix or "[none]"
        by_ext[ext] = by_ext.get(ext, 0) + 1
    return {"file_count": len(files), "by_extension": by_ext, "sample": files[:12], "goal": goal}


def _tool_echo(goal: str, context: dict[str, Any]) -> Any:
    return {"goal": goal, "context_keys": list(context.keys())}


class AgentRuntime:
    def __init__(self, name: str = "coding-agent"):
        self.name = name
        self.tools: dict[str, Callable] = {}
        self.history: list[dict[str, Any]] = []
        self.register_tool("list_files", _tool_list_files)
        self.register_tool("summarize", _tool_summarize)
        self.register_tool("echo", _tool_echo)

    def register_tool(self, name: str, fn: Callable) -> None:
        self.tools[name] = fn

    def list_tools(self) -> list[str]:
        return sorted(self.tools)

    def plan(self, goal: str) -> list[str]:
        text = (goal or "").lower()
        if "analyze" in text or "repo" in text:
            return ["list_files", "summarize"]
        return ["echo"]

    def execute(self, goal: str, context: dict[str, Any] | None = None) -> StepResult:
        """Run the plan. Each tool name is its own governance and security check.

        Fail-closed when coding-agent is not registered or the tool action
        is outside its capabilities. Does not catch tool bugs into a success.
        A tool exception fails the step and reports the exception type.
        """
        context = context or {}
        steps = self.plan(goal)
        results = []
        gate = SecurityGate(min_trust=0.5)
        for step in steps:
            gov = evaluate_request(self.name, step)
            if not gov.allowed:
                return StepResult(False, None, f"governance: {gov.reason}", steps=steps)
            sec = gate.evaluate(self.name, step)
            if not sec.allowed:
                return StepResult(False, None, f"security: {sec.reason}", steps=steps)
            if step not in self.tools:
                return StepResult(False, None, f"Tool '{step}' not registered", steps=steps)
            try:
                out = self.tools[step](goal, context)
            except Exception as e:
                return StepResult(False, None, f"{type(e).__name__}: {e}", steps=steps)
            results.append({"step": step, "output": out})
            self.history.append({"step": step, "output": out, "goal": goal})
        return StepResult(True, results, "ok", steps=steps)

    def plan_and_execute(self, goal: str, context: dict[str, Any] | None = None) -> StepResult:
        return self.execute(goal, context)

    def history_tail(self, n: int = 10) -> list[dict[str, Any]]:
        return list(self.history[-n:])
