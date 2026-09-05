# ADL Nexus

**Local-first autonomous engineering, governance, simulation, and workforce platform.**

**Version:** 0.1.0 (Core)  
**Owner:** beyond-repair / Atomic Dream Labs  
**Governance:** [ADL-Governance](https://github.com/beyond-repair/ADL-Governance) + [ADL-SEEM](https://github.com/beyond-repair/ADL-SEEM)

> The objective is not to create another repository.  
> The objective is to transform Atomic Dream Labs from a collection of projects into a single evidence-producing operating system for autonomous engineering and research.

---

## Design Principle

**Highest-leverage move is not to merge every repository into one giant application.**

That would create an unmaintainable system.

The strongest synthesis is a **layered architecture** where each major body of work becomes a subsystem, plugin, benchmark, research package, or archived historical artifact.

---

## Layered Architecture

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

### Layer 0 — Governance Kernel
**Sources:** ADL-Governance, AEGIS / forge-aegis, Capability Matrix, Portfolio Census, Repo Graph  
**Responsibilities:** Identity · Claims · Permissions · Audit · Lineage · Validation · Policy  
Every subsystem registers here. Nothing bypasses governance.

### Layer 1 — Memory Kernel
**Sources:** sovereign-clean-room, SEEM lineage, VSA / FHRR / BaNEL  
**Responsibilities:** Memory · Recall · Compression · Knowledge Graph · Embeddings · Identity Persistence  
Single source of truth. All agents use the same memory substrate.

### Layer 2 — Agent Runtime
**Sources:** sunder, Auto_Legion, GenieGPT, Agent-Snake  
**Responsibilities:** Planning · Task Decomposition · Tool Usage · Execution · Verification · Learning  
Operating system for agents.

### Layer 3 — Digital Workforce
**Sources:** Digital Double, Legion concepts  
**Responsibilities:** Engineer · Researcher · Writer · Analyst · Tester · Operator · Manager  
Not one AI. A managed workforce.

### Layer 4 — Development Environment
**Sources:** DevelopTool, RepoRover  
**Responsibilities:** Repository Analysis · Refactoring · Code Generation · Documentation · Testing · Dependency Mapping  
Agents work here. Humans supervise here.

### Layer 5 — Security Fabric
**Sources:** VigilE.S.A., Forge Aegis  
**Responsibilities:** Sandboxing · Trust Scoring · Threat Detection · Policy Enforcement · Artifact Integrity  
Every action passes through validation.

### Layer 6 — Simulation Fabric
**Sources:** Cold Boot systems, Blacksite systems  
**Responsibilities:** Scenario Testing · Agent Training · Economic Simulation · World Models · Game Environments  
Games become test environments, not separate products.

### Layer 7 — Research Fabric
**Sources:** Coherence Drive, CFT, Ware Constant phenomenology, physics repos  
**Responsibilities:** Hypothesis Tracking · Experiment Registry · Simulation · Replication · Evidence Management  
Claims cannot advance without validation.

### Layer 8 — Economic Layer
**Sources:** FortiTrade lessons, automation projects  
**Responsibilities:** Billing · Marketplaces · Agent Commerce · Subscription Management · Revenue Tracking  
Monetization lives here.

---

## Unified Workflow

```
User Request
     ↓
Governance          (Layer 0)
     ↓
Memory              (Layer 1)
     ↓
Agent Runtime       (Layer 2)
     ↓
Digital Workforce   (Layer 3)
     ↓
Execution
     ↓
Security Validation (Layer 5)
     ↓
Measurement
     ↓
Memory Update
```

---

## First Real Product — ADL Nexus Core v0.1

**Do not attempt to build the full stack.**

### Scope (strict)

1. Local-first
2. Governance enforced
3. Shared memory
4. Coding agent
5. Repository analysis
6. Benchmark system
7. Metrics dashboard

**Nothing else.**

### Non-Goals for v0.1
- Full Digital Workforce roles
- Simulation / game environments
- Economic / billing layer
- Complete Research Fabric UI
- Multi-user cloud deployment

---

## Repository Structure (v0.1)

```
ADL-Nexus/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── GOVERNANCE.md
│   ├── CLAIM_STATUS.md
│   └── ROADMAP.md
├── layer0_governance/     # Kernel registration, claims, audit
├── layer1_memory/         # Shared memory substrate (VSA / clean-room hooks)
├── layer2_agent_runtime/  # Planning + tool execution loop
├── core/                  # Nexus Core entrypoint + coding agent
├── analysis/              # Repository analysis tools
├── benchmarks/            # Benchmark system
├── dashboard/             # Metrics dashboard (local)
├── registry/              # Subsystem registration manifests
└── tests/
```

---

## 12-Month End State (Target)

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

Every existing beyond-repair repository becomes either:
- a subsystem,
- a plugin,
- a benchmark,
- a research package,
- or an archived historical artifact.

---

## Quick Start (v0.1 Scaffold)

```bash
git clone https://github.com/beyond-repair/ADL-Nexus.git
cd ADL-Nexus

# Local-first: no external services required for core path
python -m core.nexus --help
```

---

## Governance & Claim Discipline

This repository is governed by ADL-Governance and ADL-SEEM.  
Default claim level for v0.1: **1–2** (architectural + local runnable stubs).  
Experimental validation of full autonomous workforce: **false**.

See `docs/CLAIM_STATUS.md`.

---

*Built under ADL-SEEM v3.0. Truth over Agreement. Verification over Plausibility. Governance first.*
