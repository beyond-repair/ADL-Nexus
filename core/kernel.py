"""NexusKernel — assembles every layer and routes calls through governance + security.

Bootstrap (register_subsystem) is the only exception to call(). Mutating work
goes through call() or through think/authorize/commit, which check governance
before ObjectiveEngine runs. request and serve_loopback fail closed: this
process does not start a server.

There is no second dispatcher.
"""

from __future__ import annotations

from typing import Any

from layer0_governance.registry import (
    register_subsystem,
    evaluate_request,
    list_subsystems,
    get_audit_log,
)
from layer1_memory.store import MemoryStore
from layer2_agent_runtime.runtime import AgentRuntime, TOOL_ACTIONS
from layer3_workforce.roles import list_roles
from layer4_development.workspace import DevWorkspace
from layer5_security.gate import SecurityGate
from layer6_simulation.fabric import SimulationFabric
from layer7_research.registry import seed_cft_baseline, list_experiments
from layer8_economic.ledger import EconomicLedger
from adapters.sunder.bridge import SunderAdapter
from adapters.cleanroom.bridge import CleanRoomAdapter
from .objective import ObjectiveEngine
from .pathways import PATHWAY_SPEC, PathwayResult, _load_target, _resolve_callable, list_pathways, probe_packages
from .version import __version__

# claim_level is <= 2 except economic, which stays at 1 (not an elevation).
_SUBSYSTEM_META: dict[str, tuple[int, int]] = {
    "nexus-core": (0, 2),
    "memory-kernel": (1, 2),
    "coding-agent": (2, 2),
    "workforce": (3, 2),
    "development": (4, 2),
    "security-gate": (5, 2),
    "simulation": (6, 2),
    "research-fabric": (7, 2),
    "economic": (8, 1),
    "sunder-adapter": (2, 2),
    "cleanroom-adapter": (1, 2),
}

# Pathways whose target is the kernel's own instance, not a fresh object.
_BOUND_ATTR = {
    "memory": "memory",
    "runtime": "runtime",
    "development": "development",
    "security": "security",
    "simulation": "simulation",
    "economic": "economic",
    "sunder": "sunder",
    "cleanroom": "cleanroom",
}

_OBJECTIVE_ACTIONS = ["think", "authorize", "commit", "get_proposal"]


def _declared_capabilities(subsystem: str) -> list[str]:
    names: set[str] = set()
    for spec in PATHWAY_SPEC.values():
        if spec["subsystem"] == subsystem:
            names.update(spec.get("actions") or {})
    if subsystem == "coding-agent":
        names.update(TOOL_ACTIONS)
    return sorted(names)


