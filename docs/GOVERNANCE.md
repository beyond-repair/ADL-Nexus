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
