# ADL Nexus

**Local-first autonomous engineering, governance, simulation, and workforce platform.**

**Version:** 0.3.0-rc1  
**Owner:** beyond-repair / Atomic Dream Labs  
**Governance:** [ADL-Governance](https://github.com/beyond-repair/ADL-Governance) + [ADL-SEEM](https://github.com/beyond-repair/ADL-SEEM)

---

## Quick Start

```bash
git clone https://github.com/beyond-repair/ADL-Nexus.git
cd ADL-Nexus

python -m core.nexus status
python -m core.nexus adapters
python -m core.nexus research
python -m core.nexus metrics
python -m core.nexus integrity --path .
python -m core.nexus run --goal "analyze repository"
```

### Activate live adapters (optional)

Place `sunder` and/or `sovereign-clean-room` as sibling directories, or:

```bash
eval $(python scripts/bootstrap_path.py --export)
python -m core.nexus adapters
```

Core also attempts `ensure_paths()` automatically on startup.

---

## Layers

| Layer | Status |
|-------|--------|
| 0 Governance | Active |
| 1 Memory + clean-room adapter | Active |
| 2 Agent Runtime + sunder adapter | Active |
| 3 Workforce roles | Defined |
| 4 Development | Scaffolded |
| 5 Security + integrity | Active |
| 6 Simulation | Scaffolded |
| 7 Research + CFT evidence | Active |
| 8 Economic | Scaffolded |

---

*Built under ADL-SEEM v3.0. Governance first. Claim-capped adapters.*
