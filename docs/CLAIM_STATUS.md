# Claim Status — ADL Nexus

**Sweep-121 (2026-09-08):** v0.3.2 local kernel completion. Head recorded at push time.

| Field | Value |
|-------|--------|
| Version | **0.3.2** |
| Lifecycle | **RESEARCH** (not ACTIVE product) |
| Core claim level | **2** |
| Packaged pathways (stdlib import + `python run.py`) | **VERIFIED** in-tree |
| Architecture core path `request()` | **VERIFIED** local deterministic loop |
| Supervised workforce assign/complete | **VERIFIED** in-process board (not autonomy) |
| Optional integrity anchors `.nexus/anchors.json` | **VERIFIED** local only |
| Loopback Party bridge `serve` 127.0.0.1 | **PRESENT**; remote bind refused |
| Product GitHub Actions pytest | `.github/workflows/ci.yml` present; treat run conclusion separately |
| Releases / tags | **none** |
| Live sunder / clean-room adapter | **UNSUPPORTED** as live interop (stub-pass ≠ live) |
| Full autonomous workforce | **UNSUPPORTED** |
| Production platform / OmniWealth OS / AI Legion runtime | **UNSUPPORTED** |
| Pre-built signed APK | **false** |

Do not infer production completeness from layered directory names.
Do not promote lifecycle to ACTIVE because local tests pass.
