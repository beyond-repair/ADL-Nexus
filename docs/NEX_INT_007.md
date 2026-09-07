# NEX-INT-007 — Asynchronous Execution

## Status: IN PROGRESS (implementation landed; full CI pending)

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
- [ ] Full repository CI green on `nex-int-spine`

### Local adversarial suite

Command:
```
python tests/test_nex_int_007_adversarial.py
```
Result: **7 passed, 0 failed**

### Implementation commit

`f55f8912da9c7d0c7862fe1698f4698b4eb95f87`

### Files

- `governed_workforce.py`
- `persistence/` (store, recovery, execution_state)
- `adapters/workforce/adapter.py` (thin; invocation counting)
- `tests/test_nex_int_007_adversarial.py`

### Closure rule

NEX-INT-007 closes only when full repo CI on this branch is evidenced PASS in addition to the above.
