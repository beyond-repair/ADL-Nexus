# ADL Nexus Architecture — Complete

## Core Invariant

Nothing executes outside the Governance Kernel (Layer 0).

Every subsystem must:
1. Register its identity and capability surface.
2. Declare claim level.
3. Accept audit and lineage requirements.
4. Route all state-changing actions through validation.

## Layer Contracts

### Layer 0 — Governance Kernel (Active)
Identity registry · Claim validation · Permission checks · Append-only audit · Lineage · Policy evaluation

### Layer 1 — Memory Kernel (Active)
Shared local KV + future VSA/graph substrate. Single source of truth.

### Layer 2 — Agent Runtime (Active)
Goal → plan → tool calls → verification. Coding agent is the first concrete instance.

### Layer 3 — Digital Workforce (Scaffolded)
Role definitions: Engineer, Researcher, Writer, Analyst, Tester, Operator, Manager.
Routing only; full autonomy not claimed.

### Layer 4 — Development Environment (Scaffolded)
Repository analysis, future refactoring / code-generation surface.

### Layer 5 — Security Fabric (Active minimal)
Trust scoring, policy gate, sandbox declaration. Every Core action passes through it.

### Layer 6 — Simulation Fabric (Scaffolded)
Registration point for blacksite, Cold Boot / Godot, world-model test environments.

### Layer 7 — Research Fabric (Active registry)
Hypothesis / experiment / evidence registration. CFT, Coherence Drive, Ware Constant lineage mapped.

### Layer 8 — Economic Layer (Scaffolded)
Future billing, marketplace, agent commerce hooks.

## Data Flow (Core Path v0.2)

```
Request
  → Governance.evaluate()
  → Memory.retrieve()
  → AgentRuntime.plan_and_execute()
  → Security.validate()
  → Measurement.record()
  → Memory.update()
```
