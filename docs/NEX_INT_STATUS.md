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
| NEX-INT-007 Asynchronous Execution | NEXT |
| NEX-INT-008 Real Agent / LLM Handler | Pending |

## Permanent Rules

1. No automatic re-drive of uncertain RUNNING executions.
2. Absence of evidence is not evidence of safe re-execution.
3. Workforce owns Agent / Task lifecycle and evidence journal.
4. Nexus owns request identity, governance/security decisions, and audit.
5. Games (Project Cold Boot) are independent and protected.

## Files on this branch

- `adapters/workforce/contract.py` — frozen vocabulary
- `adapters/workforce/adapter.py` — thin Nexus-side adapter
- `persistence/` — durable ExecutionRecord + store
