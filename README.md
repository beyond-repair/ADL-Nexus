# ADL Nexus

**Local-first autonomous engineering, governance, simulation, and workforce platform.**

**Version:** 0.3.0-rc1  
**Lifecycle:** **RESEARCH** (Sweep-086 lock) — not ACTIVE product.  
**Owner:** beyond-repair / Atomic Dream Labs  
**Governance:** [ADL-Governance](https://github.com/beyond-repair/ADL-Governance) + [ADL-SEEM](https://github.com/beyond-repair/ADL-SEEM)

See [RESEARCH.md](RESEARCH.md) and [docs/CLAIM_STATUS.md](docs/CLAIM_STATUS.md).

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

Local CLI is present. **GitHub Actions workflows = 0 this sweep. Do not treat CLI presence as CI-verified.**

### Activate live adapters (optional)

Place `sunder` and/or `sovereign-clean-room` as sibling directories, or:

```bash
eval $(python scripts/bootstrap_path.py --export)
python -m core.nexus adapters
```

Core also attempts `ensure_paths()` automatically on startup. Adapter tests pass in **stub** mode without siblings.

---

## Layers

| Layer | Status (claim-capped) |
|-------|------------------------|
| 0 Governance | Code present; CI **absent** |
| 1 Memory + clean-room adapter | Code present; live adapter **UNVERIFIED** |
| 2 Agent Runtime + sunder adapter | Code present; live adapter **UNVERIFIED** |
| 3 Workforce roles | Defined (not full autonomy) |
| 4 Development | Scaffolded |
| 5 Security + integrity | Code present; CI **absent** |
| 6 Simulation | Scaffolded |
| 7 Research + CFT evidence | Registry present |
| 8 Economic | Scaffolded |

---

*Built under ADL-SEEM v3.0. Governance first. Claim-capped adapters. Sweep-086.*
