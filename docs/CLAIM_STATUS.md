# Claim Status — ADL Nexus

| Field | Value |
|-------|--------|
| Classification | RESEARCH / ENGINEERING PLATFORM |
| Version | 0.3.0-alpha |
| Default claim level | **2** |
| Full autonomous workforce | **false** |
| Production simulation | **false** |
| Economic settlement | **false** |
| Local-first Core path | **true** |
| Security gate in path | **true** (minimal) |
| sunder adapter | **true** (claim-capped, no hard runtime dependency) |
| clean-room adapter | **true** (claim-capped, no hard runtime dependency) |
| Deep VSA interop | **false** (deferred) |
| Live VigilE.S.A. engine | **false** (deferred) |

Adapters are deliberately fail-soft: they detect presence of upstream packages when available and otherwise operate in stub mode. No claim of full interop is made until tests prove it.
