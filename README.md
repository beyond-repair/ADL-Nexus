# ADL Nexus

**Local-first autonomous engineering, governance, simulation, and workforce platform.**

**Version:** 0.3.2  
**Lifecycle:** **RESEARCH** (Sweep-086 lock; Sweep-112/131 reconfirm) — not ACTIVE product.  
**Owner:** beyond-repair / Atomic Dream Labs  
**Governance:** [ADL-Governance](https://github.com/beyond-repair/ADL-Governance) + [ADL-SEEM](https://github.com/beyond-repair/ADL-SEEM)

See [RESEARCH.md](RESEARCH.md) and [docs/CLAIM_STATUS.md](docs/CLAIM_STATUS.md).

Production / live-adapter / full-workforce claims are **UNSUPPORTED**.

---

## Quick Start (clone & run)

Requires **Python 3.10+**. No third-party runtime dependencies (stdlib only).

```bash
git clone https://github.com/beyond-repair/ADL-Nexus.git
cd ADL-Nexus

# Easiest — no install, no venv required (stdlib only):
python run.py status
python run.py packages          # verify every packaged module imports
python run.py layers            # show pathway → module map
python run.py call --pathway development --action analyze --kw path=.
python run.py run --goal "analyze repository"
```

Installable form (puts `nexus` on PATH):

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e .

nexus status
nexus packages
nexus adapters
nexus research
nexus metrics
nexus integrity --path .
nexus run --goal "analyze repository"
```

Module form without installing:

```bash
python -m core status
python -m core.nexus status
```

Local CLI is present. Sweep-112 added `.github/workflows/ci.yml`. CI present; spine-related tests xfail under RESEARCH claim-cap (Sweep-131).

### Optional: activate live adapters

Place `sunder` and/or `sovereign-clean-room` as sibling directories (or under `vendor/`), or:

```bash
eval $(python scripts/bootstrap_path.py --export)
nexus adapters
```

Core also attempts `ensure_paths()` automatically on startup. Adapter tests pass in **stub** mode without siblings. Stub-pass is **not** live interop.

### Development / tests

```bash
pip install -e ".[dev]"
pytest
```

---

## Layers

| Layer | Status (claim-capped) |
|-------|------------------------|
| 0 Governance | Code present; first product CI **PENDING** |
| 1 Memory + clean-room adapter | Code present; live adapter **UNSUPPORTED** |
| 2 Agent Runtime + sunder adapter | Code present; live adapter **UNSUPPORTED** |
| 3 Workforce roles | Defined (not full autonomy) |
| 4 Development | Code present (analyze pathway) |
| 5 Security + integrity | Code present |
| 6 Simulation | Code present (register/list pathway) |
| 7 Research + CFT evidence | Registry present |
| 8 Economic | Code present (nominal ledger; not payments) |

---

## Packaging notes

- `pyproject.toml` defines the installable package and the `nexus` console script.
- After `pip install -e .` the project root packages are importable and the CLI is on `PATH`.
- Zero external runtime dependencies by design.
- `python run.py` works from a fresh clone with no install.
- `nexus packages` / `nexus layers` / `nexus call` are the pathway surface.

---

*Built under ADL-SEEM v3.0. Governance first. Claim-capped adapters. Packaged pathways. Sweep-113.*
