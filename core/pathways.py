"""Canonical module pathways for ADL Nexus.

Every named pathway maps to an importable package and a live object factory.
Callers go through governance + security so Layer 0 and Layer 5 stay on the path.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

PATHWAY_SPEC: dict[str, dict[str, Any]] = {
    "governance": {
        "package": "layer0_governance",
        "module": "layer0_governance.registry",
        "layer": 0,
        "subsystem": "nexus-core",
        "actions": {
            "evaluate": "evaluate_request",
            "register": "register_subsystem",
            "list": "list_subsystems",
            "audit": "get_audit_log",
        },
    },
    "memory": {
        "package": "layer1_memory",
        "module": "layer1_memory.store",
        "factory": "MemoryStore",
        "layer": 1,
        "subsystem": "memory-kernel",
        "actions": {"put": "put", "get": "get", "keys": "keys"},
    },
    "runtime": {
        "package": "layer2_agent_runtime",
        "module": "layer2_agent_runtime.runtime",
        "factory": "AgentRuntime",
        "factory_args": ("pathway-agent",),
        "layer": 2,
        "subsystem": "coding-agent",
        "actions": {},
    },
    "workforce": {
        "package": "layer3_workforce",
        "module": "layer3_workforce.roles",
        "layer": 3,
        "subsystem": "workforce",
        "actions": {
            "list": "list_roles",
            "get": "get_role",
            "assign": "assign",
            "execute": "execute",
            "complete": "complete",
            "run_goal": "run_goal",
            "list_tasks": "list_tasks",
        },
    },
    "development": {
        "package": "layer4_development",
        "module": "layer4_development.workspace",
        "factory": "DevWorkspace",
        "layer": 4,
        "subsystem": "development",
        "actions": {"analyze": "analyze", "list_entrypoints": "list_entrypoints", "info": "info"},
    },
    "security": {
        "package": "layer5_security",
        "module": "layer5_security.gate",
        "factory": "SecurityGate",
        "layer": 5,
        "subsystem": "security-gate",
        "actions": {"evaluate": "evaluate", "policy": "policy_snapshot", "log": "get_log"},
    },
    "integrity": {
        "package": "layer5_security",
        "module": "layer5_security.integrity",
        "layer": 5,
        "subsystem": "security-gate",
        "actions": {"file_hash": "file_hash", "tree_hash": "tree_hash", "verify": "verify_anchor"},
    },
    "simulation": {
        "package": "layer6_simulation",
        "module": "layer6_simulation.fabric",
        "factory": "SimulationFabric",
        "layer": 6,
        "subsystem": "simulation",
        "actions": {"register": "register", "list": "list", "info": "info"},
    },
    "research": {
        "package": "layer7_research",
        "module": "layer7_research.registry",
        "layer": 7,
        "subsystem": "research-fabric",
        "actions": {"seed": "seed_cft_baseline", "list": "list_experiments", "evidence": "add_evidence"},
    },
    "economic": {
        "package": "layer8_economic",
        "module": "layer8_economic.ledger",
        "factory": "EconomicLedger",
        "layer": 8,
        "subsystem": "economic",
        "actions": {"record": "record", "balance": "balance", "info": "info"},
    },
    "sunder": {
        "package": "adapters.sunder",
        "module": "adapters.sunder.bridge",
        "factory": "SunderAdapter",
        "layer": 2,
        "subsystem": "sunder-adapter",
        "actions": {"run_goal": "run_goal", "capabilities": "capabilities"},
    },
    "cleanroom": {
        "package": "adapters.cleanroom",
        "module": "adapters.cleanroom.bridge",
        "factory": "CleanRoomAdapter",
        "layer": 1,
        "subsystem": "cleanroom-adapter",
        "actions": {"put": "put", "get": "get", "info": "info"},
    },
    "dashboard": {
        "package": "dashboard",
        "module": "dashboard.metrics",
        "layer": 0,
        "subsystem": "nexus-core",
        "actions": {"snapshot": "snapshot"},
    },
    "registry": {
        "package": "registry",
        "module": "registry.loader",
        "layer": 0,
        "subsystem": "nexus-core",
        "actions": {"load": "load_manifests", "list": "list_manifests"},
    },
    "analysis": {
        "package": "analysis",
        "module": "analysis.repo",
        "layer": 4,
        "subsystem": "development",
        "actions": {"analyze_tree": "analyze_tree"},
    },
}


@dataclass
class PathwayResult:
    ok: bool
    pathway: str
    action: str
    allowed: bool
    result: Any = None
    reason: str = ""


def list_pathways() -> list[str]:
    return sorted(PATHWAY_SPEC)


def describe(name: str) -> dict[str, Any]:
    spec = PATHWAY_SPEC[name]
    return {
        "name": name,
        "package": spec["package"],
        "module": spec["module"],
        "layer": spec["layer"],
        "subsystem": spec["subsystem"],
        "actions": list(spec.get("actions", {})),
        "factory": spec.get("factory"),
    }


def _load_target(spec: dict[str, Any]) -> Any:
    import importlib

    mod = importlib.import_module(spec["module"])
    if spec.get("factory"):
        factory: Callable = getattr(mod, spec["factory"])
        args = spec.get("factory_args", ())
        return factory(*args)
    return mod


def _resolve_callable(target: Any, spec: dict[str, Any], action: str) -> Callable:
    mapped = spec.get("actions", {}).get(action, action)
    fn = getattr(target, mapped, None)
    if fn is None:
        raise AttributeError(f"action {action!r} not on {spec['module']}")
    return fn


def probe_packages() -> list[dict[str, Any]]:
    """Import every packaged module and report whether the pathway is live."""
    import importlib

    rows = []
    for name, spec in PATHWAY_SPEC.items():
        row: dict[str, Any] = {
            "pathway": name,
            "package": spec["package"],
            "module": spec["module"],
            "layer": spec["layer"],
            "import_ok": False,
            "error": "",
        }
        try:
            importlib.import_module(spec["package"])
            importlib.import_module(spec["module"])
            row["import_ok"] = True
        except Exception as exc:
            row["error"] = f"{type(exc).__name__}: {exc}"
        rows.append(row)
    return rows