class NexusKernel:
    """One object that can call every packaged module by pathway name."""

    def __init__(self) -> None:
        self.memory = MemoryStore()
        self.security = SecurityGate(min_trust=0.5)
        self.runtime = AgentRuntime("coding-agent")
        self.development = DevWorkspace()
        self.simulation = SimulationFabric()
        self.economic = EconomicLedger()
        self.sunder = SunderAdapter()
        self.cleanroom = CleanRoomAdapter(dim=1024)
        self.objective = ObjectiveEngine()
        self._targets: dict[str, Any] = {}
        self._bootstrapped = False

    def bootstrap(self) -> "NexusKernel":
        """Register subsystems once. This is the documented bootstrap exception.

        Registration is not a second command dispatcher. seed_cft_baseline runs
        here because it is lab content loaded at startup, not a product action.
        """
        if self._bootstrapped:
            return self
        seen: set[str] = set()
        for spec in PATHWAY_SPEC.values():
            name = spec["subsystem"]
            if name in seen:
                continue
            seen.add(name)
            layer, claim = _SUBSYSTEM_META[name]
            register_subsystem(
                name, layer=layer, claim_level=claim,
                capabilities=_declared_capabilities(name),
            )
        register_subsystem(
            "objective", layer=0, claim_level=2, capabilities=list(_OBJECTIVE_ACTIONS),
        )
        seed_cft_baseline()
        self._bootstrapped = True
        return self

    def _target_for(self, pathway: str, spec: dict[str, Any]) -> Any:
        attr = _BOUND_ATTR.get(pathway)
        if attr:
            return getattr(self, attr)
        if pathway not in self._targets:
            self._targets[pathway] = _load_target(spec)
        return self._targets[pathway]

    def call(self, pathway: str, action: str, *args: Any, **kwargs: Any) -> PathwayResult:
        self.bootstrap()
        if pathway not in PATHWAY_SPEC:
            return PathwayResult(False, pathway, action, False, reason=f"unknown pathway: {pathway}")
        spec = PATHWAY_SPEC[pathway]
        declared = spec.get("actions") or {}
        if action not in declared:
            return PathwayResult(
                False, pathway, action, False,
                reason=f"governance: action {action!r} is not declared on pathway {pathway}",
            )
        subsystem = spec["subsystem"]
        gov = evaluate_request(subsystem, action)
        sec = self.security.evaluate(subsystem, action)
        if not gov.allowed:
            return PathwayResult(False, pathway, action, False, reason=f"governance: {gov.reason}")
        if not sec.allowed:
            return PathwayResult(False, pathway, action, False, reason=f"security: {sec.reason}")
        try:
            fn = _resolve_callable(self._target_for(pathway, spec), spec, action)
            result = fn(*args, **kwargs)
            return PathwayResult(True, pathway, action, True, result=result)
        except Exception as exc:
            # Dispatcher boundary: the error is returned, not turned into ok=True.
            return PathwayResult(False, pathway, action, True, reason=f"{type(exc).__name__}: {exc}")

    def _objective_gate(self, action: str) -> dict[str, Any] | None:
        self.bootstrap()
        if action not in _OBJECTIVE_ACTIONS:
            return {"ok": False, "error": f"governance: action {action!r} is not an objective action"}
        gov = evaluate_request("objective", action)
        if not gov.allowed:
            return {"ok": False, "error": f"governance: {gov.reason}"}
        sec = self.security.evaluate("objective", action)
        if not sec.allowed:
            return {"ok": False, "error": f"security: {sec.reason}"}
        return None

    def think(self, goal: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        denied = self._objective_gate("think")
        if denied:
            return denied
        return self.objective.think(goal, context)

    def authorize(self, proposal_id: str, actor: str = "operator") -> dict[str, Any]:
        denied = self._objective_gate("authorize")
        if denied:
            return denied
        return self.objective.authorize(proposal_id, actor=actor)

    def commit(self, proposal_id: str) -> dict[str, Any]:
        """Governed commit. Refuses when unauthorized. Does not execute role work."""
        denied = self._objective_gate("commit")
        if denied:
            return denied
        return self.objective.commit(proposal_id)

    def get_proposal(self, proposal_id: str) -> dict[str, Any]:
        denied = self._objective_gate("get_proposal")
        if denied:
            return denied
        return self.objective.get_proposal(proposal_id)

    def _unavailable(self, name: str) -> dict[str, Any]:
        return {
            "ok": False,
            "fail_closed": True,
            "error": f"unavailable: NexusKernel.{name} is not implemented",
        }

    def request(self, *_args: Any, **_kwargs: Any) -> dict[str, Any]:
        """Fail closed. No request loop and no server are implemented."""
        self.bootstrap()
        return self._unavailable("request")

    def serve_loopback(self, *_args: Any, **_kwargs: Any) -> dict[str, Any]:
        """Fail closed. Does not bind a socket."""
        self.bootstrap()
        out = self._unavailable("serve_loopback")
        out["bound"] = False
        return out

    def status(self) -> dict[str, Any]:
        self.bootstrap()
        packages = probe_packages()
        return {
            "version": __version__,
            "lifecycle": "RESEARCH",
            "subsystems": list(list_subsystems().keys()),
            "pathways": list_pathways(),
            "packages_ok": all(p["import_ok"] for p in packages),
            "package_probe": packages,
            "workforce_roles": list_roles(),
            "memory_keys": self.memory.keys(),
            "experiments": len(list_experiments()),
            "sunder": self.sunder.status.__dict__,
            "cleanroom": self.cleanroom.status.__dict__,
            "audit_len": len(get_audit_log()),
            "claim_cap": 2,
            "adl_governance": "external dependency; not imported",
        }

    def metrics(self) -> dict[str, Any]:
        self.bootstrap()
        result = self.call(
            "dashboard",
            "snapshot",
            subsystems=list_subsystems(),
            audit_len=len(get_audit_log()),
            security_log_len=len(self.security.get_log()),
            memory_keys=len(self.memory.keys()),
            experiments=len(list_experiments()),
            adapter_status={
                "sunder": self.sunder.status.__dict__,
                "cleanroom": self.cleanroom.status.__dict__,
            },
        )
        if not result.ok:
            return {"ok": False, "reason": result.reason}
        return result.result


_KERNEL: NexusKernel | None = None


def get_kernel() -> NexusKernel:
    global _KERNEL
    if _KERNEL is None:
        _KERNEL = NexusKernel().bootstrap()
    return _KERNEL
