# Roadmap

## Delivered
- v0.1–v0.3.0-rc1 Core / Hardened Runtime
- **Nexus Party client** (Godot 4 + web pixel chat) — Layer 6 interactive multi-agent UI

## v0.3.2 (claim-capped, partial)
- User-facing version **0.3.2** (not 0.4)
- Supervised workforce board: assign / tasks / complete (in-process; does not execute role work)
- Optional integrity anchors at `.nexus_anchors.json` in the cwd (not `.nexus/anchors.json`)
- Runtime pathway actions: `plan`, `execute`, `list_tools`, `history_tail`
- Local claim cap **2** enforced by the in-tree registry

## Not delivered (fail closed or absent)
- `nexus request` / `NexusKernel.request` — method returns `unavailable`; no request loop
- Loopback Party bridge `nexus serve` / `NexusKernel.serve_loopback` — does not bind; no server
- Live adapter execution (sunder SCAN/SNAP/SUNDER, sovereign clean-room as source of truth)
- ADL-Governance as a live kernel (normative text is vendored; it does not decide calls)

## Still target (not claimed done)
- Live adapter confirmation (sibling import still not live interop)
- Signed Play release pipeline
- Custom pixel portrait sprites
- Economic Layer beyond nominal ledger
- `nexus request` and loopback serve, if a later sweep actually builds them
