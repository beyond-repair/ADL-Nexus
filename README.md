# ADL Nexus

**Local-first autonomous engineering, governance, simulation, and workforce platform.**

**Version:** 0.2.0 (Architecture Complete)  
**Owner:** beyond-repair / Atomic Dream Labs  
**Governance:** [ADL-Governance](https://github.com/beyond-repair/ADL-Governance) + [ADL-SEEM](https://github.com/beyond-repair/ADL-SEEM)

> The objective is not to create another repository.  
> The objective is to transform Atomic Dream Labs from a collection of projects into a single evidence-producing operating system for autonomous engineering and research.

---

## Design Principle (Immutable)

**The highest-leverage move is not to merge every repository into one giant application.**

That would create an unmaintainable system.

The strongest synthesis is a **layered architecture** where each major body of work becomes a subsystem, plugin, benchmark, research package, or archived historical artifact.

---

## Layered Architecture (Complete)

```
Layer 0 — Governance Kernel
Layer 1 — Memory Kernel
Layer 2 — Agent Runtime
Layer 3 — Digital Workforce
Layer 4 — Development Environment
Layer 5 — Security Fabric
Layer 6 — Simulation Fabric
Layer 7 — Research Fabric
Layer 8 — Economic Layer
```

| Layer | Name | Primary Sources | Status |
|-------|------|-----------------|--------|
| 0 | Governance Kernel | ADL-Governance, forge-aegis, Portfolio Census | **Active** |
| 1 | Memory Kernel | sovereign-clean-room, SEEM, VSA/FHRR/BaNEL | **Active** |
| 2 | Agent Runtime | sunder, Auto_Legion, seem-sunder-bridge | **Active** |
| 3 | Digital Workforce | LegionOS, Digital Double concepts | Scaffolded |
| 4 | Development Environment | analysis tools, future RepoRover | Scaffolded |
| 5 | Security Fabric | VigilE.S.A., forge-aegis | **Active (minimal)** |
| 6 | Simulation Fabric | blacksite, Cold Boot / Godot systems | Scaffolded |
| 7 | Research Fabric | coherence-drive, CFT, Ware Constant repos | **Active (registry)** |
| 8 | Economic Layer | FortiTrade lessons | Scaffolded |

---

## Unified Workflow (Executable)

```
User Request
     ↓
Governance          (Layer 0) — evaluate + audit
     ↓
Memory              (Layer 1) — retrieve context
     ↓
Agent Runtime       (Layer 2) — plan + tools
     ↓
Digital Workforce   (Layer 3) — role routing (v0.2+)
     ↓
Execution
     ↓
Security Validation (Layer 5) — trust + sandbox check
     ↓
Measurement
     ↓
Memory Update
```

---

## What v0.2.0 Delivers ("Architecture Complete")

- Full 9-layer directory and contract structure
- Strengthened Core with Security gate in the execution path
- Portfolio-wide subsystem registry mapping real beyond-repair repositories
- Digital Workforce role definitions (Engineer, Researcher, …)
- Research Fabric registration for CFT / Coherence Drive / Ware Constant lineage
- Security Fabric minimal enforcement (trust score + policy gate)
- Expanded coding agent + repository analysis
- Benchmark and metrics hooks
- Honest claim discipline (no false full-autonomy claims)

**Still out of scope for runtime claims:**  
Fully autonomous multi-agent companies, live economic settlement, production simulation environments, cloud multi-user deployment.

---

## Quick Start

```bash
git clone https://github.com/beyond-repair/ADL-Nexus.git
cd ADL-Nexus

python -m core.nexus status
python -m core.nexus run --goal "analyze repository" --path .
python -m core.nexus audit
python -m core.nexus memory
python -m core.nexus registry
```

---

## 12-Month End State

```
ADL Nexus
├── Governance
├── Memory
├── Agent Runtime
├── Workforce
├── Development Platform
├── Security Layer
├── Simulation Layer
└── Research Layer
```

Every existing repository becomes a subsystem, plugin, benchmark, research package, or archived historical artifact.

---

*Built under ADL-SEEM v3.0. Truth over Agreement. Verification over Plausibility. Governance first.*
