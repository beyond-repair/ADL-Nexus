"""Research Fabric — experiment / hypothesis registry (v0.2)."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import time
import hashlib
import json

@dataclass
class Experiment:
    id: str
    title: str
    hypothesis: str
    source_repo: str
    status: str  # open | running | passed | failed | superseded
    evidence: List[str] = field(default_factory=list)
    claim_level: int = 1
    created_at: float = field(default_factory=time.time)

_EXPERIMENTS: dict[str, Experiment] = {}

def register_experiment(title: str, hypothesis: str, source_repo: str, claim_level: int = 1) -> str:
    payload = f"{title}:{hypothesis}:{source_repo}:{time.time()}"
    eid = hashlib.sha256(payload.encode()).hexdigest()[:12]
    exp = Experiment(id=eid, title=title, hypothesis=hypothesis, source_repo=source_repo, status="open", claim_level=claim_level)
    _EXPERIMENTS[eid] = exp
    return eid

def add_evidence(eid: str, evidence: str) -> bool:
    if eid not in _EXPERIMENTS:
        return False
    _EXPERIMENTS[eid].evidence.append(evidence)
    return True

def set_status(eid: str, status: str) -> bool:
    if eid not in _EXPERIMENTS:
        return False
    _EXPERIMENTS[eid].status = status
    return True

def list_experiments() -> list[dict[str, Any]]:
    return [e.__dict__ for e in _EXPERIMENTS.values()]

def seed_cft_baseline():
    """Register the current CFT / Ware Constant baseline as research items."""
    register_experiment(
        "Ware Constant lock",
        "W_star = 1/(4\u03c0) under Option A is the correct phenomenological anchor",
        "ware-constant-phenomenology",
        claim_level=2,
    )
    register_experiment(
        "Local SPARC residual",
        "Median \u03c7²_red can be driven to O(1) without breaking macro r0(Mb)",
        "ware-constant-phenomenology",
        claim_level=1,
    )
    register_experiment(
        "Bullet Cluster Model D",
        "Cluster collective scale \u03be can be derived from Proca Green function without free parameters",
        "ware-constant-phenomenology",
        claim_level=1,
    )
