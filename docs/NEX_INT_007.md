# NEX-INT-007 — Asynchronous Execution

## Status: CLOSED

**Branch:** `nex-int-spine`
**HEAD:** `91db04720da3e07a38cc51b71b5a8138e3fda1bd`
**Implementation SHA:** `f55f8912da9c7d0c7862fe1698f4698b4eb95f87`
**CI fix SHA:** `91db04720da3e07a38cc51b71b5a8138e3fda1bd`
**Closure date:** 2026-09-07

### Acceptance criteria

- [x] Non-blocking accept path (`submit_async`)
- [x] Durable identity before Workforce invocation
- [x] Completion callback cannot overwrite terminal state
- [x] Recovery leaves INDETERMINATE without re-drive when no terminal evidence
- [x] Late callback after recovery ignored
- [x] Concurrent duplicate request_id → single Workforce invocation
- [x] Submit after terminal → observation only
- [x] Submit after INDETERMINATE → no re-drive
- [x] Boundary: no Agent/Task/Orchestrator imports in Nexus governed path
- [x] Full repository tests on branch PASS

### Full repository suite

```
command: python -m pytest -q
branch: nex-int-spine
result: 17 passed, 0 failed
exit: 0
```

### Adversarial suite

```
command: python tests/test_nex_int_007_adversarial.py
result: 7 passed, 0 failed
```

A–F invariants verified. Boundary AST audit PASS.

### Minimal defects fixed for CI

1. `layer5_security/gate.py` — add `execute_work` (and `integrity`) to allow policy so governed workforce is not false-denied.
2. `layer3_workforce/roles.py` — field order fix (pre-existing dataclass TypeError blocking collection).

### NEX-INT-008

NOT STARTED. Next: Gate 1 only — narrow handler contract.
