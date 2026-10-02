# Governance Integration

ADL Nexus is subordinate to:

- [ADL-Governance](https://github.com/beyond-repair/ADL-Governance)
- [ADL-SEEM](https://github.com/beyond-repair/ADL-SEEM)
- [forge-aegis](https://github.com/beyond-repair/forge-aegis) (AEGIS / Artifact Graph integrity)

**Classification:** RESEARCH (Sweep-086 lock; Sweep-112 reconfirm).
**Canonical owner for portfolio governance docs:** ADL-Governance.
**Canonical VSA / SEEM runtime:** sovereign-clean-room (not this repo).
**Canonical workforce product surface:** Digital_Double_virtual_workforce (not this repo).

## Non-Negotiable Rules

1. No subsystem may self-elevate claim level.
2. All state mutations must be auditable.
3. Local-first default: no network calls required for Core path.
4. Human override always takes precedence.
5. Fail-closed on policy violation.
6. Layer folders are not proof of implemented capability.

## Registration Requirement

Before a subsystem is considered active inside Nexus, it must be entered in `registry/` with a signed (or hash-anchored) manifest.


## Imported constitution (text only)

`imported/adl_governance/` holds verbatim copies of `CONSTITUTION.md`, `CLAIM_VALIDATION.md`, and `LIFECYCLE.md` from ADL-Governance `main` commit `c2f677ff9613fc2c9614535b1bb34e1b3d8857ed`. `SOURCE.txt` records that commit and the SHA-256 of each file. `layer0_governance.imported_constitution.load_import` refuses startup when a file is missing or the hash does not match.

That import is not a live kernel. It is not RealityOS, Sunder, or a clean-room engine. `layer0_governance.registry` remains the decision stand-in. It still has no human-override channel and no signed-manifest check.

## Local ceiling (this repository)

Published claim is **≤1**. The stand-in enforces `claim_level <= 2` (`MAX_CLAIM_LEVEL`). `register_subsystem` rejects a claim above that ceiling and rejects self-elevation of an existing subsystem. `evaluate_request` denies any stored claim above the ceiling, including action `status`. Refusing 3–5 is not evidence of CLAIM_VALIDATION Level 2.
