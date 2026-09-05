# ADL Nexus Architecture

## Core Invariant

Nothing executes outside the Governance Kernel (Layer 0).

Every subsystem must:
1. Register its identity and capability surface.
2. Declare claim level.
3. Accept audit and lineage requirements.
4. Route all state-changing actions through validation.

## Layer Contracts (v0.1)

### Layer 0 — Governance Kernel
- Identity registry
- Claim validation
- Permission checks
- Audit log append-only
- Lineage / provenance
- Policy evaluation

### Layer 1 — Memory Kernel
- Shared key-value + vector + graph substrate
- VSA / clean-room hooks (sovereign-clean-room)
- Identity persistence across sessions
- Single source of truth for all agents

### Layer 2 — Agent Runtime
- Goal → plan → tool calls → verification loop
- Coding agent as first concrete instance
- Local tool sandbox only in v0.1

### Higher Layers (stubs only in v0.1)
Layers 3–8 exist as registration points and documentation.  
No production runtime claims are made for them in v0.1.

## Data Flow (Core Path)

```
Request
  → Governance.evaluate(request)
  → Memory.retrieve(context)
  → AgentRuntime.plan_and_execute()
  → Security.validate(actions)   # minimal in v0.1
  → Measurement.record()
  → Memory.update()
```

## Subsystem Registration

Every external repository that becomes a subsystem must provide a `nexus-manifest.yaml` (or equivalent) declaring:
- name
- layer
- claim_level
- capabilities
- dependencies
- audit_hooks
