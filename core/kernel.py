"""NexusKernel — assembles every layer and routes calls through governance + security."""

from __future__ import annotations

from typing import Any

from layer0_governance.registry import (
    register_subsystem,
    evaluate_request,
    list_subsystems,
    get_audit_log,
)
from layer1_memory.store import MemoryStore
from layer3_workforce.roles import list_roles
from layer4_development.workspace import DevWorkspace
from layer5_security.gate import SecurityGate
from layer6_simulation.fabric import SimulationFabric
from layer7_research.registry import seed_cft_baseline, list_experiments
from layer8_economic.ledger import EconomicLedger
from adapters.sunder.bridge import SunderAdapter
from adapters.cleanroom.bridge import CleanRoomAdapter
from dashboard.metrics import snapshot

from .pathways import PATHWAY_SPEC, PathwayResult, _load_target, _resolve_callable, list_pathways, probe_packages


class NexusKernel:
    """One object that can call every packaged module by pathway name."""

    def __init__(self) -> None:
        self.memory = MemoryStore()
        self.security = SecurityGate(min_trust=0.5)
        self.development = DevWorkspace()
        self.simulation = SimulationFabric()
        self.economic = EconomicLedger()
        self.sunder = SunderAdapter()
        self.cleanroom = CleanRoomAdapter(dim=1024)
        self._targets: dict[str, Any] = {}
        self._bootstrapped = False

    def bootstrap(self) -> "NexusKernel":
        if self._bootstrapped:
            return self
        register_subsystem(
            "nexus-core", layer=0, claim_level=2,
            capabilities=["status", "run", "audit", "memory", "registry", "roles",
                          "research", "adapters", "metrics", "integrity", "call", "packages",
                          "evaluate", "register", "list"],
        )
        register_subsystem("coding-agent", layer=2, claim_level=2,
                           capabilities=["list_files", "summarize", "echo"])
        register_subsystem("memory-kernel", layer=1, claim_level=2,
                           capabilities=["put", "get", "keys"])
        register_subsystem("workforce", layer=3, claim_level=2,
                           capabilities=["list", "get"])
        register_subsystem("development", layer=4, claim_level=2,
                           capabilities=["analyze", "list_entrypoints", "info"])
        register_subsystem("security-gate", layer=5, claim_level=2,
                           capabilities=["evaluate", "integrity", "file_hash", "tree_hash", "verify"])
        register_subsystem("simulation", layer=6, claim_level=2,
                           capabilities=["register", "list", "info"])
        register_subsystem("research-fabric", layer=7, claim_level=2,
                           capabilities=["register", "list", "evidence", "seed"])
        register_subsystem("economic", layer=8, claim_level=1,
                           capabilities=["record", "balance", "info"])
        register_subsystem("sunder-adapter", layer=2, claim_level=2,
                           capabilities=["scan", "run_goal", "capabilities"])
        register_subsystem("cleanroom-adapter", layer=1, claim_level=2,
                           capabilities=["put", "get", "info", "query"])
        seed_cft_baseline()
        self._bootstrapped = True
        return self

    def call(self, pathway: str, action: str, *args: Any, **kwargs: Any) -> PathwayResult:
        self.bootstrap()
        if pathway not in PATHWAY_SPEC:
            return PathwayResult(False, pathway, action, False, reason=f"unknown pathway: {pathway}")
        spec = PATHWAY_SPEC[pathway]
        subsystem = spec["subsystem"]
        gov = evaluate_request(subsystem, action)
        sec = self.security.evaluate(subsystem, action)
        if not gov.allowed:
            return PathwayResult(False, pathway, action, False, reason=f"governance: {gov.reason}")
        if not sec.allowed:
            return PathwayResult(False, pathway, action, False, reason=f"security: {sec.reason}")
        try:
            if pathway not in self._targets:
                self._targets[pathway] = _load_target(spec)
            fn = _resolve_callable(self._targets[pathway], spec, action)
            result = fn(*args, **kwargs)
            return PathwayResult(True, pathway, action, True, result=result)
        except Exception as exc:
            return PathwayResult(False, pathway, action, True, reason=f"{type(exc).__name__}: {exc}")

    def status(self) -> dict[str, Any]:
        self.bootstrap()
        packages = probe_packages()
        return {
            "version": "0.3.1",
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
        }

    def metrics(self) -> dict[str, Any]:
        self.bootstrap()
        return snapshot(
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


_KERNEL: NexusKernel | None = None


def get_kernel() -> NexusKernel:
    global _KERNEL
    if _KERNEL is None:
        _KERNEL = NexusKernel().bootstrap()
    return _KERNEL
