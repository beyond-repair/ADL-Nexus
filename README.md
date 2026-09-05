# ADL Nexus

**Local-first autonomous engineering, governance, simulation, and workforce platform.**

**Version:** 0.3.0-beta (Hardened Runtime)  
**Owner:** beyond-repair / Atomic Dream Labs  
**Governance:** [ADL-Governance](https://github.com/beyond-repair/ADL-Governance) + [ADL-SEEM](https://github.com/beyond-repair/ADL-SEEM)

> Transform Atomic Dream Labs from a collection of projects into a single evidence-producing operating system for autonomous engineering and research — without merging everything into one unmaintainable monolith.

---

## Status

| Layer | Status |
|-------|--------|
| 0 Governance | **Active** |
| 1 Memory + clean-room adapter | **Active** (live engine when importable) |
| 2 Agent Runtime + sunder adapter | **Active** (claim-capped) |
| 3 Workforce roles | Defined |
| 4 Development | Scaffolded |
| 5 Security (policy table) | **Active** |
| 6 Simulation | Scaffolded |
| 7 Research + CFT evidence | **Active** |
| 8 Economic | Scaffolded |

---

## Quick Start

```bash
git clone https://github.com/beyond-repair/ADL-Nexus.git
cd ADL-Nexus

python -m core.nexus status
python -m core.nexus run --goal "analyze repository"
python -m core.nexus research
python -m core.nexus adapters
python -m core.nexus metrics
python -m core.nexus audit
```

To activate live clean-room mode, put `sovereign-clean-room` on `PYTHONPATH` (so `core.clean_room_vsa` imports).

---

*Built under ADL-SEEM v3.0. Governance first. Claim-capped adapters.*
