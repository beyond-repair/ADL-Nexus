# NEX-INT Spine Status

**Program:** Atomic Dream Labs Recursive Consolidation
**Branch:** `nex-int-spine`
**Updated:** 2026-09-07

## Locked Architecture

Nexus coordinates. It does not absorb Workforce, Sovereign Core, or AEGIS.

```
ADL-GOVERNANCE
       |
  policy / claims
       |
       v
  ADL-NEXUS (coordination)
       |
  +----+----+------------+
  v    v    v            v
Workforce  AEGIS  Clean Room  Research
```

## Gate Status

| Gate | State |
|------|-------|
| NEX-INT-001 Contract | LOCKED |
| NEX-INT-002 Nexus Adapter | PASS |
| NEX-INT-003 Workforce Executor | PASS |
| NEX-INT-004 Governed Vertical Slice | PASS (local) |
| NEX-INT-005 Durable Execution Identity | PASS (local) |
| NEX-INT-006 Recovery / Reconciliation | CLOSED (local) |
| NEX-INT-007 Asynchronous Execution | IN PROGRESS |
| ├─ async acceptance | PASS |
| ├─ Workforce worker ownership | PASS |
| ├─ Nexus completion callback | PASS |
| ├─ dual persistence | PASS |
| ├─ prior-gate regression | PASS |
| └─ restart semantics under async | NEXT |
| NEX-INT-008 Real Agent / LLM Handler | Pending |

## Permanent Rules

1. No automatic re-drive of uncertain RUNNING executions.
2. Absence of evidence is not evidence of safe re-execution.
3. Workforce owns Agent / Task lifecycle and evidence journal.
4. Nexus owns request identity, governance/security decisions, and audit.
5. Games (Project Cold Boot) are independent and protected.
6. Synchronous `submit()` remains the compatibility path; `submit_async()` is the NEX-INT-007 surface.

## Compatibility

```
submit(request)           → existing synchronous contract (NEX-INT-001..006)
submit_async(request)     → non-blocking async contract (NEX-INT-007)
submit(request, asynchronous=True) → same as submit_async
```
