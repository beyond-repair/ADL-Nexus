# ADL Nexus

**Local-first autonomous engineering, governance, simulation, and workforce platform.**

**Version:** 0.3.0-alpha (Hardened Runtime foundation)  
**Owner:** beyond-repair / Atomic Dream Labs  
**Governance:** [ADL-Governance](https://github.com/beyond-repair/ADL-Governance) + [ADL-SEEM](https://github.com/beyond-repair/ADL-SEEM)

> The objective is not to create another repository.  
> The objective is to transform Atomic Dream Labs from a collection of projects into a single evidence-producing operating system for autonomous engineering and research.

---

## Design Principle (Immutable)

**The highest-leverage move is not to merge every repository into one giant application.**

The strongest synthesis is a **layered architecture** where each major body of work becomes a subsystem, plugin, benchmark, research package, or archived historical artifact.

---

## Current Status — v0.3.0-alpha

| Layer | Name | Status |
|-------|------|--------|
| 0 | Governance Kernel | **Active** |
| 1 | Memory Kernel | **Active** + clean-room adapter |
| 2 | Agent Runtime | **Active** + sunder adapter |
| 3 | Digital Workforce | Scaffolded (roles defined) |
| 4 | Development Environment | Scaffolded |
| 5 | Security Fabric | **Active** (minimal gate) |
| 6 | Simulation Fabric | Scaffolded |
| 7 | Research Fabric | **Active** + CFT evidence hooks |
| 8 | Economic Layer | Scaffolded |

### What is new in 0.3.0-alpha
- `adapters/sunder` — claim-capped bridge to the sunder coding agent
- `adapters/cleanroom` — claim-capped bridge toward sovereign-clean-room VSA memory
- Research Fabric can attach evidence records to experiments
- Stronger subsystem manifests and portfolio map
- Core CLI expanded (`adapters`, richer `research`)

**Still honest:** Full deep VSA runtime interop and production VigilE.S.A. policy engine are not yet claimed.

---

## Quick Start

```bash
git clone https://github.com/beyond-repair/ADL-Nexus.git
cd ADL-Nexus

python -m core.nexus status
python -m core.nexus run --goal "analyze repository"
python -m core.nexus research
python -m core.nexus adapters
python -m core.nexus audit
```

---

## Unified Workflow

```
User Request
     ↓
Governance (L0)
     ↓
Memory (L1) ± clean-room adapter
     ↓
Agent Runtime (L2) ± sunder adapter
     ↓
Workforce routing (L3)
     ↓
Execution
     ↓
Security Validation (L5)
     ↓
Measurement + Research evidence
     ↓
Memory Update
```

---

*Built under ADL-SEEM v3.0. Truth over Agreement. Verification over Plausibility. Governance first.*
