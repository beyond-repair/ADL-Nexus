# NEX-INT-007 — Asynchronous Execution

## Objective

Allow a governed WorkRequest to be accepted and return without blocking on handler completion, while preserving every invariant from NEX-INT-001–006.

## Path

```
WorkRequest
    ↓
Governance + Security
    ↓
Durable Nexus identity (RUNNING)
    ↓
submit_async()
    ↓
Workforce-owned worker
    ↓
handler
    ↓
Workforce evidence journal (terminal)
    ↓
completion callback
    ↓
Nexus ExecutionRecord (terminal)
```

## Ownership

| Concern | Owner |
|---------|-------|
| Worker pool / handles | Workforce |
| Handler invocation | Workforce |
| Evidence journal | Workforce |
| Request identity + audit | Nexus |
| Completion callback consumption | Nexus |

## Next sub-gate

Async process-death / restart:

```
submit_async() → RUNNING → Workforce executing → process death
    ↓
restart → NEX-INT-006 recovery → Workforce evidence
    ↓
RECONCILE or INDETERMINATE → NO RE-DRIVE
```
