# Catalog Gap Report — 2026-10-27T230933Z

**Source:** Live GitHub search `user:beyond-repair` total_count=83, incomplete_results=false (reconfirmed via observed_2026_10_27.py freeze).

**Locked artifacts:**
- adl-capability-matrix: inventory_count=67 rows (capability_matrix.json)
- aegis-repo-graph: 72 repository artifacts (catalog.py rows, snapshot 2026-09-04)

## Matrix Gap (observed - matrix): 16 names — UNASSIGNED

cluster and claim_cap remain null (do not invent). Expansion is operator-only.

1. ADL-Nexus
2. Open-Energy-Fusion
3. Sovereign-Epistemic-Reality-Engine
4. adl-capability-matrix
5. adl-function-census
6. atomicdreamlabs
7. bloch-coherence-factor2
8. finite-gasket-spectral-derivatives
9. informational-flux-identity
10. mend
11. mendthegame
12. os-family-constitution-map
13. scale-functional-I
14. seem-identity-unifier
15. seem-sunder-bridge
16. sunder-cleanroom-vsa-adapter

## Catalog Gap (observed - catalog): 18 names — UNASSIGNED / observation-only

1. ADL-Nexus
2. CFTv3.3-IQG-Unified-Framework  (spelling variant; catalog has CFT-v3.3-IQG-Unified-Framework)
3. Open-Energy-Fusion
4. RealityOS
5. Sovereign-Epistemic-Reality-Engine
6. adl-capability-matrix
7. adl-function-census
8. atomicdreamlabs
9. bloch-coherence-factor2
10. finite-gasket-spectral-derivatives
11. informational-flux-identity
12. mend
13. mendthegame
14. os-family-constitution-map
15. scale-functional-I
16. seem-identity-unifier
17. seem-sunder-bridge
18. sunder-cleanroom-vsa-adapter

## Catalog-only (catalog - observed): 7 names

These are absent from the 2026-10-27 search freeze. Some are planned queue or historical.

1. CFT-v3.3-IQG-Unified-Framework (spelling variant of observed CFTv3.3-...)
2. MyCore
3. SuperAGI
4. bolt.new
5. clean-room-skill-export (planned queue)
6. docs
7. sunder-aegis-bridge (planned queue)

## Notes

- Intersection matrix ∩ catalog = 65.
- Matrix ⊂ observed (no matrix names missing from live search).
- Claim status for both tools remains ≤1 / RESEARCH. Locked inventories are snapshots, not live completeness.
- No mutations to locked JSON or catalog rows performed. This report is additive observation only.
- Deterministic comparison via local Python on frozen observed list + locked files.

Evidence: downloaded capability_matrix.json, catalog.py, observed_2026_10_27.py; set difference computation.
