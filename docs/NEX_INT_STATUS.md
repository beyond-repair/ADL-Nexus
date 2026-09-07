# NEX-INT Spine Status

**Program:** Atomic Dream Labs Recursive Consolidation
**Branch:** `nex-int-spine`
**Updated:** 2026-09-07
**HEAD (implementation):** `f55f8912da9c7d0c7862fe1698f4698b4eb95f87`

## Gate Status

| Gate | State |
|------|-------|
| NEX-INT-001 Contract | LOCKED |
| NEX-INT-002 Nexus Adapter | PASS |
| NEX-INT-003 Workforce Executor | PASS (Workforce repo) |
| NEX-INT-004 Governed Vertical Slice | PASS (code on branch) |
| NEX-INT-005 Durable Execution Identity | PASS (code on branch) |
| NEX-INT-006 Recovery / Reconciliation | CLOSED (code on branch) |
| NEX-INT-007 Asynchronous Execution | IN PROGRESS |
| ├─ governed_workforce + recovery | LANDED remote |
| ├─ adversarial A–F | PASS local (7/7) |
| ├─ boundary audit (AST) | PASS local |
| └─ full repo CI on branch | PENDING |
| NEX-INT-008 Real Agent / LLM Handler | NOT STARTED |

## Permanent Rules

1. No automatic re-drive of uncertain RUNNING executions.
2. Absence of evidence is not evidence of safe re-execution.
3. Workforce owns Agent / Task lifecycle and evidence journal.
4. Nexus owns request identity, governance/security decisions, and audit.
5. Games (Project Cold Boot) are independent and protected.
6. Late callbacks cannot resurrect terminal or INDETERMINATE executions.

## Compatibility

```
submit(request)                    → synchronous
submit_async(request)              → non-blocking
submit(request, asynchronous=True) → same as submit_async
```
