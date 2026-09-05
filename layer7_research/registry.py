"""Research Fabric — experiment / hypothesis / evidence registry (v0.3)."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import time
import hashlib

@dataclass
class Evidence:
    id: str
    kind: str  # note | metric | artifact | killgate
    content: str
    source: str
    created_at: float = field(default_factory=time.time)

@dataclass
class Experiment:
    id: str
    title: str
    hypothesis: str
    source_repo: str
    status: str  # open | running | passed | failed | superseded
    evidence: List[Evidence] = field(default_factory=list)
    claim_level: int = 1
    created_at: float = field(default_factory=time.time)

_EXPERIMENTS: dict[str, Experiment] = {}

def register_experiment(title: str, hypothesis: str, source_repo: str, claim_level: int = 1) -> str:
    payload = f"{title}:{hypothesis}:{source_repo}:{time.time()}"
    eid = hashlib.sha256(payload.encode()).hexdigest()[:12]
    exp = Experiment(id=eid, title=title, hypothesis=hypothesis, source_repo=source_repo, status="open", claim_level=claim_level)
    _EXPERIMENTS[eid] = exp
    return eid

def add_evidence(eid: str, kind: str, content: str, source: str = "manual") -> str | None:
    if eid not in _EXPERIMENTS:
        return None
    ev_id = hashlib.sha256(f"{eid}:{content}:{time.time()}".encode()).hexdigest()[:10]
    ev = Evidence(id=ev_id, kind=kind, content=content, source=source)
    _EXPERIMENTS[eid].evidence.append(ev)
    return ev_id

def set_status(eid: str, status: str) -> bool:
    if eid not in _EXPERIMENTS:
        return False
    _EXPERIMENTS[eid].status = status
    return True

def list_experiments() -> list[dict[str, Any]]:
    out = []
    for e in _EXPERIMENTS.values():
        d = e.__dict__.copy()
        d["evidence"] = [ev.__dict__ for ev in e.evidence]
        out.append(d)
    return out

def seed_cft_baseline():
    """Register the current CFT / Ware Constant baseline and attach known ledger evidence."""
    if _EXPERIMENTS:
        return  # already seeded

    e1 = register_experiment(
        "Ware Constant lock",
        "W_star = 1/(4\u03c0) under Option A is the correct phenomenological anchor",
        "ware-constant-phenomenology",
        claim_level=2,
    )
    add_evidence(e1, "note", "CONSISTENCY.md and Math.md lock W_star = 1/(4\u03c0); Option A demotes M2 to geometric factor", "CFTv3.3 ledger")
    add_evidence(e1, "metric", "Agreement with rounded 0.08 is ~0.53%", "WSTAR_ENTROPIC_DERIVATION.md")
    add_evidence(e1, "killgate", "killgate_verification.py Gate2 v_infty in SPARC range for Mb=1e11 under W_star=0.08", "killgate_verification.py")

    e2 = register_experiment(
        "Local SPARC residual",
        "Median \u03c7²_red can be driven to O(1) without breaking macro r0(Mb)",
        "ware-constant-phenomenology",
        claim_level=1,
    )
    add_evidence(e2, "metric", "Continuous scipy pass median \u03c7²_red ~9.1 (36% <5, 53% <10)", "SPARC_CHI2_REPORT.md")
    add_evidence(e2, "note", "Macro r0(Mb) never varied; W locked", "SPARC_CHI2_REPORT.md")
    add_evidence(e2, "artifact", "Re-run: python sparc_run.py --mode o1 && python killgate_verification.py (offline)", "ware-constant-phenomenology")

    e3 = register_experiment(
        "Bullet Cluster Model D",
        "Cluster collective scale \u03be can be derived from Proca Green function without free parameters",
        "ware-constant-phenomenology",
        claim_level=1,
    )
    add_evidence(e3, "note", "Simple r0/c FAIL; Model D (cluster \u03be) preferred because it preserves galactic lock", "bullet_alt_lag.py")
    add_evidence(e3, "killgate", "bullet_alt_lag.py: simple lag FAIL; Model D status OPEN", "bullet_alt_lag.py")

    e4 = register_experiment(
        "Lensing saturation \u03b4_sat",
        "\u03b4_sat can be derived from |A|^4 bulk coefficient rather than tuned to 1.2",
        "ware-constant-phenomenology",
        claim_level=1,
    )
    add_evidence(e4, "note", "Current \u03b4_sat=1.2 is explicit phenomenological parameter; \u03bb_A from bulk still OPEN", "delta_sat_from_A4.py")
    add_evidence(e4, "killgate", "killgate_verification.py Gate3 recovers ~2.2 via saturated formula with \u03b4_sat=1.2", "killgate_verification.py")
