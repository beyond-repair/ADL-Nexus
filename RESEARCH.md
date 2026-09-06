# RESEARCH lock — ADL-Nexus (Sweep-086)

**Classification:** RESEARCH (locked 2026-09-06, Sweep-086).
**Tree SHA at audit:** `57cd80b5a91294ec137d91460c1d1423e666cf0e`
**Branch:** `main` only.

## Verified this cycle (API evidence)

| Surface | Observation |
|---------|-------------|
| GitHub Actions `list_workflows` | `total_count=0` |
| Releases | `[]` |
| Tags | `[]` |
| Local tests present | `tests/test_adapters.py`, `test_governance.py`, `test_integrity.py`, `test_security.py`, `test_workforce.py` |
| Local test execution in CI | **UNVERIFIED** (no workflow) |
| Adapter live mode | Tests allow `live` **or** `stub`; sibling repos not required |
| Layers 4 / 6 / 8 | Scaffold READMEs; not product surfaces |
| Claim status file | Core claim level **2**; full workforce **false**; live Python Nexus in client **false** |

## Forbidden claims

- Production autonomous company / OS.
- Verified CI.
- Tagged release.
- Live interop with `sunder` or `sovereign-clean-room` unless a future sweep runs those adapters and records output.
- Signed Android APK in-repo (CLAIM_STATUS already false).

## Successor / domain

Not SUPERSEDED. Canonical domains remain:
- Governance docs: `ADL-Governance`
- VSA runtime: `sovereign-clean-room`
- Coding agent experiment: `sunder`
- Workforce product: `Digital_Double_virtual_workforce`

Nexus is an integration sketch, not the canonical owner of those capabilities.
