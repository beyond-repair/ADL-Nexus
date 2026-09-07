# ADL Nexus

**Local-first autonomous engineering, governance, simulation, and workforce platform.**

**Version:** 0.3.0-rc1  
**Lifecycle:** **RESEARCH** (Sweep-086 lock; Sweep-112 reconfirm) — not ACTIVE product.  
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

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -e .

nexus status
nexus adapters
nexus research
nexus metrics
nexus integrity --path .
nexus run --goal "analyze repository"
```

Module form without installing:

```bash
python -m core.nexus status
```

Local CLI is present. Sweep-112 added `.github/workflows/ci.yml`. Treat first Actions conclusion as **PENDING** until listed success.

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
| 4 Development | Scaffolded |
| 5 Security + integrity | Code present |
| 6 Simulation | Scaffolded |
| 7 Research + CFT evidence | Registry present |
| 8 Economic | Scaffolded |

---

## Packaging notes

- `pyproject.toml` defines the installable package and the `nexus` console script.
- After `pip install -e .` the project root packages are importable and the CLI is on `PATH`.
- Zero external runtime dependencies by design.

---

*Built under ADL-SEEM v3.0. Governance first. Claim-capped adapters. Sweep-112.*
