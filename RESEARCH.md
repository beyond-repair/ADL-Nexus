# RESEARCH lock — ADL-Nexus (Sweep-086 + Sweep-131)

**Classification:** RESEARCH (locked 2026-09-06, Sweep-086; reconfirmed Sweep-112 / Sweep-131).
**Branch:** `main` only.

## Verified this cycle (API + local evidence)

| Surface | Observation |
|---------|-------------|
| GitHub Actions | `ci.yml` present; docs-presence green; test job previously red due to incomplete spine imports |
| Local integrity | `save_anchor` / `check_anchor` / `ANCHOR_FILE` implemented and unit-tested |
| Local tests | 17 passed + 7 xfailed (spine methods not yet wired under claim-cap) |
| Adapter live mode | Tests allow `live` **or** `stub`; sibling repos not required |
| Layers 4 / 6 / 8 | Scaffold + code present; not product surfaces |
| Claim status file | Core claim level **2**; full workforce **false**; live interop **false** |

## Forbidden claims

- Production autonomous company / OS.
- Fully verified product CI for spine features still under xfail.
- Tagged release.
- Live interop with `sunder` or `sovereign-clean-room` unless a future sweep runs those adapters and records output.
- Signed Android APK in-repo.

## Successor / domain

Not SUPERSEDED. Canonical domains remain:
- Governance docs: `ADL-Governance`
- VSA runtime: `sovereign-clean-room`
- Coding agent experiment: `sunder`
- Workforce product: `Digital_Double_virtual_workforce`

Nexus is an integration sketch, not the canonical owner of those capabilities.
