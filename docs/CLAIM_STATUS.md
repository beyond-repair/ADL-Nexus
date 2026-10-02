# Claim Status — ADL Nexus

**Local repair:** claim cap enforced; mutating CLI commands go through `NexusKernel.call`; empty xfails replaced with contract tests. Lifecycle is still **RESEARCH**.

| Field | Value |
|-------|--------|
| Version | **0.3.2** (pyproject, CLI help, and `kernel.status`). Not 0.4. |
| Lifecycle | **RESEARCH** (not ACTIVE product) |
| Core claim level | **2**, enforced (`claim_level <= 2`). README badge matches this cap. |
| ADL-Governance package | **UNSUPPORTED** as an import. External dependency. Local registry is the stand-in only. |
| Product contract | `docs/PRODUCT.md` — nine subsystems; absorb on strength only |
| Local integrity anchors (`save_anchor` / `check_anchor`) | **VERIFIED** (unit). File is `.nexus_anchors.json` in the cwd, not `.nexus/anchors.json`. |
| Supervised workforce assign/complete (in-process) | **VERIFIED** — assign checks the role contract (unknown role and a capability outside that contract are rejected; no task is stored). complete only flips pending/assigned to complete. Execution is not implemented. |
| `think` / `authorize` / `commit` on NexusKernel | **LOCAL** — ObjectiveEngine is called after a governance check. Commit assigns a task only when authorized. Not autonomous execution. |
| Runtime pathway `execute` | **LOCAL** — actions `plan`, `execute`, `list_tools`, `history_tail`. Each planned tool is governance-checked. |
| `NexusKernel.request` / `serve_loopback` | **UNSUPPORTED** — fail closed with a deterministic error. No server is started. |
| Reality / provenance pathways | **LOCAL** — registered actions only (`reality` state/info, `provenance` list/get/record). Reality stays `live: false` and is not RealityOS; confidence is labeled hardcoded. Unknown actions deny. |
| cleanroom `query` | **DENIED** on purpose. Not a declared pathway action. `SecurityGate` unknown-action heuristic trust **0.25** (below 0.5). Not added to `POLICY["allow"]`. |
| Live RealityOS twin | **UNSUPPORTED** |
| Live Digital Double runtime | **UNSUPPORTED** |
| Live sunder / clean-room / AEGIS pipeline | **UNSUPPORTED** — missing sunder is `unavailable`; import without a real `scan` call is `detected`, not `live` |
| Full autonomous workforce / deploy / payments | **UNSUPPORTED** |
| Physics / Coherence Drive as product features | **FORBIDDEN** (research lab only). Kernel bootstrap does not seed CFT. Explicit `research --seed` and `seed_cft_baseline()` can. |

Do not infer production completeness from layered directory names.
Do not promote lifecycle to ACTIVE because local tests pass.
